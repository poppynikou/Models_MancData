import numpy as np 
import pandas as pd
import os
import shutil 
import nibabel as nib 

def get_PatientNo(PatientID):
        
    anonymisation_key = pd.read_csv('T:/Poppy/Anonymisation_Key.csv', header = 0)
    PatientNo = anonymisation_key.loc[anonymisation_key['Patient_ID'] == int(PatientID[0:9])]['No_Patient_ID'].item()
    return PatientNo
    
def get_img_objects( img_path):
        
        img_obj = nib.load(img_path)
        img_data = np.array(img_obj.get_fdata())
        img_affine = img_obj.affine
        img_header = img_obj.header

        return img_data, img_affine, img_header

base_path = 'T:/Poppy/PatData/batch2'

patients = os.listdir(base_path)

for patient in patients:
    
    
    new_path = base_path + '/' + str(patient) + '/pCT/BIN_MOUTH.nii'
    if os.path.exists(new_path):
        
        
        zipped_path = base_path + '/' + str(patient) + '/pCT/BIN_MOUTH.nii.gz'
        img_data, img_affine, img_header = get_img_objects(new_path)

        NewNiftiObj  = nib.Nifti1Image(img_data, img_affine, img_header)
        nib.save(NewNiftiObj, zipped_path)
        
        os.remove(new_path)
        
        