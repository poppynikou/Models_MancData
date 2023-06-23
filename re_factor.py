import os 
import nibabel 
import pandas as pd
import shutil 

'''
Script to preprocess the data from CBCT Packs 
You need excell sheet which contains patient ID, anonymised patient ID and then the relative dates of the CBCTs of that patient
It renames and re-files in terms of pCT, and relative CBCT dates.

'''


output_csv_path = 'T:/Poppy/Anonymisation_Key.csv'
anonymisation_key = pd.read_csv(output_csv_path, header = 0)
print(anonymisation_key.head)

exported_data_path = 'T:/Poppy/PatData/'
patients = os.listdir(exported_data_path)

for index, patient in enumerate(patients):

    if patient[0:3] != 'HN_':

        # rename folders according to easier patient numbers instead
        original_patient_path = exported_data_path + patient
        new_patient_path = exported_data_path + str(anonymisation_key.loc[anonymisation_key['Patient_ID'] == int(patient[0:9])]['No_Patient_ID'].item())
        os.rename(original_patient_path, new_patient_path)

        # create folders within the patient for the imaging data
        img_list = os.listdir(new_patient_path)

        # sort out the pCT data 
        pCT_folder_path = new_patient_path + '/pCT'
        if not os.path.exists(pCT_folder_path):
            os.mkdir(pCT_folder_path)
        original_pCT_img_path = new_patient_path + '/pCT.nii'
        new_pCT_img_path = pCT_folder_path + '/pCT.nii'
        shutil.move(original_pCT_img_path, new_pCT_img_path)

        # list of CBCTs 
        CBCT_list = os.listdir(new_patient_path)

        for index, CBCT in enumerate(CBCT_list):

            if CBCT != 'pCT':
                
                # identifies CBCT which you want to move
                CBCT_column_name = 'CBCT' + str(index+1)
                CBCT_rel_time_point = anonymisation_key.loc[anonymisation_key['Patient_ID'] == int(patient[0:9])][CBCT_column_name].item()
                original_patient_path = new_patient_path + '/CBCT' + str(index) + '.nii'

                # creates new folder for the new CBCT
                new_patient_folder = new_patient_path + '/CBCT_' + str(CBCT_rel_time_point)
                if not os.path.exists(new_patient_folder):
                    os.mkdir(new_patient_folder)

                # moves CBCT into folder 
                if len(os.listdir(new_patient_folder)) != 0:
                    name_index = int(len(os.listdir(new_patient_folder)))+1
                    new_CBCT_patient_path = new_patient_folder + '/CBCT_' + str(CBCT_rel_time_point) + '_'+str(name_index)+'.nii'
                else:
                    new_CBCT_patient_path = new_patient_folder + '/CBCT_' + str(CBCT_rel_time_point) + '.nii'

                shutil.move(original_patient_path, new_CBCT_patient_path)


           
           



            

            