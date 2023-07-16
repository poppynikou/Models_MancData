import numpy as np 
import os

patients = np.arange(0,10)
reg_f3d = 'T:/Poppy/niftireg_executables/reg_f3d.exe'
ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
base_path = 'T:/Poppy/PatData/test/'

for patient in patients:

    patienttomodel_path = base_path + '/HN_' + str(patient) + '/pCT/model_space/'

    float_img = patienttomodel_path + 'AFFINE_pCT.nii.gz'
    cpp = patienttomodel_path + 'cpp_pCT.nii.gz'
    resampled_img = patienttomodel_path + 'DEFORMABLE_pCT.nii.gz'

    command_basic = reg_f3d + ' -ref ' + ref_img + ' -flo ' + float_img + ' -res ' + resampled_img + ' -cpp ' + cpp 
    command_params = ' -sx -10 -sy -10 -sz -10 -be 0 --lncc -5 -ln 5 -vel -omp 12 -le 0.1'
    
    command = command_basic + command_params
    
    os.system(command)