import os 
from utils import *
import numpy as np 
import pandas as pd 

patients = np.arange(0,10)
excel_sheet_cut_path = ''
preprocessing_info = pd.read_csv(excel_sheet_cut_path, header = 0)
base_path =  'T:/Poppy/PatData/test/'

for patient in patients:

    slice_cut = #

    patient_info = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]# & (preprocessing_info['CBCT_INDEX']==(index+1))]
    lower_slice_cut = patient_info['LOWER'].iloc[0]
    upper_slice_cut = patient_info['UPPER'].iloc[0]
    slice_cut = [lower_slice_cut, upper_slice_cut]

    patienttomodel_path = base_path + '/HN_' + str(patient) + '/pCT/model_space/'


    CT_path = patienttomodel_path +  'InitAlignment_pCT.nii.gz'
    Sform_matrix_path = patienttomodel_path + 'InitAlignment_pCT_Sform.txt'
    CT_CROPPED_path = patienttomodel_path + 'cropped_InitAlignment_pCT.nii.gz'
    updated_img_path = patienttomodel_path + 'InitAlignment_pCT_cropped.nii.gz'
    crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = True)
    os.remove(Sform_matrix_path)
    os.remove(CT_CROPPED_path)