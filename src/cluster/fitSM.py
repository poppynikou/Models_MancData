import numpy as np 
from classes import *
import sys
import os 

'''
Add in the different options for the training time points
'random' 
'weekly' 
'specific time points' 
'''

# base path to where the batches of patient images are stored
base_path = sys.argv[1]
# path to the file which contains all patient info
patients_csv_path = sys.argv[2]
#patient 
patient = 'HN_' + str(sys.argv[3])
# number of control points 
numcp = int(sys.argv[4])


results_path = "/home/pnikou/Documents/Manc_Data/noLOO/"

if not os.path.exists(results_path):
        os.mkdir(results_path)

PSM_Model = PSM(base_path, patient, numcp, patients_csv_path, results_path)
PSM_Model.set_training_time_points()
PSM_Model.set_testing_time_points()
PSM_Model.set_reference_data()

PSM_Model.fit_SM()
PSM_Model.test_SM()
PSM_Model.save_SM() 


if patient == 'HN_19':
        PSM_Model.resample_GT_Model()
        PSM_Model.resample_RTSTRUCTs()
        PSM_Model.resample_GT_RTSTRUCTs()
else:
        PSM_Model.resample_RTSTRUCTs()



                        

                        