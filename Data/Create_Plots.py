import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
from math import ceil
path_to_csv = 'C:/Users/Poppy/Documents/Manc_data/Data/Anonymisation_Key.csv'
path_to_shifts_csv = 'C:/Users/Poppy/Documents/Manc_data/Data/Day_shifts.csv'

def remove_duplicates(array):
    return np.array(list(set(array)), dtype = np.int8)

data = pd.read_csv(path_to_csv, header = 0)
patients_ = data['Index'].tolist()

shifts = pd.read_csv(path_to_shifts_csv, header = 0)

CBCT_timepoints = []
patients = []

for patient in patients_:

    No_CBCTs = data.loc[data['Index']==patient]['No_CBCTs'].iloc[0]
    
    patient_CBCT_timepoints = []
    patient_data = []

    for CBCT_index in range(0, No_CBCTs):

        CBCT_header = 'CBCT' + str(CBCT_index)
        timepoint = data.loc[data['Index']==patient][CBCT_header].iloc[0]
        patient_CBCT_timepoints.append(timepoint)

    CBCT_timepoints.append(remove_duplicates(patient_CBCT_timepoints))
    #print(np.ones(len(remove_duplicates(patient_CBCT_timepoints)), dtype = np.int8)*patient)
    patients.append(np.ones(len(remove_duplicates(patient_CBCT_timepoints)), dtype = np.int8)*patient)



for patient_index in patients_:
    plt.scatter(CBCT_timepoints[patient_index], patients[patient_index], color = 'k', marker = '.')



plt.plot(-0.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(4.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(6.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(11.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(13.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(18.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(20.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(25.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(27.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(32.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(34.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(39.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(41.5*np.ones(72), np.arange(-2, 70), color = 'c')

plt.xlabel('CBCT relative time point')
plt.ylabel('Patient')
plt.savefig('original.png')
plt.close()

shifted_CBCT_timepoints = []

for patient_index,CBCT_timepoint in enumerate(CBCT_timepoints):

    data_set = np.sort(np.array(CBCT_timepoint, dtype = np.int8))

    shift = shifts.loc[shifts['Patient'] == patient_index]['Shift']

    shifted_data = data_set + int(shift)

    shifted_CBCT_timepoints.append(shifted_data)

print(np.shape(shifted_CBCT_timepoints))

for patient_index in patients_:
   
    plt.scatter(shifted_CBCT_timepoints[patient_index], patients[patient_index], color = 'k', marker = '.')

plt.plot(-0.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(4.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(6.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(11.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(13.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(18.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(20.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(25.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(27.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(32.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(34.5*np.ones(72), np.arange(-2, 70), color = 'c')
plt.plot(39.5*np.ones(72), np.arange(-2, 70), color = 'tab:green')
plt.plot(41.5*np.ones(72), np.arange(-2, 70), color = 'c')

plt.xlabel('shifted CBCT relative time point')
plt.ylabel('Patient')
plt.savefig('shifted.png')
plt.close()

shifted_CBCT_timepoints_all = np.concatenate(shifted_CBCT_timepoints, axis=0)
last_date = [shifted_CBCT_timepoint[-1] for shifted_CBCT_timepoint in shifted_CBCT_timepoints]

plt.hist(shifted_CBCT_timepoints_all, bins=np.arange(min(shifted_CBCT_timepoints_all), max(shifted_CBCT_timepoints_all)))
plt.hist(last_date, bins = np.arange(min(last_date), max(last_date)), color = 'k')
plt.xlabel('shifted CBCT relative time point')
plt.ylabel('Frequency')
plt.savefig('Frequency.png')