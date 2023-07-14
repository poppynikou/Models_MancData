import nibabel as nib
import numpy as np 
import os 
from datetime import datetime, date




# check this works 
def get_time_points(base_path, patient_no):
    '''
    This function assumes that each image is stored in the folder w/ naming convention:

    CBCT_yyyymmdd - for CBCT images
    CT_yyyymmdd - for CT images 

    This function only lists the dates of the CBCT images.
    returns: yyyymmdd
    
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


def get_img_metadata(img_path):
    img = nib.load(img_path)
    img_shape = img.header['dim'][1:4]
    img_resolution = img.header['pixdim'][1:4]

    return img_shape, img_resolution


def get_metadata(cpp_directory):

    cpp = nib.load(cpp_directory)
    cpp_affine, cpp_header = cpp.affine, cpp.header

    return cpp_affine, cpp_header


def get_total_CBCT_numbers(patient_list):

    no_CBCTs = 0
    for patient in patient_list:
        no_CBCTs = no_CBCTs + len(get_dates(patient))

    return no_CBCTs


def get_image_objects(Img_path):
    
    img = nib.load(Img_path)
    img_obj = img.get_fdata()
    img_affine = img.affine
    img_header = img.header

    return img_obj, img_affine, img_header


'''

# check the cpp_directory path whenever you need  it 
def get_cpp_shape(base_path, Patient_no, CBCT_time_point):

    # reads in the cpp file, finds it's shape and resolution of the pixels 
    cpp_directory = base + '/HN_' + str(patient) + '/CBCT_' + str(CBCT_time_point) + '/'


    cpp = nib.load(cpp_directory)
    
    cpp_shape = tuple(cpp.header['dim'][1:4],) + (3,)
    cpp_resolution = cpp.header['pixdim'][1:4]
    
    return cpp_shape, cpp_resolution


def get_modelvel(Patient_no, CBCT_dates, cpp_shape, model_space = True):
    # creates an array to store cpp data
    coordinates = np.empty(shape=((len(CBCT_dates), ) + tuple(cpp_shape)), dtype=np.float32)
    #print(coordinates.shape)
    # gets all the data from all the CBCTs in that patient series
    
    for i, CBCT_date in enumerate(CBCT_dates):
        if model_space:
            cpp_directory = 'D:/Transported_Patients/HN_'+str(Patient_no)+'/CBCT_'+str(CBCT_date)+'/velocity_T3.nii.gz'
        else: 
            cpp_directory = 'D:/pCT_Atlas/New_Longitudinal_Regs/HN_'+str(Patient_no)+'/CBCT_'+str(CBCT_date)+'/cpp_CBCT_'+str(CBCT_date)+'.nii.gz'
        cpp = nib.load(cpp_directory)
        cpp = np.squeeze(cpp.dataobj)
        #cpp = cpp[0:67, 0:67, 0:35, :] # only if in the patient specific space, some patients are longer than others 
        coordinates[i] = cpp

    return coordinates


def get_cpp(Patient_no, CBCT_dates, cpp_shape):
    
    # creates an array to store cpp data
    coordinates = np.empty(shape=((len(CBCT_dates), ) + tuple(cpp_shape)))
    
    # gets all the data from all the CBCTs in that patient series
    for i, CBCT_date in enumerate(CBCT_dates):

        cpp_directory = 'D://UCLH_HN//HN_' + str(Patient_no) + '//CBCT_' + str(CBCT_date) + '//GROUPWISE_REGs//cpp_grid.nii.gz'
        cpp = nib.load(cpp_directory)
        cpp = np.squeeze(cpp.dataobj)
        coordinates[i] = cpp

    return coordinates



def get_structures(patient, pCT_date):

    structure_folder = 'D://UCLH_HN//HN_' + str(patient) + '//CT_' + str(pCT_date) + '//STRUCTURES//'

    folder = os.listdir(structure_folder)

    CTV_doses = ['CTV'+ str(file[7:9]) for file in folder if file[0:7] == 'BIN_CTV']

    Body = ['NOBOLUS_BODY' for file in folder if file[0:16] == 'BIN_NOBOLUS_BODY']

    if Body == []:  
        Body.append('BODY')

    return CTV_doses + Body
'''