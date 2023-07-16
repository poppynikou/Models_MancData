import numpy as np 
from utils import * 
import pandas as pd 

patients = np.arange(0,10)

base_path = 'T:/Poppy/PatData/test/'
excel_sheet = 
y_cut_data =  pd.read_csv(excel_sheet, header=0)


for patient in patients:

    CT_img_path = base_path + '/HN_' + str(patient) + '/pCT/pCT.nii.gz'
    y_slice = 
    masked_img_path = base_path + '/HN_' + str(patient) + '/pCT/MASKED_pCT.nii.gz'

    # masks the image 
    mask_img(CT_img_path, y_slice, masked_img_path, masking_value = np.NaN)
