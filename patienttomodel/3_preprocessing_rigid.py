import os 
from utils import *
import numpy as np 
import pandas as pd 

patients = np.arange(0,10)

base_path =  'T:/Poppy/PatData/test/'
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

excel_sheet_cut_path = base_path + '/Rigid_pCT_preprocessing.csv'
preprocessing_info = pd.read_csv(excel_sheet_cut_path, header = 0)

for patient in patients:

    patient_info = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]
    lower_slice_cut = patient_info['rigid_lower'].iloc[0]
    upper_slice_cut = patient_info['rigid_upper'].iloc[0]
    slice_cut = [lower_slice_cut, upper_slice_cut]
    #print(slice_cut)
    patienttomodel_path = base_path + '/HN_' + str(patient) + '/pCT/model_space/'
#
    CT_path = base_path + '/HN_' + str(patient) + '/pCT/rescaled_MASKED_pCT.nii.gz'
    Sform_matrix_path = patienttomodel_path + 'crop_Sform.txt'
    CT_CROPPED_path = patienttomodel_path + 'cropped_pCT.nii.gz'
    updated_img_path = patienttomodel_path + 'pCT_cropped.nii.gz'
    crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = True)
    os.remove(Sform_matrix_path)
    os.remove(CT_CROPPED_path)
    
    # update the cropped img with with the initial alignment
    img_to_be_updated = updated_img_path
    affine = patienttomodel_path + 'InitAlignment_affine.txt'
    updated_img_path = updated_img_path
    # update the Sform of the cropped image 
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img_path
    os.system(command)
    
    # update CT with the initial alignment 
    img_to_be_updated = base_path + '/HN_' + str(patient) + '/pCT/rescaled_MASKED_pCT.nii.gz'
    affine = patienttomodel_path + 'InitAlignment_affine.txt'
    updated_img_path = patienttomodel_path + 'InitAlignment_MASKED_rescaled_pCT.nii.gz'
    # update the Sform of the cropped image 
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img_path
    os.system(command)
    
    