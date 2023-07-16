import numpy as np 
from utils import * 
import pandas as pd 

patients = np.arange(0,10)

base_path = 'T:/Poppy/PatData/test/'
excel_sheet = 'T:/Poppy/PatData/test/Rigid_pCT_preprocessing.csv'
preprocessing_info =  pd.read_csv(excel_sheet, header=0)


for patient in patients:

    CT_img_path = base_path + '/HN_' + str(patient) + '/pCT/pCT.nii.gz'
    y_slice_upper = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]['y_slice_upper'].iloc[0]
    y_slice_lower = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]['y_slice_lower'].iloc[0]
    y_slices = [y_slice_upper, y_slice_lower]
    x_slice_upper = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]['x_slice_upper'].iloc[0]
    x_slice_lower = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]['x_slice_lower'].iloc[0]
    x_slices = [x_slice_upper, x_slice_lower]
    z_cut = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]['z_cut'].iloc[0]
    
    masked_img_path = base_path + '/HN_' + str(patient) + '/pCT/rescaled_MASKED_pCT.nii.gz'
    rescaled_img_path = base_path + '/HN_' + str(patient) + '/pCT/rescaled_pCT.nii.gz'
    
    rescale_CT(CT_img_path, rescaled_img_path)
    
    # masks the image 
    
    mask_img(rescaled_img_path, y_slices, x_slices, z_cut, masked_img_path, masking_value = np.NaN)
    




