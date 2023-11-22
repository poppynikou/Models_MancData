import numpy as np 
from classes import *
import sys

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

results_path = "/home/pnikou/Documents/Manc_Data/LOO/"
if not os.path.exists(results_path):
        os.mkdir(results_path)
        
PSM_Model = PSM(base_path, patient, numcp, patients_csv_path, results_path)
Training_time_points = PSM_Model.get_training_time_points()

# LOO model
for index, time_point in enumerate(Training_time_points[1:-1]):

        # define time points in the building and testing
        training_time_points = Training_time_points.copy()
        training_time_points.remove(training_time_points[index+1])
        testing_time_point = [Training_time_points[index+1]]
        
        PSM_Model.set_training_time_points(training_time_points)
        PSM_Model.set_testing_time_points(testing_time_point)
        PSM_Model.set_reference_data()

        PSM_Model.fit_SM()
        PSM_Model.test_SM()
        PSM_Model.save_SM() 
        
        PSM_Model.resample_GT_Model()
        PSM_Model.resample_RTSTRUCTs()
        PSM_Model.resample_GT_RTSTRUCTs()

                        

                        