import os
import shutil 
import pandas as pd
import nibabel as nib 
import numpy as np 
from src.utils.functions import *

class MancData():
    
    def __init__(self, base_path, niftireg_path, atlas_path):

        self.base_path = base_path
        self.reg_transform = niftireg_path +'/reg_transform.exe'
        self.reg_average = niftireg_path +'/reg_average.exe'
        self.reg_aladin = niftireg_path +'/reg_aladin.exe'
        self.reg_resample = niftireg_path +'/reg_resample.exe'
        self.reg_f3d = niftireg_path +'/reg_f3d.exe'
        self.atlas_path = atlas_path

    def create_log_file(self, patient):

        self.path_to_log_file = self.base_path + '/log.txt'
        file = open(self.path_to_log_file,"w+")
    
    def write_to_logfile(self, text):
        file = open(self.path_to_log_file,"w+")
        file.write(str(text) + '\n')

    def read_anonymisation_key(self, anonymisation_key_path):

        anonymisation_key = pd.read_csv(anonymisation_key_path, header = 0)
        return anonymisation_key
    

    def get_img_objects(self, img_path):
    
        img_obj = nib.load(img_path)
        img_data = np.array(img_obj.get_fdata())
        img_affine = img_obj.affine
        img_header = img_obj.header

        return img_data, img_affine, img_header

class PatientData(MancData):

    def __init__(self, PatientID, base_path, niftireg_path):
        self.PatientID = PatientID
        MancData.__init__(self, base_path, niftireg_path, '')


    def get_PatientNo(self, anonymisation_key_path):
        
        self.anonymisation_key = self.read_anonymisation_key(anonymisation_key_path)
        self.PatientNo = self.anonymisation_key.loc[self.anonymisation_key['Patient_ID'] == int(self.PatientID[0:9])]['No_Patient_ID'].item()
        return self.PatientNo
    
    def get_CBCT_relative_timepoints(self):

        CBCT_relative_timepoints = self.anonymisation_key.loc[self.anonymisation_key['Patient_ID'] == int(self.PatientID[0:9])].iloc[:,4:35].values.tolist()
        self.CBCT_relative_timepoints = CBCT_relative_timepoints[0]
        self.CBCT_relative_timepoints = [int(x) for x in self.CBCT_relative_timepoints if ~np.isnan(x)]
        return self.CBCT_relative_timepoints

    def get_patient_folder(self):
        self.patient_folder_path = str(self.base_path) + '/' + str(self.PatientNo) + '/'
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
        pCT_file = [file for file in os.listdir(self.patient_folder_path) if file[0:8] == 'pCT.nii'][0]
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
            CBCT_path = CBCT_folder + '/CBCT_' + str(self.CBCT_relative_timepoints[index]) + '.nii'

            if os.path.exists(original_CBCT_path):
                shutil.move(original_CBCT_path, CBCT_path)
    
    

