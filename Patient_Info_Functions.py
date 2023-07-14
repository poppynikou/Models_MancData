import nibabel as nib
import numpy as np 
import os 
from datetime import datetime, date

def get_pCT_date(patient_no):
    # function to find the pCT date for a specific patient 
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    # list all contents of the directory 
    dates = os.listdir(directory)
    # find all folders which start with 'CT_'
    CT_dates = [date[-8:]  for date in list(dates) if date[0:2] == 'CT' and date[-3:] != 'dcm']
    CT_dates = np.asarray(CT_dates, dtype=object)
    # get the dates times, so that you can get the one which is earliest in time 
    CT_datetimes = [datetime(int(CT[0:4]), int(CT[4:6]), int(CT[6:8])) for CT in CT_dates]
    pCT_datetime = [min(CT_datetimes)]

    Boolean = np.in1d(CT_datetimes, pCT_datetime)

    pCT_date = CT_dates[Boolean][0]
    
    return pCT_date

def get_rCT_date(patient_no):
    # function to find the pCT date for a specific patient 
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    # list all contents of the directory 
    dates = os.listdir(directory)
    # find all folders which start with 'CT_'
    CT_dates = [date[-8:]  for date in list(dates) if date[0:2] == 'CT' and date[-3:] != 'dcm']
    CT_dates = np.asarray(CT_dates, dtype=object)
    # get the dates times, so that you can get the one which is earliest in time 
    CT_datetimes = [datetime(int(CT[0:4]), int(CT[4:6]), int(CT[6:8])) for CT in CT_dates]
    rCT_datetime = [max(CT_datetimes)]

    Boolean = np.in1d(CT_datetimes, rCT_datetime)

    rCT_date = CT_dates[Boolean][0]
    
    return rCT_date



def get_dates(patient_no):
    '''
    This function assumes that each image is stored in the folder w/ naming convention:

    CBCT_yyyymmdd - for CBCT images
    CT_yyyymmdd - for CT images 

    This function only lists the dates of the CBCT images.
    returns: yyyymmdd
    
    '''
    # function to find folder names of the CBCTs in the patient directory
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    dates = os.listdir(directory)
    CBCT_dates = [date[-8:]  for date in list(dates) if date[0:4] == 'CBCT' and date[-3:] != 'dcm']
    return CBCT_dates


def get_time_points(CBCT_dates):
    '''
    This assumes that the first time points is the first CBCT in the series
    '''

    # create an array to store the time points
    time_points = []

    # find the date for the first CBCT date 
    day_zero = CBCT_dates[0]
    date_zero = date(int(day_zero[0:4]), int(day_zero[4:6]),  int(day_zero[6:8]))

    # loop through dates and get the time points
    for CBCT_date in CBCT_dates:
        
        CBCT_date = CBCT_date
        date_i = date(int(CBCT_date[0:4]), int(CBCT_date[4:6]),  int(CBCT_date[6:8]))
        time_points.append((date_i-date_zero).days) 

    return time_points

def get_cpp_shape(Patient_no, CBCT_date):

    # reads in the cpp file, finds it's shape and resolution of the pixels 
    cpp_directory = 'D://UCLH_HN//HN_' + str(Patient_no) + '//CBCT_' + str(CBCT_date) + '//GROUPWISE_REGs//cpp_grid.nii.gz'
    cpp = nib.load(cpp_directory)
    
    cpp_shape = tuple(cpp.header['dim'][1:4],) + (3,)
    cpp_resolution = cpp.header['pixdim'][1:4]
    
    return cpp_shape, cpp_resolution


def get_img_metadata(Patient_no, CBCT_date):
    img_directory = 'D://UCLH_HN//HN_' + str(Patient_no) + '//CBCT_' + str(CBCT_date) + '//GROUPWISE_RIGID_REGS//RIG_ALIGNED_CBCTs//CBCT_'+str(CBCT_date)+'.nii.gz'
    img = nib.load(img_directory)
    img_shape = img.header['dim'][1:4]
    img_resolution = img.header['pixdim'][1:4]

    return img_shape, img_resolution

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


def get_metadata(cpp_directory):

    cpp = nib.load(cpp_directory)
    
    cpp_affine, cpp_header = cpp.affine, cpp.header

    return cpp_affine, cpp_header

def get_structures(patient, pCT_date):

    structure_folder = 'D://UCLH_HN//HN_' + str(patient) + '//CT_' + str(pCT_date) + '//STRUCTURES//'

    folder = os.listdir(structure_folder)

    CTV_doses = ['CTV'+ str(file[7:9]) for file in folder if file[0:7] == 'BIN_CTV']

    Body = ['NOBOLUS_BODY' for file in folder if file[0:16] == 'BIN_NOBOLUS_BODY']

    if Body == []:  
        Body.append('BODY')

    return CTV_doses + Body

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
import nibabel as nib
import numpy as np 
import os 
from datetime import datetime, date

