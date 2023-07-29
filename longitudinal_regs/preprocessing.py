import os
import numpy as np 
from utils import *

patients = np.arange(10,16)# insert specific patients you want to work with 
#np.arange(0,10)
reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'
ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
base_path = 'T:/Poppy/PatData/test2/'

for patient in patients:
    
    patient_path = base_path + '/HN_' + str(patient)
    modelspace_patient_path = base_path + '/UCLHMODELSPACE_REGS/HN_'+str(patient)
    if not os.path.exists(modelspace_patient_path):
        os.mkdir(modelspace_patient_path)
    modelspace_patientpCT_path = modelspace_patient_path + '/pCT'
    if not os.path.exists(modelspace_patientpCT_path):
        os.mkdir(modelspace_patientpCT_path)
        
    transformation = patient_path +'/T_model.nii.gz'
    
    # make sure image is a float 
    float_img = patient_path + '/pCT/rescaled_bedMASKED_pCT.nii.gz'
    resampled_img = modelspace_patientpCT_path + '/MASKED_pCT.nii.gz'
    # do this 
    resample_CT(ref_img, float_img, transformation, resampled_img, np.NaN)
    
    
    CBCT_dates = get_time_points(base_path, patient)
    for CBCT_date in CBCT_dates:
        
        modelspace_patientCBCT_path = modelspace_patient_path + '/CBCT_' + str(CBCT_date)
        if not os.path.exists(modelspace_patientCBCT_path):
            os.mkdir(modelspace_patientCBCT_path)
        
        patientspace_CBCT_path = patient_path + '/CBCT_'  + str(CBCT_date)
        
        CBCT_path = patientspace_CBCT_path+'/CBCT_'+str(CBCT_date)+'.nii.gz'
        convert_to_float(CBCT_path)
        
        # and clip intensities
        float_img = patientspace_CBCT_path+'/MASKED_CBCT_'+str(CBCT_date)+'.nii.gz'
        mask_elekta_CBCT(CBCT_path, float_img)
        
        float_img = patientspace_CBCT_path + '/MASKED_CBCT_'+str(CBCT_date)+'.nii.gz'
        resampled_img = modelspace_patientCBCT_path + '/MASKED_CBCT_'+str(CBCT_date)+'.nii.gz'
        # do this 
        resample_CT(ref_img, float_img, transformation, resampled_img, np.NaN)