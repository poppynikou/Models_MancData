import os 
import shutil 


for batch in [2,3]:
    
    base_path = 'X:/Poppy/PatData/batch'+str(batch)+'/'

    patients = os.listdir(base_path)
    for patient in patients: 
        if patient[0:3] == 'HN_':
            
            path1 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_0'
            path2 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_1'
            path3 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_2'
            path4 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/postprocessing'
            path0 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/'
            path5 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE_crop'
            path6 = 'X:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_pCT'
            
            for path in [path1, path2, path3, path4, path0,path5, path6]:
                
                if os.path.exists(path):
                    shutil.rmtree(path)
    
    