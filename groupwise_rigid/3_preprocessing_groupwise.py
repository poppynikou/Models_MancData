## this script is used to preprocess images for the groupwise rigid registrations
## the images are cropped in the region in the bottom of the skull and the first two vertibra
# the z slices were defined manually by myself and are saved in excel sheet 'D:/MODELSPACE_UCLH_HN/Rigid_groupwise_preprocessing.xlsx'
# create a matrix to update the Sform and then save it as .txt file 
## then update the sform header 
# and then copy the results into the affine_0 folder ready for the groupwise registrations 
# and rename them in the correct way for the groupwise regs 

import os
import nibabel as nib 
import numpy as np 
import pandas as pd
from shutil import copyfile
import shutil 
import sys
from Patient_Info_Functions import get_time_points

reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
# path to niftireg

# enter patient list 
patients =  np.arange(0,10)
base_path = 'T:/Poppy/PatData'

cut_path = base_path + '/Rigid_groupwise_preprocessing.csv'
preprocessing_info = pd.read_csv(cut_path, header=0)

for patient in patients:
    print(patient)

    # make paths 
    original_Path = base_path + '/HN_' + str(patient) + '/CBCT_GROUPWISE/'
    if not os.path.exists(original_Path):
        os.mkdir(original_Path)
    preprocessing_path = original_Path + 'preprocessing/'
    if not os.path.exists(preprocessing_path):
        os.mkdir(preprocessing_path)
    affine_folder = original_Path + 'affine_0'
    if not os.path.exists(affine_folder):
        os.mkdir(affine_folder)


    CBCTs = get_time_points(base_path, patient)
    

    for index, CBCT_date in enumerate(CBCTs):

    
        source = 'T:/Poppy/PatData/HN_'+str(patient) + '/CBCT_' + str(CBCT_date) +'/CBCT_' + str(CBCT_date) + '.nii.gz'
        destination = preprocessing_path  + 'CBCT_' + str(CBCT_date) + '.nii.gz'
        shutil.copy(source, destination)
        
        # access info from the excel sheet 
        patient_info = preprocessing_info.loc[(preprocessing_info['PATIENT']==int(patient))]# & (preprocessing_info['CBCT_INDEX']==(index+1))]
        lower_slice_cut = patient_info['LOWER'].iloc[0]
        upper_slice_cut = patient_info['UPPER'].iloc[0]

        #define CBCT path 
        CBCT_path =  preprocessing_path  + 'CBCT_' + str(CBCT_date) + '.nii.gz'

        # calculates the z shift to move the cropped image to
        CBCT = nib.load(CBCT_path)
        slice_width = CBCT.header['pixdim'][3]
        z_shift = lower_slice_cut * slice_width

        # creates the transformation matrix to use in updating the Sform 
        identity_matrix = np.identity(4)
        identity_matrix[2][3] = z_shift #[row][column]
        #print(identity_matrix)

        # saves the transformation matrix to use later on with updating the Sform 
        Sform_matrix_path = preprocessing_path + 'Sform_' + str(CBCT_date)  + '.txt'
        identity_matrix = pd.DataFrame(identity_matrix)
        np.savetxt(Sform_matrix_path, identity_matrix, fmt='%d')

        #define where to save the cropped image
        CBCT_CROPPED_path = preprocessing_path  + 'cropped_CBCT_' + str(CBCT_date) + '.nii.gz'

        # crop the image 
        CBCT_image = np.array(CBCT.dataobj)[:,lower_slice_cut:upper_slice_cut,:]

        # save the cropped image 
        clipped_img = nib.Nifti1Image(CBCT_image, CBCT.affine, CBCT.header)
        nib.save(clipped_img, CBCT_CROPPED_path) 

        # define the parameters for updating the Sform of the cropped image 
        img_to_be_updated = CBCT_CROPPED_path
        affine = Sform_matrix_path
        updated_img = preprocessing_path  + 'cropped_Sformupdated_CBCT_' + str(CBCT_date) + '.nii.gz'

        # update the Sform of the cropped image 
        command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
        os.system(command)

        source = updated_img
        destination = affine_folder + '/CBCT_' + str(CBCT_date) + '.nii.gz'
        shutil.copy(source, destination)
