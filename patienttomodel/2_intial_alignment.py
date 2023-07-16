import numpy as np 
import os 


reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
base_path = 'T:/Poppy/PatData/test/'
patients = np.arange(0,10)
hn_atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'

for patient in patients: 

    patienttomodel_path = base_path + '/HN_' + str(patient) + '/pCT/model_space/'
    if not os.path.exists(patienttomodel_path):
        os.mkdir(patienttomodel_path)

    ref_img = hn_atlas_path
    float_img = base_path + '/HN_' + str(patient) + '/pCT/pCT.nii.gz'
    affine = patienttomodel_path + 'InitAlignment_affine.txt'
    resampled_img = patienttomodel_path + 'resampled_InitAlignment_pCT.nii.gz'
    command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + affine + ' -res ' + resampled_img + ' -rigOnly -omp 12'
    os.system(command)

    os.remove(resampled_img)

    img_to_be_updated = base_path + '/HN_' + str(patient) + '/pCT/pCT.nii.gz'
    updated_img = patienttomodel_path + 'InitAlignment_pCT.nii.gz'
    # update the Sform of the cropped image 
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
    os.system(command)