class Image(MancData):
    
    def __init__(self, PatientNo, base_path, niftireg_path):

        self.PatientNo = PatientNo
        MancData.__init__(self, base_path, niftireg_path, '')
        return
    
    def read_meta_info(self, csv_file):

        meta_info =  pd.read_csv(csv_file, header=0)
        self.patient_masking_info = meta_info.loc[(meta_info['PatientNo']==self.PatientNo)]
    
    
    def zip_nifti(self, img_path):

        # read in data 
        img_data, img_affine, img_header = self.get_img_objects(img_path)

        # set new name
        zipped_img_path = str(img_path) + '.gz'

        # resave as zipped
        NewNiftiObj = nib.Nifti1Image(img_data, img_affine, img_header)
        nib.save(NewNiftiObj, zipped_img_path)

        # remove old .nii obj 
        os.remove(img_path)

    
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
        
    def rename_parotid(self, name, flip = False):
        new_name = name
        file_path = self.base_path + '/' + self.PatientNo + '/pCT/'
        if name.__contains__('PAROTIDL'):
            if flip:
                new_name=new_name.replace('PAROTIDL','RPAROTID')
            else:
                new_name=new_name.replace('PAROTIDL','LPAROTID')
            source = file_path + name
            destination = file_path + new_name
            os.rename(source, destination)   
        elif name.__contains__('PAROTIDR'):
            if flip:
                new_name=new_name.replace('PAROTIDR','LPAROTID')
            else:
                new_name=new_name.replace('PAROTIDR','RPAROTID')
            source = file_path + name
            destination = file_path + new_name
            os.rename(source, destination)
        elif name.__contains__('PAROTIDIPSI'):
            if flip:
                new_name=new_name.replace('PAROTIDIPSI','CONTRAPAROTID')
            else:
                new_name=new_name.replace('PAROTIDIPSI','IPSIPAROTID')
            source = file_path + name
            destination = file_path + new_name
            os.rename(source, destination)
        elif name.__contains__('PAROTIDCONTRA'):
            if flip:
                new_name=new_name.replace('PAROTIDCONTRA','IPSIPAROTID')
            else:
                new_name=new_name.replace('PAROTIDCONTRA','CONTRAPAROTID')
            source = file_path + name
            destination = file_path + new_name
            os.rename(source, destination)
    
    def flip_img(self, img_path, new_img_path = False):

            img_data, img_affine, img_header = self.get_img_objects(img_path)
                
            img_flipped = np.flip(img_data, axis = 0)
            NewNiftiObj = nib.Nifti1Image(img_flipped, img_affine, img_header)
            if new_img_path != False:
                nib.save(NewNiftiObj, new_img_path)#
            else:
                nib.save(NewNiftiObj, img_path)
            


    def convert_to_float(self, img_path, new_img_path = False):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = np.array(img_data, dtype = np.float32)

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
        NewNiftiObj.set_data_dtype('float32')
        if new_img_path != False:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#


    def rescale_HU(self, img_path, new_img_path = False):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = img_data.copy()
        img_data_copy = img_data_copy - 1024

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
       
        if new_img_path != False:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#

    def clip_HU(self, img_path, new_img_path = False):
    
        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = img_data.copy()
        img_data_copy[img_data_copy>1500] = 1500

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
       
        if new_img_path != False:
            nib.save(NewNiftiObj, new_img_path)#
        else:
            nib.save(NewNiftiObj, img_path)#

    def return_masking_info(self):
        
        y_slice_upper = self.patient_masking_info['CT_M_Y_+'].iloc[0]
        y_slice_lower = self.patient_masking_info['CT_M_Y_-'].iloc[0]
        y_slices = [int(y_slice_upper), int(y_slice_lower)]
        x_slice_upper = self.patient_masking_info['CT_M_X_+'].iloc[0]
        x_slice_lower = self.patient_masking_info['CT_M_X_-'].iloc[0]
        x_slices = [int(x_slice_upper), int(x_slice_lower)]
        z_slice = int(self.patient_masking_info['CT_M_Z'].iloc[0])
        
        return x_slices, y_slices, z_slice
       

    def mask_CT(self, img_path, new_atlas_img_path, new_masked_img_path):
        
        x_slices, y_slices, z_slice = self.return_masking_info()

        img_data, img_affine, img_header = self.get_img_objects(img_path)

        img_data_copy = np.array(img_data.copy())
        (x,y,z) = np.shape(img_data_copy)

        img_data_copy[:,y_slices[0]:y,:] = np.NaN
        img_data_copy[:,0:y_slices[1],:] = np.NaN

        newNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
        nib.save(newNiftiObj, new_masked_img_path)

        # mask out the mouth region 
        if os.path.exists(self.base_path + '/' + str(self.PatientNo) + '/pCT/BIN_CTVHIGH.nii.gz'):
            img_data_ctvhigh, _, _ = self.get_img_objects(self.base_path + '/' + str(self.PatientNo) + '/pCT/BIN_CTVHIGH.nii.gz')
            del _
            img_data_ctvhigh= np.array(img_data_ctvhigh, dtype = np.bool8)
            img_data_copy[img_data_ctvhigh] = np.NaN
        else:
            print('Patient ' + str(self.PatientNo) + ' no high dose CTV Mask')
            
        img_data_copy[x_slices[0]:x,:,:] = np.NaN
        img_data_copy[0:x_slices[1],:,:] = np.NaN
        img_data_copy[:,:,z_slice:z] = np.NaN
        newNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
        nib.save(newNiftiObj, new_atlas_img_path)


    def mask_CBCT(self, img_path, new_img_path):

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        img_data_copy = img_data.copy()
        # index at top corner 
        masking_HU = img_data_copy[0,0,0]
        img_data_copy[img_data_copy == masking_HU] = np.NaN

        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
       
        nib.save(NewNiftiObj, new_img_path)
        

    def return_cropping_info(self, ImgType):

        if ImgType == 'CT':
            z_slice_upper = self.patient_masking_info['CT_C_+'].iloc[0]
            z_slice_lower = self.patient_masking_info['CT_C_-'].iloc[0]
        elif ImgType == 'CBCT':
            z_slice_upper = self.patient_masking_info['CBCT_C_+'].iloc[0]
            z_slice_lower = self.patient_masking_info['CBCT_C_-'].iloc[0]

        return int(z_slice_upper), int(z_slice_lower)

    def calc_Sform_matrix(self, img_path, affine_matrix_path, z_slice):
        
        # calculates the z shift to move the cropped image to
        _, _, img_header = self.get_img_objects(img_path)
        del _
        slice_width = img_header['pixdim'][3]
        z_shift = z_slice * slice_width

        # creates the transformation matrix to use in updating the Sform 
        identity_matrix = np.identity(4)
        identity_matrix[2][3] = z_shift 
        #print(identity_matrix)

        # saves the transformation matrix to use later on with updating the Sform 
        identity_matrix = pd.DataFrame(identity_matrix)
        np.savetxt(affine_matrix_path, identity_matrix, fmt='%d')

    def crop_Img(self, img_path, new_img_path, ImgType):

        z_slice_upper, z_slice_lower = self.return_cropping_info(ImgType=ImgType)
        affine_matrix_path = 'Sform_matrix_path.txt'

        self.calc_Sform_matrix(img_path, affine_matrix_path, z_slice_lower)

        img_data, img_affine, img_header = self.get_img_objects(img_path)
        
        if ImgType == 'CT':
            img_data_copy = img_data[:,:,z_slice_lower:z_slice_upper]
        elif ImgType == 'CBCT':
            img_data_copy = img_data[:,z_slice_lower:z_slice_upper, :]

        # save the cropped image 
        NewNiftiObj = nib.Nifti1Image(img_data_copy, img_affine, img_header)
        nib.save(NewNiftiObj, new_img_path) 

        UpdSform(self.reg_transform, new_img_path, affine_matrix_path, new_img_path)

        os.remove(affine_matrix_path)


