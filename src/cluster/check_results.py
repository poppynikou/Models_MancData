'''
check to see what results are missing 
'''

from classes import *

base_path = 'D:/CHRISTIE_HN/'
patients_csv_path = os.path.join(os.getcwd(), 'Data/Anonymisation_Key.csv')
results_path = ''

patients = os.listdir(os.path.join(base_path, 'Masks'))
numcps = np.arange(4,8)
Models = ['LOO', 'noLOO']
structures = ['BRAINSTEM', 'CORD', 'CTVHIGH', 'CTVLOW', 'LPAROTID', 'RPAROTID']

text_file1 = 'LOO_log.txt'
file1 = open(text_file1, 'a')
text_file2 = 'noLOO_log.txt'
file2 = open(text_file2, 'a')


for patient in patients:

    for numcp in numcps:

        PSM_Model = PSM(base_path, patient, numcp, patients_csv_path, results_path)
        Training_time_points = PSM_Model.get_CBCT_time_points()

        for model in Models:
            
            if model == 'LOO':

                for time_point in Training_time_points[1:-1]:
                    #check cpp exists
                    cpp_path = base_path + str(model) + '/PSM_CPS_' + str(numcp) + '/' + str(patient) + '/cpp_' + str(time_point) + '.nii.gz'
                    if not os.path.exists(cpp_path):
                        file1.write(str(cpp_path) + '\n')
                    for structure in structures:
                        structure_path = base_path + str(model) + '/PSM_CPS_' + str(numcp) + '/' + str(patient) + '/BIN_' +str(structure) + '_T_' + str(time_point) + '.nii.gz'
                        if not os.path.exists(structure_path):
                            file1.write(str(structure_path) + '\n')
            else:    
                for time_point in Training_time_points:
                    #check cpp exists
                    cpp_path = base_path + str(model) + '/PSM_CPS_' + str(numcp) + '/' + str(patient) + '/cpp_' + str(time_point) + '.nii.gz'
                    if not os.path.exists(cpp_path):
                        file2.write(str(cpp_path) + '\n')

                    for structure in structures:
                        structure_path = base_path + str(model) + '/PSM_CPS_' + str(numcp) + '/' + str(patient) + '/BIN_' +str(structure) + '_T_' + str(time_point) + '.nii.gz'
                        if not os.path.exists(structure_path):
                            file2.write(str(structure_path) + '\n')