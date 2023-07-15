# align the pCT to the CBCT series
# first we have to crop the pCT into the region of the CBCT series to align them 
import pandas as pd
import os
import shutil 
from Patient_Info_Functions import *
import numpy as np 

reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'

patients = np.arange(0,10)
base_path = 'T:/Poppy/PatData/'
cut_path = 'T:/Poppy/PatData/Rigid_pCT_preprocessing.csv'
preprocessing_info = pd.read_csv(cut_path, header=0)

for patient in patients:

    CBCTs_dates = get_time_points(base_path, patient)

    results_path = base_path + '/HN_'+str(patient)+'/CBCT_pCT/'
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    pCT_results_path = base_path + '/HN_'+str(patient)+'/CBCT_pCT/pCT/'
    if not os.path.exists(pCT_results_path):
        os.mkdir(pCT_results_path)
    CBCT_results_path = base_path + '/HN_'+str(patient)+'/CBCT_pCT/CBCT/'
    if not os.path.exists(CBCT_results_path):
        os.mkdir(CBCT_results_path)

    CT_path = base_path + '/HN_'+str(patient)+'/pCT/MASKED_rescaled_pCT.nii.gz'

    # access info from the excel sheet 
    patient_info = preprocessing_info.loc[preprocessing_info['PATIENT']==int(patient)]

    lower_slice_cut = patient_info['LOWER'].iloc[0]
    upper_slice_cut = patient_info['UPPER'].iloc[0]

    # calculates the z shift to move the cropped image to
    CT = nib.load(CT_path)
    slice_width = CT.header['pixdim'][3]
    z_shift = lower_slice_cut * slice_width

    # creates the transformation matrix to use in updating the Sform 
    identity_matrix = np.identity(4)
    identity_matrix[2][3] = z_shift #[row][column]
    #print(identity_matrix)

    # saves the transformation matrix to use later on with updating the Sform 
    Sform_matrix_path = pCT_results_path + 'cropped_CT_Sform_update.txt'
    identity_matrix = pd.DataFrame(identity_matrix)
    np.savetxt(Sform_matrix_path, identity_matrix, fmt='%d')

    #define where to save the cropped image
    CT_CROPPED_path = pCT_results_path  + 'cropped_CT.nii.gz'

    # crop the image 
    CT_image = np.array(CT.dataobj)[:,:,lower_slice_cut:upper_slice_cut]

    # save the cropped image 
    clipped_img = nib.Nifti1Image(CT_image, CT.affine, CT.header)
    nib.save(clipped_img, CT_CROPPED_path) 

    # define the parameters for updating the Sform of the cropped image 
    img_to_be_updated = CT_CROPPED_path
    affine = Sform_matrix_path
    updated_img = pCT_results_path  + 'cropped_Sformupdated_CT.nii.gz'

    # update the Sform of the cropped image 
    command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
    os.system(command)

    # rigidly align the cropped pCT to the first cropped CBCT in the series
    ref_img = pCT_results_path  + 'cropped_Sformupdated_CT.nii.gz'
    float_img = base_path + '/HN_'+str(patient)+'/CBCT_GROUPWISE/affine_2/CBCT_' + str(CBCTs_dates[0]) + '.nii.gz'
    transformation = pCT_results_path + 'affine.txt'
    resampled_img = pCT_results_path + 'CBCT_' + str(CBCTs_dates[0]) + '.nii.gz'
    # rigid alignment of the cropped pCT to the first CBCT in the series
    command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img + ' -rigOnly -omp 12' 
    os.system(command)

    os.remove(resampled_img)

    # update each CBCT with the affine to align to the pCT
    for CBCT in CBCTs_dates:

        CBCT_to_update = base_path + '/HN_'+str(patient)+'/CBCT_GROUPWISE/postprocessing/CBCT_' + str(CBCT) + '.nii.gz'
        affine = pCT_results_path + 'affine.txt'
        updated_img = CBCT_results_path + '/CBCT_'+ str(CBCT) + '.nii.gz'

        # update the Sform of the cropped image 
        command = reg_transform + ' -ref ' + CBCT_to_update + ' -updSform ' + CBCT_to_update + ' ' + affine + ' ' + updated_img
        os.system(command)

