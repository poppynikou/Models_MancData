import shutil
import os

batches = [2,3]


for batch in batches:
    base_path = 'X:/Poppy/PatData/batch' + str(batch) + '/'
    patients = os.listdir(base_path)
    for patient in patients: 
        
            if patient[0:3] == 'HN_':
                
                
                path = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_0/'
                if os.path.exists(path):
                    shutil.rmtree(path)
                path ='X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_1/'
                if os.path.exists(path):
                    shutil.rmtree(path)
                path = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_2/'
                if os.path.exists(path):
                    shutil.rmtree(path)
                path = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/postprocessing/'
                if os.path.exists(path):
                    shutil.rmtree(path)
                path = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/'
                if os.path.exists(path):
                    shutil.rmtree(path)
                path =  'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_pCT'
                if os.path.exists(path):
                    shutil.rmtree(path)
                   