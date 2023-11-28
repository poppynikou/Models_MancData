import nibabel as nib
import numpy as np 
from utils import *
import sys
import os 

base_path = sys.argv[1]
Anonymisation_key_path = sys.argv[2]
Patient = int(sys.argv[3])
Model = int(sys.argv[4])
Numcps = int(sys.argv[5])

structures = ['BRAINSTEM', 'CORD', 'CTVHIGH', 'CTVLOW', 'CTVMEDIUM', 'LPAROTID', 'RPAROTID']

if Model == 0:
    results_path = base_path + '/LOO/PSM_CPS_' + str(Numcps) + '/HN_' + str(Patient) 
elif Model == 1:
    results_path = base_path + '/noLOO/PSM_CPS_' + str(Numcps) + '/HN_' + str(Patient) 

text_file = results_path + '/GeometricResults.txt'
if os.file.exists(text_file):
    os.remove(text_file)

file = open(text_file, 'a')
file.write('PATIENT TIMEPOINT STRUCTURE DICE AVERAGE_SDISTANCE 95_SDISTANCE \n')

timepoints = get_timepoints(Anonymisation_key_path, Patient)

for timepoint in timepoints[1:-1]:
        
        for structure in structures:

            gt_binary_path = base_path + '/CPPs/HN_'+str(Patient) + '/CBCT_' + str(timepoint) + '/BIN_' + str(structure) + '.nii.gz'
            print(gt_binary_path)
            
            if os.path.exists(gt_binary_path):

                test_binary_path = results_path + '/BIN_' + str(structure) + '_T_' + str(timepoint) + '.nii.gz'
                print(test_binary_path)

                gt_binary_obj, _, _ = get_image_objects(gt_binary_path)
                gt_binary = np.array(gt_binary_obj, dtype = np.bool8).copy()
                del gt_binary_obj
                del _

                test_binary_obj, _, test_binary_hdr = get_image_objects(test_binary_path)
                test_binary = np.array(test_binary_obj, dtype = np.bool8).copy()
                del test_binary_obj
                del _

                # define pixel dimensions for the distance calculations
                pix_dimensions = test_binary_hdr['pixdim']
                voxel_Spacing = [pix_dimensions[1], pix_dimensions[2], pix_dimensions[3]]


                # catch any images which now contain no image because of error 
                #Empty = no voxels 
                if (is_empty(test_binary)) or (is_empty(gt_binary)):
                    # write to file 
                    file.write(str(Patient) + ' ' + str(timepoint) + ' ' + str(structure) + ' Empty Empty Empty \n')
                else:
                    
                    # calculate statistics 
                    DICE_score = dc(test_binary, gt_binary)
                    HausdorfDistance = hd95(test_binary, gt_binary, voxelspacing=voxel_Spacing, connectivity=1)
                    AverageDistance = asd(test_binary, gt_binary, voxelspacing=voxel_Spacing, connectivity=1)

                    # write to file 
                    file.write(str(Patient) + ' ' + str(timepoint) + ' ' + str(structure) + ' ' + str(DICE_score) + ' ' + str(AverageDistance) + ' ' + str(HausdorfDistance)  + '\n')

                
