import os
import shutil 
from Functions.Patient_Info_Functions import *
import numpy as np 
reg_transform = 'C:/Users/poppy/Documents/Nifty/niftyreg_install/bin/reg_transform.exe'
reg_resample = 'C:/Users/poppy/Documents/Nifty/niftyreg_install/bin/reg_resample.exe'


'''
patients = np.arange(1,21)
no_iterations = 5
for patient in patients:

    CBCTs = get_dates(patient)

    postprocessing_directory = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/'
    if not os.path.exists(postprocessing_directory):
        os.mkdir(postprocessing_directory)

    for CBCT in CBCTs:

        CBCT_original = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/preprocessing/CBCT_' + str(CBCT) + '.nii.gz'
        destination = postprocessing_directory + '/CBCT_' + str(CBCT) + '.nii.gz'
        shutil.copy(CBCT_original, destination)

        for itteration in np.arange(1,no_iterations+2):
            
            affine = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/affine_'+str(itteration)+'/comp_affine_' + str(CBCT) + '.txt'

            # update Sform of image
            img_to_be_updated = destination
            affine = affine
            updated_img = postprocessing_directory + 'CBCT_' + str(CBCT) + '.nii.gz'
            command = reg_transform + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
            os.system(command)


patients = np.append(np.arange(2,10), np.arange(12,21))
no_iterations = 5

for patient in patients:

    CBCTs = get_dates(patient)
    pCT_date = get_pCT_date(patient)

    for CBCT in CBCTs:

        for itteration in np.arange(1,no_iterations+1):
    
            if itteration == 1:
                transformation1 = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/affine_'+str(itteration)+'/comp_affine_'+ str(CBCT) + '.txt'
            else: 
                transformation1 = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/comp_affine'+ str(CBCT) + '.txt'

            transformation2 = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/affine_'+str(itteration+1)+'/comp_affine_'+ str(CBCT) + '.txt'
            composed_transformation = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/comp_affine'+ str(CBCT) + '.txt'
            command = reg_transform + ' -comp ' + transformation2 + ' ' + transformation1 + ' ' + composed_transformation
            os.system(command)

        transformation1 ='D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/comp_affine'+ str(CBCT) + '.txt'
        transformation2 = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_pCT/pCT/affine.txt'

        folder_out = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_pCT/COMPOSED/'
        if not os.path.exists(folder_out):
            os.mkdir(folder_out)

        composed_transformation = folder_out + 'affine'+ str(CBCT) + '.txt'
        command = reg_transform + ' -comp ' + transformation1 + ' ' + transformation2 + ' ' + composed_transformation
        os.system(command)

        # compose all the transformations 
        ## resample with the same reference image 

        CBCT_original = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'//CBCT_GROUPWISE/preprocessing/CBCT_' + str(CBCT) + '.nii.gz'
        destination = folder_out + 'CBCT_' + str(CBCT) + '.nii.gz'
        shutil.copy(CBCT_original, destination)

        ref_img =  'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CT_'+str(pCT_date)+'/CT_'+str(pCT_date)+'.nii.gz'
        float_img = folder_out + 'CBCT_' + str(CBCT) + '.nii.gz'
        transformation = folder_out + 'affine'+ str(CBCT) + '.txt'
        resampled_img = folder_out + 'CBCT_' + str(CBCT) + '.nii.gz'
        command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -omp 12 -pad nan'
        os.system(command)



'''

# patients 1,10,11 somehow I lost their groupwise results
patients = [1,10,11]

for patient in patients:
    
    CBCTs = get_dates(patient)
    pCT_date = get_pCT_date(patient)

    for CBCT in CBCTs:

        folder_out = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_pCT/COMPOSED/'
        if not os.path.exists(folder_out):
            os.mkdir(folder_out)

        original = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_pCT/CBCT/final_affine_CBCT_'+ str(CBCT) + '.txt'
        destination = folder_out + 'affine'+ str(CBCT) + '.txt'
        shutil.copy(original, destination)

        source = 'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CBCT_'+str(CBCT)+'/InitAligned_MASKED_CBCT_'+str(CBCT)+'.nii.gz'
        destination = folder_out  + 'CBCT_' + str(CBCT) + '.nii.gz'
        shutil.copy(source, destination)

        ref_img =  'D:/MODELSPACE_UCLH_HN/HN_'+str(patient)+'/CT_'+str(pCT_date)+'/CT_'+str(pCT_date)+'.nii.gz'
        float_img = folder_out  + 'CBCT_' + str(CBCT) + '.nii.gz'
        transformation = folder_out + 'affine'+ str(CBCT) + '.txt'
        resampled_img = folder_out + 'CBCT_' + str(CBCT) + '.nii.gz'
        command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -omp 12 -pad nan'
        os.system(command)