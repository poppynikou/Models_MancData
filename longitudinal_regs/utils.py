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

