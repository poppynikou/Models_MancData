import os 
base_path = 'T:/Poppy/PatData/batch3/'

for patient in os.listdir(base_path):

    structures = [x for x in os.listdir(base_path + '/' + str(patient)) if x.__contains__('BIN_')]
                     
    if len(structures) < 7:
        
        print(patient)
        print(structures)
    
