
# resample 
#LOO cps7 HN23 and HN62 again just incase something went wrong 

import os 

ref_img = 'D:/pCT_Atlas/GroupWise/Itteration_7/average_pCT.nii.gz'
cpp_path = 'D:/CHRISTIE_HN/LOO/PSM_CPS_7/HN_62/cpp_28.nii.gz'
float_path = 'D:/CHRISTIE_HN/Masks/HN_62/atlas/'
resampled_path = 'D:/CHRISTIE_HN/LOO/PSM_CPS_7/HN_62/test/'
structures = os.listdir(float_path)

reg_resample = 'C:/Users/poppy/Documents/Nifty/niftyreg_install/bin/reg_resample.exe '

for structure in structures: 

    float_img = float_path + str(structure) 
    resampled_img = resampled_path + str(structure) 
    command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -cpp ' + cpp_path + ' -res ' + resampled_img  + ' -inter 1 -pad 0'   

    os.system(command)