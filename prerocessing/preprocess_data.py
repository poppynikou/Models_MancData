import os
from classes import *

structures = []
base_path = ''
niftireg_path = ''

# path to the file which contains all patient info
patients_csv_path = 'T:/Poppy/Anonymisation_Key.csv'

flip_record = base_path + 'flip_record.txt'
flip_record = open(flip_record, 'a')
flip_record.write('Patient No_Left_CTV_Voxels No_Right_CTV_Voxels Difference Flip \n')

# create instance of data class 
Data = MancData(structures, base_path)
Data.define_niftireg_path(niftireg_path)
Data.read_anonymisation_key(patients_csv_path)

patients = os.listdir(base_path)

for patient in patients:

    # check if the preprocessing for that patient has already been done

    PatientID = patient
    PatientObj = PatientData(PatientID)
    PatientNo = PatientObj.get_PatientNo()

    # refactor the data into organised folders 
    PatientObj.refactor_pCT()
    PatientObj.refactor_structures()
    PatientObj.refactor_CBCTs()

    # create image class 
    ImgObj = Image(PatientNo)

    # find patient folder to search through
    patient_path = PatientObj.get_patient_folder()

    # find all files within a directory which are nifti files
    for path, subdirs, files in os.walk(patient_path):
        for name in files:
            file_path = os.path.join(path, name) 
            if name[-4:] == '.nii':
                # zip all nifty data 
                ImgObj.zip_nifti(file_path)


    flip_img_Bool = ImgObj.flip_img_Bool(flip_record)

    # preprocess the images 
    for path, subdirs, files in os.walk(patient_path):
        for name in files:

            file_path = os.path.join(path, name) 

            if flip_img_Bool:
                ImgObj.flip_img(file_path)
                ImgObj.rename_parotid(file_path, flip = True)
            else:
                ImgObj.rename_parotid(file_path, flip = False)
        
            if name[0:3] == 'pCT':
                ImgObj.convert_to_float(file_path)
                ImgObj.rescale_HU(file_path)
                ImgObj.clip_HU(file_path)
                atlas_img_path = ''
                masked_img_path = ''
                ImgObj.mask_CT(file_path, atlas_img_path, masked_img_path)
                cropped_img_path = ''
                ImgObj.crop_Img(file_path, cropped_img_path, ImgType = 'CT')

            elif name[0:4] == 'CBCT':
                ImgObj.convert_to_float(file_path)
                masked_img_path = '' 
                ImgObj.mask_CBCT(file_path, masked_img_path)
                cropped_img_path = ''
                ImgObj.crop_Img(file_path, cropped_img_path, ImgType = 'CBCT')




    

                