def get_pCT_date(patient_no):
    # function to find the pCT date for a specific patient 
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    # list all contents of the directory 
    dates = os.listdir(directory)
    # find all folders which start with 'CT_'
    CT_dates = [date[-8:]  for date in list(dates) if date[0:2] == 'CT' and date[-3:] != 'dcm']
    CT_dates = np.asarray(CT_dates, dtype=object)
    # get the dates times, so that you can get the one which is earliest in time 
    CT_datetimes = [datetime(int(CT[0:4]), int(CT[4:6]), int(CT[6:8])) for CT in CT_dates]
    pCT_datetime = [min(CT_datetimes)]

    Boolean = np.in1d(CT_datetimes, pCT_datetime)

    pCT_date = CT_dates[Boolean][0]
    
    return pCT_date

def get_rCT_date(patient_no):
    # function to find the pCT date for a specific patient 
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    # list all contents of the directory 
    dates = os.listdir(directory)
    # find all folders which start with 'CT_'
    CT_dates = [date[-8:]  for date in list(dates) if date[0:2] == 'CT' and date[-3:] != 'dcm']
    CT_dates = np.asarray(CT_dates, dtype=object)
    # get the dates times, so that you can get the one which is earliest in time 
    CT_datetimes = [datetime(int(CT[0:4]), int(CT[4:6]), int(CT[6:8])) for CT in CT_dates]
    rCT_datetime = [max(CT_datetimes)]

    Boolean = np.in1d(CT_datetimes, rCT_datetime)

    rCT_date = CT_dates[Boolean][0]
    
    return rCT_date



def get_dates(patient_no):
    '''
    This function assumes that each image is stored in the folder w/ naming convention:

    CBCT_yyyymmdd - for CBCT images
    CT_yyyymmdd - for CT images 

    This function only lists the dates of the CBCT images.
    returns: yyyymmdd
    
    '''
    # function to find folder names of the CBCTs in the patient directory
    directory = 'D://UCLH_HN//HN_' + str(patient_no) + '//'
    dates = os.listdir(directory)
    CBCT_dates = [date[-8:]  for date in list(dates) if date[0:4] == 'CBCT' and date[-3:] != 'dcm']
    return CBCT_dates


def get_time_points(CBCT_dates):
    '''
    This assumes that the first time points is the first CBCT in the series
    '''

    # create an array to store the time points
    time_points = []

    # find the date for the first CBCT date 
    day_zero = CBCT_dates[0]
    date_zero = date(int(day_zero[0:4]), int(day_zero[4:6]),  int(day_zero[6:8]))

    # loop through dates and get the time points
    for CBCT_date in CBCT_dates:
        
        CBCT_date = CBCT_date
        date_i = date(int(CBCT_date[0:4]), int(CBCT_date[4:6]),  int(CBCT_date[6:8]))
        time_points.append((date_i-date_zero).days) 

    return time_points

def get_cpp_shape(Patient_no, CBCT_date):

    # reads in the cpp file, finds it's shape and resolution of the pixels 
    cpp_directory = 'D://UCLH_HN//HN_' + str(Patient_no) + '//CBCT_' + str(CBCT_date) + '//GROUPWISE_REGs//cpp_grid.nii.gz'
    cpp = nib.load(cpp_directory)
    
    cpp_shape = tuple(cpp.header['dim'][1:4],) + (3,)
    cpp_resolution = cpp.header['pixdim'][1:4]
    
    return cpp_shape, cpp_resolution


def get_img_metadata(Patient_no, CBCT_date):
    img_directory = 'D://UCLH_HN//HN_' + str(Patient_no) + '//CBCT_' + str(CBCT_date) + '//GROUPWISE_RIGID_REGS//RIG_ALIGNED_CBCTs//CBCT_'+str(CBCT_date)+'.nii.gz'
    img = nib.load(img_directory)
    img_shape = img.header['dim'][1:4]
    img_resolution = img.header['pixdim'][1:4]

    return img_shape, img_resolution

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


def get_metadata(cpp_directory):

    cpp = nib.load(cpp_directory)
    
    cpp_affine, cpp_header = cpp.affine, cpp.header

    return cpp_affine, cpp_header

def get_structures(patient, pCT_date):

    structure_folder = 'D://UCLH_HN//HN_' + str(patient) + '//CT_' + str(pCT_date) + '//STRUCTURES//'

    folder = os.listdir(structure_folder)

    CTV_doses = ['CTV'+ str(file[7:9]) for file in folder if file[0:7] == 'BIN_CTV']

    Body = ['NOBOLUS_BODY' for file in folder if file[0:16] == 'BIN_NOBOLUS_BODY']

    if Body == []:  
        Body.append('BODY')

    return CTV_doses + Body

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