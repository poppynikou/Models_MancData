import os
import numpy as np 
from utils import *

patients = np.arange(0,10)
reg_f3d = 'T:/Poppy/niftireg_executables/reg_f3d.exe'
base_path = 'T:/Poppy/PatData/test/'

for patient in patients:
    
    patient_path = base_path + '/HN_' + str(patient) + '/MODELSPACE_REGS/'
    
    CBCT_dates = get_time_points(base_path, patient)
    
    for CBCT_date in CBCT_dates:
        
        float_img = patient_path + '/pCT.nii.gz'
        
        CBCT_path = patient_path + '/CBCT_' + str(CBCT_date) + '/'
        ref_img = CBCT_path + 'CBCT_' + str(CBCT_date) + '.nii.gz'
        resampled_img = CBCT_path + 'DEF_CBCT_' + str(CBCT_date) + '.nii.gz'
        cpp = CBCT_path + 'cpp_CBCT_' + str(CBCT_date) + '.nii.gz'

        command_basic = reg_f3d + ' -ref ' + ref_img + ' -flo ' + float_img + ' -res ' + resampled_img + ' -cpp ' + cpp 
        command_params = ' -sx -10 -sy -10 -sz -10 -be 0 --lncc -5 -ln 5 -vel -omp 12 -le 0.1'
        
        command = command_basic + command_params
        os.system(command)