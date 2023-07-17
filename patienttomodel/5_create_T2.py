import numpy as np 
import os
from utils import *

patients = np.arange(4,10)
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
ref_img = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
base_path = 'T:/Poppy/PatData/test/'
basic_command = reg_transform + ' -ref ' + ref_img + ' -comp ' 
rigid_transformations = ['InitAlignment_affine', 'atlas_rigid', 'atlas_affine']

for patient in patients:
    
    patient_path = base_path + '/HN_' + str(patient) + '/pCT/model_space'
    
    # composition of transformations one after the other 
    
    for transformation in rigid_transformations:
        
        # convert rigid transformation to deformation field so that you can then do the composition 
        
        command = reg_transform + ' -ref ' + ref_img + ' -def ' + patient_path + '/' + transformation + '.txt ' + patient_path  +'/' + transformation + '.nii.gz'
        #print(command)
        os.system(command)
    
    
    command1 = patient_path + '/atlas_rigid.nii.gz ' + patient_path + '/InitAlignment_affine.nii.gz '+ patient_path +'/comp1.nii.gz'
    os.system(basic_command + command1)
    os.remove(patient_path + '/atlas_rigid.nii.gz')
    os.remove(patient_path + '/InitAlignment_affine.nii.gz')
    
    
    command2 = patient_path +'/atlas_affine.nii.gz ' + patient_path +'/comp1.nii.gz ' +  patient_path +'/comp2.nii.gz '
    os.system(basic_command + command2)
    os.remove(patient_path +'/comp1.nii.gz ')
    os.remove(patient_path +'/atlas_affine.nii.gz')
    
    command3 = patient_path +'/cpp_pCT.nii.gz ' + patient_path +'/comp2.nii.gz ' + base_path + '/HN_' + str(patient) + '/T_model.nii.gz '
    os.system(basic_command + command3)
    os.remove(patient_path +'/comp2.nii.gz ')
    
    float_img = base_path + '/HN_' + str(patient) + '/pCT/pCT.nii.gz'
    #convert_to_float(float_img)
    
    transformation = base_path + '/HN_' + str(patient) + '/T_model.nii.gz '
    resampled_img = patient_path + '/pCT.nii.gz'
    #resample_CT(ref_img, float_img, transformation, resampled_img, -1000)

    
    