class GroupwiseRegs(MancData):

    def __init__(self, PatientNo, no_itterations, base_path, niftireg_path):
        self.PatientNo = PatientNo 
        self.no_itterations = no_itterations 
        MancData.__init__(self, base_path, niftireg_path, '')
        MancData.write_to_logfile('Groupwise Registration Patient ' + str(self.PatientNo))
        return
        
    def get_CBCT_relative_timepoints(self, anonymisation_key_path):

        anonymisation_key = self.read_anonymisation_key(anonymisation_key_path)
        CBCT_relative_timepoints = anonymisation_key.loc[anonymisation_key['No_Patient_ID'] == self.PatientNo].iloc[:,4:35].values.tolist()
        self.CBCT_relative_timepoints = CBCT_relative_timepoints[0]
        self.CBCT_relative_timepoints = [int(x) for x in self.CBCT_relative_timepoints if ~np.isnan(x)]
        return self.CBCT_relative_timepoints

    def refactor(self):

        # function that makes sure the folders are correctly set-up
        self.results_folder = str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_GROUPWISE/'
        if not os.path.exists(self.results_folder):
            os.mkdir(self.results_folder)
        
        for no_itteration in np.arange(0, self.no_itterations+1):
            affine_folder = self.results_folder + 'affine_' + str(no_itteration)
            if not os.path.exists(affine_folder):
                os.mkdir(affine_folder)

        self.postprocessing_path = self.results_folder + 'postprocessing/'
        if not os.path.exists(self.postprocessing_path):
            os.mkdir(self.postprocessing_path)

        self.CBCT_pCT_path = str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_pCT/'
        if not os.path.exists(self.CBCT_pCT_path):
            os.mkdir(self.CBCT_pCT_path)


        
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            # cropped imgs 
            source = str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_' + str(CBCT_timepoint) + '/MASKED_CBCT_' +str(CBCT_timepoint) + '.nii.gz'
            destination = self.results_folder + 'affine_0/CBCT_' + str(CBCT_timepoint) + '.nii.gz'
            shutil.copy(source, destination)

        for CBCT_timepoint in self.CBCT_relative_timepoints:
            # full imgs 
            source = str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_' + str(CBCT_timepoint) + '/MASKED_CBCT_' +str(CBCT_timepoint) + '.nii.gz'
            destination = self.postprocessing_path + '/CBCT_' + str(CBCT_timepoint) + '.nii.gz'
            shutil.copy(source, destination)
        
        
    
    def set_itteration(self, itteration):

        self.itteration = itteration
        
    def set_ref_img(self):

        # set the target/ reference img for that iteration 
        if self.itteration == 0:
            self.ref_img = str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_0/CBCT_0.nii.gz'
        else:
            self.ref_img = self.results_folder + '/affine_' + str(self.itteration) + '/average_CBCT.nii.gz'
    
    def set_float_imgs(self):
        self.float_imgs = []
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            self.float_imgs.append(self.results_folder + '/affine_' + str(self.itteration) + '/CBCT_'+str(CBCT_timepoint)+'.nii.gz')

    def set_rigidReg_affinematrixes(self):
    
        self.affine_matrixes = []
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            self.affine_matrixes.append(self.results_folder + '/affine_' + str(self.itteration+1) + '/affine_'+str(CBCT_timepoint)+'.txt')

    def set_rigidReg_resampledimgs(self):

        self.rigidReg_resampled_imgs = []
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            self.rigidReg_resampled_imgs.append(self.results_folder + '/affine_' + str(self.itteration +1) + '/res_CBCT_'+str(CBCT_timepoint)+'.nii.gz')

    def set_composed_affinematrixes(self):

        self.compaffine_matrixes = []
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            self.compaffine_matrixes.append(self.results_folder + '/affine_' + str(self.itteration+1) + '/comp_affine_'+str(CBCT_timepoint)+'.txt')

    def set_resampledimgs(self):

        self.resampled_imgs = []
        for CBCT_timepoint in self.CBCT_relative_timepoints:
            self.resampled_imgs.append(self.results_folder + '/affine_' + str(self.itteration+1) + '/CBCT_'+str(CBCT_timepoint)+'.nii.gz')

    def set__itteration(self, itteration):

        self.set_itteration(itteration)
        self.set_ref_img()
        self.set_float_imgs()
        self.set_rigidReg_affinematrixes()
        self.set_rigidReg_resampledimgs()
        self.set_composed_affinematrixes()
        self.set_resampledimgs()

    def rigidGroupReg(self):

        for index in np.arange(0, len(self.CBCT_relative_timepoints)):

            float_img = self.float_imgs[index]
            affine_matrix = self.affine_matrixes[index]
            resampled_img = self.rigidReg_resampled_imgs[index]

            rigidReg(self.reg_aladin, self.ref_img, float_img, affine_matrix, resampled_img, RigOnly = True)

            #os.remove(resampled_img)

            self.test__rigidReg()



    def test__rigidReg(self, affine_matrix_path):

        if not os.file.exists(affine_matrix_path):

            matrix = np.identity(4)
            np.savetxt(affine_matrix_path, matrix)

            MancData.write_to_logfile('Rigid Registration saved as identity: ' + str(affine_matrix_path))


    def avgAffine(self):

        self.average_affine = self.results_folder + '/affine_' + str(self.itteration + 1) + '/average_affine.txt'

        avgAff(self.reg_average, self.average_affine, self.affine_matrixes)

    def invAffine(self):
        
        self.inv_affine = self.results_folder + '/affine_' + str(self.itteration + 1) + '/inv_average_affine.txt'

        invAff(self.reg_transform, self.ref_img, self.average_affine, self.inv_affine)

    def compAffine(self):

        for index in np.arange(0, len(self.CBCT_relative_timepoints)):
            
            affine_matrix = self.affine_matrixes[index]
            comp_matrix = self.compaffine_matrixes[index]

            compAff(self.reg_transform, self.ref_img, self.inv_affine, affine_matrix, comp_matrix)

    def resampleImages(self):

        for index in np.arange(0, len(self.CBCT_relative_timepoints)):
            
            float_img = self.float_imgs[index]
            resampled_img = self.resampled_imgs[index]
            transformation = self.compaffine_matrixes[index]
            
            resampleImg(self.reg_resample, self.ref_img, float_img, transformation, resampled_img)
    
    def avgImage(self):

        avg_img_path = self.results_folder + '/affine_' + str(self.itteration +1) + '/average_CBCT.nii.gz'

        img_data, _, _ = self.get_img_objects(self.resampled_imgs[0])
        img_shape = np.shape(np.array(img_data))
        del(img_data)
        del(_)

        # create an array of nans for storage
        Nan_map = np.empty(shape=(img_shape[0],img_shape[1],img_shape[2],len(self.resampled_imgs)))
        del(img_shape)

        for index in np.arange(0,len(self.resampled_imgs)):

            # imports the data 
            img_data, img_affine, img_header = self.get_img_objects(self.resampled_imgs[index])
          

            #store
            Nan_map[:,:,:,index] = img_data

        del(img_data)

        # calculate the average image, ignoring the nans
        Masked_Average = np.nanmean(Nan_map, axis = 3)
        del(Nan_map)
        Average = Masked_Average.copy()
        del(Masked_Average)  

        # save 
        Avg_Niftiobj = nib.Nifti1Image(Average, img_affine, img_header)
        nib.save(Avg_Niftiobj, avg_img_path)


    def UpdateGroupSform(self):

        for CBCT_timepoint in self.CBCT_relative_timepoints:
            for itteration in np.arange(0, self.no_itterations):
                
                img = self.postprocessing_path + '/CBCT_' + str(CBCT_timepoint) + '.nii.gz'
                affine_matrix_path = self.results_folder + '/affine_' + str(itteration+1) + '/comp_affine_'+str(CBCT_timepoint)+'.txt'

                UpdSform(self.reg_transform, img, affine_matrix_path, img)

    def rigidpCTReg(self):

        ref_img = self.results_folder = str(self.base_path) + '/' + str(self.PatientNo) + '/pCT/MASKED_pCT.nii.gz'
        float_img = self.postprocessing_path + '/CBCT_0.nii.gz'
        transformation = self.CBCT_pCT_path + '/affine.txt'
        resampled_img = self.CBCT_pCT_path + '/CBCT_0.nii.gz'

        rigidReg(self.reg_aladin, ref_img, float_img, transformation, resampled_img, RigOnly= True)

        self.test__rigidReg(transformation)

    def UpdateSform(self):

        for CBCT_timepoint in self.CBCT_relative_timepoints:

            img_to_be_updated = self.postprocessing_path + '/CBCT_' + str(CBCT_timepoint) + '.nii.gz'
            affine_matrix_path = self.CBCT_pCT_path + '/affine.txt'
            updated_img = self.CBCT_pCT_path + '/CBCT_' + str(CBCT_timepoint) + '.nii.gz'

            UpdSform(self.reg_transform, img_to_be_updated, affine_matrix_path, updated_img)
    
