import os
import pandas as pd
#import nibabel as nib 
import numpy as np 

# find number of patients which are already anonymised and ordered in my data folder 
def find_no_anonymised(path):

    folders = os.listdir(path)

    no_anonymised = len([folder for folder in folders if folder[0:3] == 'HN_'])

    return no_anonymised


exported_data_path = 'T:/Poppy/PatData/'
output_csv_path = 'T:/Poppy/Poppys_Packs.csv'

'''
patients = os.listdir(exported_data_path)
patient_dataframe = {'Patient_ID':[], 'No_Patient_ID':[], 'No_CBCTs':[]}

for index, patient in enumerate(patients):

    patient_dataframe['Patient_ID'].append(patient[0:9])
    
    No_CBCTs = int(len(os.listdir(exported_data_path + patient))) -1
    patient_dataframe['No_CBCTs'].append(No_CBCTs)

    offset = find_no_anonymised(exported_data_path)

    Patient_ID_No = index + offset
    Patient_ID = 'HN_' + str(Patient_ID_No)
    patient_dataframe['No_Patient_ID'].append(Patient_ID)


dataFrame = pd.DataFrame(patient_dataframe)

# write dataFrame to SalesRecords CSV file
dataFrame.to_csv(output_csv_path)

'''







