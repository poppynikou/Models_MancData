import os 

reg_f3d = 'T:/Poppy/niftireg_executables/reg_f3d.exe'


ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
float_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/AFFINE_pCT.nii.gz'
cpp_grid = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/cpp_grid.nii.gz'
resulting_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/DEF_pCT.nii.gz'

basic_command = reg_f3d + ' -ref ' + ref_img + ' -flo ' + float_img + ' -cpp ' + cpp_grid + ' -res ' + resulting_img 
reg_params = ' -be 0 --lncc -5 -ln 5 -vel -omp 12 -le 0.1 -sx -5 -sy -5 -sz -5'

command = basic_command + reg_params
os.system(command)