class AtlasRegs(MancData):

    def __init__(self, PatientNo, base_path, niftireg_path, atlas_path):
        MancData.__init__(self, base_path, niftireg_path, atlas_path)
        self.PatientNo = PatientNo
        self.PatientPath = self.base_path + '/' + str(self.PatientNo) +'/'
        self.PatientCTPath = self.PatientPath + 'pCT/'
        MancData.write_to_logfile('Atlas Registration Patient ' + str(self.PatientNo))
        

    def refactor(self):
        self.ModelSpacePath = self.PatientCTPath + '/model_space/'
        if not os.path.exists(self.ModelSpacePath):
            os.mkdir(self.ModelSpacePath)

        UCLHRegsPath = self.base_path + '/UCLHMODELSPACE_REGS/'
        if not os.path.exists(UCLHRegsPath):
            os.mkdir(UCLHRegsPath)
        
        self.PatientUCLHRegsPath = UCLHRegsPath + str(self.PatientNo) +'/'
        if not os.path.exists(self.PatientUCLHRegsPath):
            os.mkdir(self.PatientUCLHRegsPath)

    def test__RigidReg(self, affine_matrix_path):
        if not os.path.exists(affine_matrix_path):

            matrix = np.identity(4)
            np.savetxt(affine_matrix_path, matrix)

            MancData.write_to_logfile('Rigid Registration saved as identity: ' + str(affine_matrix_path))
    

    def InitAlignment(self):

        float_img = self.PatientCTPath + 'atlas_MASKED_pCT.nii.gz'
        affine_matrix = self.ModelSpacePath + 'InitAlignment_atlas.txt'
        resampled_img = self.ModelSpacePath + 'resampled_InitAlignment_pCT.nii.gz'

        rigidReg(self.reg_aladin, self.atlas_path, float_img, affine_matrix, resampled_img, RigOnly= True)
        #os.remove(resampled_img)

        self.test__RigidReg(affine_matrix)

        img_to_be_updated = self.PatientCTPath + 'atlas_MASKED_pCT.nii.gz' 
        updated_img = self.ModelSpacePath + 'InitAlignment_pCT.nii.gz'
        UpdSform(self.reg_transform, img_to_be_updated, affine_matrix, updated_img)
        return

    def RigidReg(self):

        float_img = self.ModelSpacePath + 'InitAlignment_pCT.nii.gz'
        affine_matrix = self.ModelSpacePath + 'Rigid_atlas.txt'
        resampled_img = self.ModelSpacePath + 'resampled_pCT_atlas_rigid.nii.gz'

        rigidReg(self.reg_aladin, self.atlas_path, float_img, affine_matrix, resampled_img, RigOnly= True)
        #os.remove(resampled_img)

        self.test__RigidReg(affine_matrix)
        
        img_to_be_updated = self.ModelSpacePath + 'InitAlignment_pCT.nii.gz'
        updated_img = self.ModelSpacePath + 'Rigid_pCT.nii.gz'
        UpdSform(self.reg_transform, img_to_be_updated, affine_matrix, updated_img)

        return
    
    def AffineReg(self):

        float_img = self.ModelSpacePath + 'Rigid_pCT.nii.gz'
        affine_matrix = self.ModelSpacePath + 'Affine_atlas.txt'
        resampled_img =self.ModelSpacePath + 'resampled_pCT_atlas_affine.nii.gz'

        rigidReg(self.reg_aladin, self.atlas_path, float_img, affine_matrix, resampled_img, RigOnly= False)
        #os.remove(resampled_img)

        self.test__RigidReg(affine_matrix)
        
        img_to_be_updated = self.ModelSpacePath + 'Rigid_pCT.nii.gz'
        updated_img = self.ModelSpacePath + 'Affine_pCT.nii.gz'
        UpdSform(self.reg_transform, img_to_be_updated, affine_matrix, updated_img)
        
        return
    
    def DefReg(self):

        float_img = self.ModelSpacePath + 'Affine_pCT.nii.gz'
        resampled_img = self.ModelSpacePath + 'DEF_pCT.nii.gz'
        transformation = self.ModelSpacePath + 'cpp_pCT.nii.gz'
        deformableReg(self.reg_f3d, self.atlas_path, float_img, resampled_img, transformation)
        return
    
    def Calc_Tatlas(self):
        
        # calculate deformation fields of affine matrixes
        input_transformation = self.ModelSpacePath + 'InitAlignment_atlas.txt'
        output_transformation = self.ModelSpacePath + 'InitAlignment_atlas.nii.gz'
        RigidToDeformation(self.reg_transform, self.atlas_path, input_transformation, output_transformation)
        input_transformation = self.ModelSpacePath + 'Rigid_atlas.txt'
        output_transformation = self.ModelSpacePath + 'Rigid_atlas.nii.gz'
        RigidToDeformation(self.reg_transform, self.atlas_path, input_transformation, output_transformation)
        input_transformation = self.ModelSpacePath + 'Affine_atlas.txt'
        output_transformation = self.ModelSpacePath + 'Affine_atlas.nii.gz'
        RigidToDeformation(self.reg_transform, self.atlas_path, input_transformation, output_transformation)

        transformation1 = self.ModelSpacePath + 'Rigid_atlas.nii.gz'
        transformation2 = self.ModelSpacePath + 'InitAlignment_atlas.nii.gz'
        output_transformation1 = self.ModelSpacePath + 'comp1.nii.gz'
        ComposeTransformations(self.reg_transform, self.atlas_path, transformation1, transformation2, output_transformation1)
        #os.remove(transformation1)
        #os.remove(transformation2)

        transformation1 = self.ModelSpacePath + 'Affine_atlas.nii.gz'
        transformation2 = self.ModelSpacePath + 'comp1.nii.gz'
        output_transformation2 = self.ModelSpacePath + 'comp2.nii.gz'
        ComposeTransformations(self.reg_transform, self.atlas_path, transformation1, transformation2, output_transformation2)
        #os.remove(transformation1)
        #os.remove(transformation2)

        transformation1 = self.ModelSpacePath + 'cpp_pCT.nii.gz'
        transformation2 = self.ModelSpacePath + 'comp2.nii.gz'
        output_transformation3 = self.PatientPath + 'T_model.nii.gz'
        ComposeTransformations(self.reg_transform, self.atlas_path, transformation1, transformation2, output_transformation3)
        #os.remove(transformation2)

        return


    def ResampleImgs(self, CBCT_timepoints):

        # function which uses T_model to resample all patient images into the model space
        T_model = self.PatientPath + 'T_model.nii.gz'
        
        float_img = self.PatientCTPath + 'MASKED_pCT.nii.gz'
        resampled_img = self.PatientUCLHRegsPath + '/MASKED_pCT.nii.gz'
        resampleImg(self.reg_resample, self.atlas_path, float_img, T_model, resampled_img)
        
        for CBCT_timepoint in CBCT_timepoints:

            CBCT_RegsPath = self.PatientUCLHRegsPath + '/CBCT_' + str(CBCT_timepoint)
            if not os.path.exists(CBCT_RegsPath):
                os.mkdir(CBCT_RegsPath)
 
            float_img =  str(self.base_path) + '/' + str(self.PatientNo) + '/CBCT_pCT/CBCT_' + str(CBCT_timepoint) + '.nii.gz'
            resampled_img = CBCT_RegsPath + '/MASKED_CBCT.nii.gz'
            resampleImg(self.reg_resample, self.atlas_path, float_img, T_model, resampled_img)

        


