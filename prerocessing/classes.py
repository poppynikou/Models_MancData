import os
import shutil 
import pandas as pd
import nibabel as nib 
import numpy as np 


class MancData():
    
    def __init__(self, structures, base_path):

        self.structures = structures
        self.base_path = base_path

    def read_anonymisation_key(self, anonymisation_key_path):

        self.anonymisation_key = pd.read_csv(anonymisation_key_path, header = 0)
        return self.anonymisation_key


class PatientData(MancData):

    def __init__(self, PatientID):

        self.PatientID = PatientID

    def get_PatientNo(self):

        self.PatientNo = self.anonymisation_key.loc[self.anonymisation_key['Patient_ID'] == int(PatientID[0:9])]['No_Patient_ID'].item()

        return self.PatientNo
    
    def get_CBCT_relative_timepoints(self):

        # -------> check this [3:34] is correct <-------
        self.CBCT_relative_timepoints = self.anonymisation_key.loc[self.anonymisation_key['Patient_ID'] == int(patient[0:9])][3:34].item()

        return self.CBCT_relative_timepoints
    
    def get_patient_folder(self):

        return self.patient_folder_path

    def refactor_pCT(self):

        # rename folders according to easier patient numbers instead
        original_patient_folder_path = str(self.base_path) + '/' + str(self.PatientID) + '/'
        self.patient_folder_path = str(self.base_path) + '/' + str(self.PatientNo) + '/'
        os.rename(original_patient_folder_path, self.patient_folder_path)

        # create pCT folder
        self.pCT_folder_path = str(self.patient_folder_path) + '/pCT/' 
        if not os.path.exists(self.pCT_folder_path):
            os.mkdir(self.pCT_folder_path)

        # move pCT file 
        pCT_file = [file for file in os.listdir(self.patient_folder_path) if file[0:8] == 'pCT.nii']
        original_pCT_path = self.patient_folder_path + pCT_file
        pCT_path = str(self.pCT_folder_path)  + pCT_file

        if os.path.exists(original_pCT_path):
            shutil.move(original_pCT_path, pCT_path)

    def refactor_structures(self):

        # sort out the structures
        structure_files = [file for file in os.listdir(self.patient_folder_path) if file[0:3] =='BIN']
        for structure_file in structure_files:

            original_structure_path = self.patient_folder_path + '/' + structure_file
            structure_path = self.pCT_folder_path + '/' + structure_file

            if os.path.exists(original_structure_path):
                shutil.move(original_structure_path, structure_path)

    def refactor_CBCTs(self):

        # list of CBCTs 
        CBCT_list = [file for file in os.listdir(self.patient_folder_path) if file[0:4] =='CBCT']

        # loop through CBCTs
        for index, CBCT in enumerate(CBCT_list):

            # creates new folder for the new CBCT
            CBCT_folder = self.patient_folder_path + '/CBCT_' + str(self.CBCT_relative_timepoints[index])
            if not os.path.exists(CBCT_folder):
                os.mkdir(CBCT_folder)

            # move the CBCT file 
            original_CBCT_path = self.patient_folder_path + '/' + str(CBCT)
            CBCT_path = CBCT_folder + '/CBCT_' + str(self.CBCT_relative_timepoints[index])

            if os.path.exists(original_CBCT_path):
                shutil.move(original_CBCT_path, CBCT_path)
    
    



