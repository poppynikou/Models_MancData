import numpy as np 
import os


'''
note to future self: this may throw errors as it wont like composition of .txt with .txt
or .txt with .nii.gz 


'''


patients = np.arange(0,10)
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
base_path = 'T:/Poppy/PatData/test/'
basic_command = reg_transform + ' -ref ' + ref_img + ' -comp ' 

for patient in patients:
    
    patient_path = base_path + '/HN_' + str(patient) + '/pCT/model_space'
    
    transformations = ['InitAlignment_affine', 'atlas_rigid', 'atlas_affine', 'cpp_pCT.nii.gz']
    
    
    # composition of transformations one after the other 
    
    command1 = patient_path + 'atlas_rigid.txt ' + patient + 'InitAlignment_affine.txt '+ patient_path +'comp1.nii.gz'
    os.system(command1)
    
    
    command2 = patient_path +'atlas_affine.txt ' + patient_path +'comp1.nii.gz ' +  patient_path +'comp2.nii.gz '
    os.remove(patient_path +'comp1.nii.gz ')
    os.system(command2)
    
    command3 = patient_path +'cpp_pCT.nii.gz ' + patient_path +'comp2.nii.gz ' + patient_path +'T2.nii.gz '
    os.remove(patient_path +'comp2.nii.gz ')
    os.system(command3)
    
    
    
        
        
    