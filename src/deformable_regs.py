import os
import numpy as np 
from utils import *

### CHECK THIS CODE ###

patients = np.arange(1,8)
reg_f3d = 'T:/Poppy/niftireg_executables/reg_f3d.exe'
base_path = 'T:/Poppy/PatData/test/'

# preprocessing
#1. mask out the mouth in the CBCTs
#2. create directories to store the results 
#3. save a file to onedrive to tell you each time a registration is completed 


for patient in patients:
    
    patient_path = base_path + '/UCLHMODELSPACE_REGS/HN_' + str(patient)
    float_img = patient_path + '/pCT/MASKED_pCT.nii.gz'
    
    CBCT_dates = get_time_points(base_path, patient)
    
    for CBCT_date in CBCT_dates:
        
        CBCT_path = patient_path + '/CBCT_' + str(CBCT_date) + '/'
        ref_img = CBCT_path + 'MASKED_CBCT_' + str(CBCT_date) + '.nii.gz'
        resampled_img = CBCT_path + 'DEF_CBCT_' + str(CBCT_date) + '.nii.gz'
        cpp = CBCT_path + 'cpp_CBCT_' + str(CBCT_date) + '.nii.gz'

        command_basic = reg_f3d + ' -ref ' + ref_img + ' -flo ' + float_img + ' -res ' + resampled_img + ' -cpp ' + cpp 
        command_params = ' -sx -10 -sy -10 -sz -10 -be 0 --lncc -5 -ln 5 -vel -omp 12 -le 0.1 -pad nan'
        
        command = command_basic + command_params
        os.system(command)