class Image(MancData):
    
    def __init__(self, PatientNo):

        self.PatientNo = PatientNo
        return
    
    def get_img_objects(self, img_path):

        img_obj = nib.load(img_path)
        img_data = np.array(img_obj.get_fdata())
        img_affine = img_obj.affine
        img_header = img_obj.header

        return img_data, img_affine, img_header
    
    def zip_nifti(self, img_path):

        # read in data 
        img_data, img_affine, img_header = self.get_img_objects(img_path)

        # define new name
        zipped_img_path = str(img_path) + '.gz'

        # resave as zipped
        NewNiftiObj = nib.Nifti1Image(img_data, img_affine, img_header)
        nib.save(NewNiftiObj, zipped_img_path)

        # remove old .nii obj 
        os.remove(self.img_path)

    
    def flip_img_Bool(self, flip_record):

        path_to_CT = self.base_path + str(self.PatientNo) + '/pCT/pCT.nii.gz'
        path_to_CTV = self.base_path + str(self.PatientNo) + '/pCT/BIN_CTVHIGH.nii.gz'
        path_to_CORD = self.base_path + str(self.PatientNo) + '/pCT/BIN_CORD.nii.gz'

        # import imgs which you need
        CT_img, _, _ = self.get_img_objects(path_to_CT)
        CTV_img, _, _ = self.get_img_objects(path_to_CTV)
        CORD_img, _, _ = self.get_img_objects(path_to_CORD)
        del _ 

        # shape of the images 
        x_shape, _, _ = np.shape(CT_img)
        del _

        # sum the voxel values in each slice
        sum_slices = np.sum(np.sum(CORD_img, axis =0), axis=0)
        # first the first non zero value, this corresponds to the first axial slice in which non zero values are stored
        z_coord = np.where(np.array(sum_slices) != 0)[0][-1]

        # the number of non zero voxels in the indexed slcice
        no_nonzero_in_indexslice = len(np.where(CORD_img[:,:,z_coord]!=0)[0])
        # the middle non zero voxel in the indexed slice
        middle_nonzero_index = int(no_nonzero_in_indexslice/2)
        # coordinated of the middle of the spinal cord 
        x_coord = np.where(CORD_img[:,:,z_coord]!=0)[0][middle_nonzero_index]
        #y_coord = np.where(CORD_img[:,:,z_coord]!=0)[1][middle_nonzero_index]

        # find number of voxels in left and right hand side
        # to determine whether you need to flip images 
        CTV_left = int(np.sum(np.sum(np.sum(CTV_img[0:x_coord,:,:], axis = 2), axis=1)))
        CTV_right = int(np.sum(np.sum(np.sum(CTV_img[x_coord:x_shape,:,:], axis = 2), axis=1)))
        Difference_in_Voxels = np.abs(CTV_left - CTV_right)

        # flip so that all patients have majority of CTV of the right hand side 
        if CTV_left > CTV_right:
            flip_record.write(str(self.PatientNo) + ' ' + str(CTV_left) + ' ' + str(CTV_right) + ' ' + str(Difference_in_Voxels) + ' True \n')
            return True
        
        else:
            flip_record.write(str(self.PatientNo) + ' ' + str(CTV_left) + ' ' + str(CTV_right) + ' ' + str(Difference_in_Voxels) + ' False \n')
            return False
    
    def flip_img(self, img_path, new_img_path = False):

            img_data, img_affine, img_header = self.get_img_objects(img_path)
                
            img_flipped = np.flip(img_data, axis = 0)
            NewNiftiObj = nib.Nifti1Image(img_flipped, img_affine, img_header)
            if new_img_path:
                nib.save(NewNiftiObj, new_img_path)#
            else:
                nib.save(NewNiftiObj, img_path)#
         

    def convert_to_float(self, img_path, new_img_path = False):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = np.array(img_data, dtype = np.float32)

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
        NewNiftiObj.set_data_dtype('float32')
        if new_img_path:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#


    def rescale_HU(self, img_path, new_img_path = False):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = img_data.copy()
        img_data_copy = img_data_copy+ 1024

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
       
        if new_img_path:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#

    
    def mask_CT(self, img_path, new_img_path = False):
        
        return 
    
    def mask_CBCT(self, img_path, new_img_path = False):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = img_data.copy()
        # index at top corner 
        masking_HU = img_data_copy[0,0,0]
        img_data_copy[img_data_copy == masking_HU] = np.NaN

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
       
        if new_img_path:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#


