
import os
import numpy as np 
from utils import *

patients = np.arange(0,10)
reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'
ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
base_path = 'T:/Poppy/PatData/test/'

for patient in patients:
    
    patient_path = base_path + '/HN_' + str(patient)
    
    CBCT_dates = get_time_points(base_path, patient)
    
    transformation = patient_path +'/model_space/T2.nii.gz'

    float_img = base_path + '/HN_' + str(patient) + '/pCT/modelspace_rescaled_bedMASKED_pCT.nii.gz'
    resampled_img = base_path + '/HN_' + str(patient) + '/MODELSPACE_REGS/pCT.nii.gz'
    # do this 
    
    for CBCT_date in CBCT_dates:
        
        float_img = base_path + '/HN_' + str(patient) + '/CBCT_'+str(CBCT_date)+'MASKED_CBCT'+str(CBCT_date)+'.nii.gz'
        resampled_img = base_path + '/HN_' + str(patient) + '/MODELSPACE_REGS/CBCT_'+str(CBCT_date)+'MASKED_CBCT'+str(CBCT_date)+'.nii.gz

        # do this 