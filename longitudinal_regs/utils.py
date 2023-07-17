import nibabel as nib
import numpy as np 
import os 
from datetime import datetime, date

# check this works 
def get_time_points(base_path, patient_no):
    '''
    This function assumes that each image is stored in the folder w/ naming convention:
    CBCT_no - for CBCT images
    This function only lists the relative time points of the CBCT images.
    returns: no
    
    '''
    CBCT_dates = []
    # function to find folder names of the CBCTs in the patient directory
    directory = base_path + '/HN_' + str(patient_no) + '/'
    dates = os.listdir(directory)
    for date in dates:
        if date[0:4] == 'CBCT':
            if len(date) == 7:
                CBCT_dates.append(date[-2:])
            elif len(date) ==6:
                CBCT_dates.append(date[-1])
    CBCT_dates = np.sort(np.array(CBCT_dates, dtype = int))
    return CBCT_dates

def mask_elekta_CBCT(img_path, masked_img_path):
        
    CBCT_obj = nib.load(img_path)
    CBCT_img = CBCT_obj.get_fdata()
    CBCT_affine = CBCT_obj.affine
    CBCT_header = CBCT_obj.header

    CBCT_img_ = CBCT_img.copy()
    CBCT_img_ = np.array(CBCT_img_, dtype = np.float32)

    # index at top corner 
    masking_HU = CBCT_img_[0,0,0]

    CBCT_img_[CBCT_img_ == masking_HU] = np.NaN

    CBCT_header.set_data_dtype(np.float32)
    NewNiftiObj = nib.Nifti1Image(CBCT_img_, CBCT_affine, CBCT_header)
    nib.save(NewNiftiObj, masked_img_path)
    
    
def convert_to_float(img_path):
    
    img_obj, img_affine, img_header = get_image_objects(img_path)
    
    img_obj_copy = np.array(img_obj, dtype = np.float32)
    
    
    niftiobject1 = nib.Nifti1Image(img_obj_copy, img_affine, img_header)
    niftiobject1.set_data_dtype('float32')
    nib.save(niftiobject1, img_path)
    
def get_image_objects(Img_path):
    
    img = nib.load(Img_path)
    img_obj = img.get_fdata()
    img_affine = img.affine
    img_header = img.header

    return img_obj, img_affine, img_header



def resample_CT(ref_img, float_img, transformation, resampled_img, padding_value):
    
    reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'
    
    command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -pad ' + str(padding_value) + ' -omp 12'
    os.system(command)
