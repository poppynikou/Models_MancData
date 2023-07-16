# first align a patient rigidly 
import numpy as np 
import os
'''
I decided that you don't need to crop the images for the rigid and affine alignment
You just need a good mask, to make sure that only the anatomy shown in the atlas is shown in the patient CT
The initial alignment code just puts them into the same space 
'''

hn_atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
base_path = 'T:/Poppy/PatData/test/'

patients = np.arange(0,10)

for patient in patients:

    patienttomodel_path = base_path + '/HN_' + str(patient) + '/pCT/model_space/'

    pCT_hn_path = patienttomodel_path + 'InitAlignment_MASKED_rescaled_pCT.nii.gz'

    ref_img = hn_atlas_path
    #float_img =  patienttomodel_path + 'pCT_cropped.nii.gz'
    float_img = pCT_hn_path
    transformation = patienttomodel_path + '/atlas_rigid.txt'
    resampled_img1 = patienttomodel_path + '/resampled_pCT_atlas_rigid.nii.gz'
    command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img1 + ' -rigOnly -omp 12' 
    os.system(command)

    # delete resampled img, and update the Sform 
    os.remove(resampled_img1)
    
    # update the Sform of the non-cropped image 
    img_to_be_updated = pCT_hn_path 
    affine = transformation
    updated_img = patienttomodel_path + '/RIGID_pCT.nii.gz'
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
    os.system(command)


    ref_img = hn_atlas_path
    float_img = updated_img
    transformation = patienttomodel_path + '/atlas_affine.txt'
    resampled_img2 = patienttomodel_path + '/resampled_pCT_atlas_affine.nii.gz'
    command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img2 +  ' -omp 12' 
    os.system(command)

    # delete resampled img, and update the Sform 
    os.remove(resampled_img2)

    # update the Sform of the non-cropped image 
    img_to_be_updated = updated_img
    affine = transformation
    updated_img = patienttomodel_path + '/AFFINE_pCT.nii.gz'
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
    os.system(command)
    # first align a patient rigidly 



 