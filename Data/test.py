import numpy as np 
import pandas as pd
import os

anonymisation_key_path = os.path.join(os.getcwd(), 'Data\\Anonymisation_Key.csv') 
Patient_No = 'HN_0'
anonymisation_key = pd.read_csv(anonymisation_key_path, header = 0)
#print(anonymisation_key.loc[anonymisation_key['No_Patient_ID'] == self.Patient_No])
CBCT_relative_timepoints = anonymisation_key.loc[anonymisation_key['No_Patient_ID'] == Patient_No].iloc[:,4:35].values.tolist()
CBCT_relative_timepoints = CBCT_relative_timepoints[0]
CBCT_relative_timepoints = [int(x) for x in CBCT_relative_timepoints if ~np.isnan(x)]
#CBCT_relative_timepoints = np.unique(CBCT_relative_timepoints)
CBCT_relative_timepoints = list(set(CBCT_relative_timepoints))
print(CBCT_relative_timepoints)