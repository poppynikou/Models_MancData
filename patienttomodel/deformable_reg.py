import numpy as np 
import os

patients = np.arange(0,10)

ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'

for patient in patients:

    float_img = 'T:/Poppy/PatData/HN_'+str(patient)+'/pCT/UCLHAtlas_Alignment/AFFINE_pCT.nii.gz'
    cpp = 'T:/Poppy/PatData/HN_'+str(patient)+'/pCT/UCLHAtlas_Alignment/cpp_pCT.nii.gz'
    resampled_img = 'T:/Poppy/PatData/HN_'+str(patient)+'/pCT/UCLHAtlas_Alignment/DEFORMABLE_pCT.nii.gz'


    command_basic = reg_f3d + ' -ref ' + ref_img + ' -flo ' + float_img + ' -res ' + resampled_img + ' -cpp ' + cpp 
    command_params = ' -sx -10 -sy -10 -sz -10 -be 0 --lncc -5 -ln 5 -vel -omp 12 -le 0.1'
    
    command = command_basic + command_params
    
    os.system(command)