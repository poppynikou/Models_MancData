import os
import shutil 
from Patient_Info_Functions import *
import numpy as np 
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'

base_path = 'T:/Poppy/PatData/'

patients = [3]#np.arange(3,10)
no_iterations = 2 # i dont want to use all the itterations - I don't think it makes any difference on this data 
# gives you one updated Sform image at the end 
for patient in patients:

    CBCTs = get_time_points(base_path, patient)

    postprocessing_directory = 'T:/Poppy/PatData/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/'
    if not os.path.exists(postprocessing_directory):
        os.mkdir(postprocessing_directory)

    for CBCT in CBCTs:

        CBCT_original = 'T:/Poppy/PatData/HN_'+str(patient)+'/CBCT_GROUPWISE/preprocessing/CBCT_' + str(CBCT) + '.nii.gz'
        destination = postprocessing_directory + '/CBCT_' + str(CBCT) + '.nii.gz'
        shutil.copy(CBCT_original, destination)

        for itteration in np.arange(1,no_iterations+1):
            
            affine = 'T:/Poppy/PatData/HN_'+str(patient)+'/CBCT_GROUPWISE/affine_'+str(itteration)+'/comp_affine_' + str(CBCT) + '.txt'

            # update Sform of image
            img_to_be_updated = destination
            affine = affine
            updated_img = postprocessing_directory + 'CBCT_' + str(CBCT) + '.nii.gz'
            command = reg_transform + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
            os.system(command)


