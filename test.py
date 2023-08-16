import os 
import shutil 


for batch in [2,3]:
    
    base_path = 'T:/Poppy/PatData/batch'+str(batch)+'/'

    patients = os.listdir(base_path)
    for patient in patients: 
        if patient[0:3] == 'HN_':
            
            path1 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_0'
            path2 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_1'
            path3 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/affine_2'
            path4 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/postprocessing'
            path0 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE/'
            path5 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_GROUPWISE_crop'
            path6 = 'T:/Poppy/PatData/batch'+str(batch)+'/'+str(patient)+'/CBCT_pCT'
            
            for path in [path1, path2, path3, path4, path0,path5, path6]:
                
                if os.path.exists(path):
                    shutil.rmtree(path)
    
    