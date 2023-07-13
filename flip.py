import nibabel as nib 
import numpy as np 
import os 
from flip_utils import * 

'''
Script which flips images so that all patients are ipsilateral on the right hand side. 
Voxels are summed on the left and right hand side of the image. 
The middle of the image is calculated using the location of the voxel in the middle of the first slice of the spinal cord.  
Images and binary structure files are all flipped and resaved. 
A record is kept of the no of voxels which were on the right, left, the absolute difference and whether they were flipped for later use. 

Patient must be stored in base_path. 
Then the tree goes base_path/patientfolder/img_folder/img
'''


base_path = 'C:/Users/poppy/Documents/test_data/'
patients = []
flip_record = 'flip_record.txt'
file = open(flip_record, 'a')
file.write('Patient No_Left_CTV_Voxels No_Right_CTV_Voxels Difference Flip \n')

for patient in patients: 

    base_patient_path = + base_path + 'HN_' + str(patient) + '/'
    path_to_CT = base_patient_path + 'CT_20160129.nii.gz'
    path_to_CTV = base_patient_path + 'BIN_CTV70_CT_20160129.nii.gz'
    path_to_CORD = base_patient_path + 'BIN_CORD_CT_20160129.nii.gz'

    # import imgs which you need
    CT_img, CT_affine, CT_header = get_metadata(path_to_CT)
    CTV_img, _, _ = get_metadata(path_to_CTV)
    CORD_img, _, _ = get_metadata(path_to_CORD)
    del _ 

    # shape of the images 
    x_shape, y_shape, z_shape = np.shape(CT_img)

    # sum the voxel values in each slice
    sum_slices = np.sum(np.sum(CORD_img, axis =0), axis=0)
    # first the first non zero value, this corresponds to the first axial slice in which non zero values are stored
    z_coord = np.where(np.array(sum_slices) != 0)[0][-1]

    # the number of non zero voxels in the indexed slcice
    no_nonzero_in_indexslice = len(np.where(CORD_img[:,:,z_coord]!=0)[0])
    # the middle non zero voxel in the indexed slice
    middle_nonzero_index = int(no_nonzero_in_indexslice/2)
    # coordinated of the middle of the spinal cord 
    x_coord = np.where(CORD_img[:,:,z_coord]!=0)[0][middle_nonzero_index]
    y_coord = np.where(CORD_img[:,:,z_coord]!=0)[1][middle_nonzero_index]

    # find number of voxels in left and right hand side
    # to determine whether you need to flip images 
    CTV_left = np.sum(np.sum(np.sum(CTV_img[0:x_coord,:,:], axis = 2), axis=1))
    CTV_right = np.sum(np.sum(np.sum(CTV_img[x_coord:x_shape,:,:], axis = 2), axis=1))
    Difference_in_Voxels = np.abs(CTV_left - CTV_right)

    # flip so that all patients have majority of CTV of the right hand side 
    if CTV_left > CTV_right:

        file.write(str(patient) + ' ' + str(CTV_left) + ' ' + str(CTV_right) + ' ' + str(Difference_in_Voxels) + ' True \n')

        folders = os.listdir(base_patient_path)

        # searchs for folders in that patient directory 
        for folder in folders:

            imgs = os.list(base_patient_path + '/' + folder)

            # searched for images within the folder
            for img in imgs:

                img_path = base_patient_path + '/' + folder + '/' + img

                # flips imgs and binary objects 
                img_obj, affine, header = get_metadata(path_to_CT)
                
                img_flipped = np.flip(img_obj, axis = 0)
                resampled_img_path = base_patient_path + '/' + folder + '/' + img
                NewNiftiObj = nib.Nifti1Image(img_flipped, affine, header)
                nib.save(NewNiftiObj, resampled_img_path)

    else:
        file.write(str(patient) + ' ' + str(CTV_left) + ' ' + str(CTV_right) + ' ' + str(Difference_in_Voxels) + ' False \n')




