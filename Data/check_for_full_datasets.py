import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from math import ceil

path_to_csv = 'C:/Users/Poppy/Documents/Manc_data/Data/Anonymisation_Key.csv'

data = pd.read_csv(path_to_csv, header = 0)
patients_ = data['Index'].tolist()

def remove_duplicates(array):
    return np.array(list(set(array)), dtype = np.int8)

for patient in patients_:

    No_CBCTs = data.loc[data['Index']==patient]['No_CBCTs'].iloc[0]
    
    patient_CBCT_timepoints = []

    for CBCT_index in range(0, No_CBCTs):

        CBCT_header = 'CBCT' + str(CBCT_index)
        timepoint = data.loc[data['Index']==patient][CBCT_header].iloc[0]
        patient_CBCT_timepoints.append(timepoint)

    patient_CBCT_timepoints = remove_duplicates(patient_CBCT_timepoints)

    data_set = np.sort(np.array(patient_CBCT_timepoints, dtype = np.int8))

 