class DefromableRegs(MancData):

    def __init__(self, PatientNo, base_path, niftireg_path):
        MancData.__init__(self, base_path, niftireg_path, '')
        self.PatientNo = PatientNo
        self.PatientUCLHRegsPath = self.base_path + '/UCLHMODELSPACE_REGS/' + str(self.PatientNo)
        MancData.write_to_logfile('Deformable Registration Patient ' + str(self.PatientNo))

    def set__CBCTtimepoint(self, CBCT_timepoint):

        self.CBCT_timepoint = CBCT_timepoint

    def test__DefReg(self, transformation_path):

        if not os.path.exists(self):
            MancData.write_to_logfile('Failed Registration CBCT: ' + str(self.CBCT_timepoint))



    def DefReg(self):
        
        float_img = self.PatientUCLHRegsPath + '/MASKED_pCT.nii.gz'
        ref_img = self.PatientUCLHRegsPath + '/CBCT_' + str(self.CBCT_timepoint) + '/MASKED_CBCT.nii.gz'
        resampled_img = self.PatientUCLHRegsPath + '/CBCT_' + str(self.CBCT_timepoint) + '/DEF_CBCT.nii.gz'
        cpp = self.PatientUCLHRegsPath + '/CBCT_' + str(self.CBCT_timepoint) +'/cpp_CBCT.nii.gz'

        deformableReg(self.reg_f3d, ref_img, float_img, resampled_img, cpp)

        self.test__DefReg()

    