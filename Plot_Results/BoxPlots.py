import os 
import matplotlib.pyplot as plt 
import pandas as pd 

structures = ['CTVHIGH', 'CTVLOW', 'CORD', 'LPAROTID', 'RPAROTID', 'BRAINSTEM']
metrics = ['DICE', 'AVERAGE_SDISTANCE', '95_SDISTANCE']
models = ['LOO', 'noLOO']
CPs = [4,5,6,7]
patients = os.listdir('D:/CHRISTIE_HN/Masks')

for structure in structures:

    CPS_Results = pd.DataFrame()

    for CP in CPs:

        for patient in patients:

            try:
                path_to_results = 'D:/CHRISTIE_HN/LOO/PSM_CPS_'+str(CP)+'/'+str(patient)+'/GeometricResults.txt'
                #print(path_to_results)
                Results = pd.read_csv(path_to_results, delimiter = ' ', header = None, skiprows=[0], names=list('abcdef'))     
                

            except:
                print(path_to_results)
        #print(CPS_Results.head())