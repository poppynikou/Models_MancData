import numpy as np 
from src.utils.classes import *
import os
import pandas as pd
from src.utils.functions import * 

batches = [2,3]
niftireg_path = 'X:/Poppy/niftireg_executables/'
no_itterations = 2
# path to the file which contains all patient info
patients_csv_path = 'X:/Poppy/Anonymisation_Key.csv'
atlas_path = 'X:/Poppy/PatData/MASKED_average_pCT.nii.gz'
onedrive_path = 'C:/Users/Poppy/OneDrive - University College London/Manc_Data_Log/'

for batch in batches:
    base_path = 'X:/Poppy/PatData/batch' + str(batch) + '/'
    patients = os.listdir(base_path)
    for patient in patients: 
        
            if patient[0:3] == 'HN_':
                
                try:    
                    # if a certain path exists and is not empty 
                    # check before you do it again 
                    ImageObj = Image(patient, base_path, niftireg_path)

                    GroupwiseReg = GroupwiseRegs(patient,no_itterations, base_path, niftireg_path, onedrive_path)
                    CBCT_relative_timepoints = GroupwiseReg.get_CBCT_relative_timepoints(patients_csv_path)
                    GroupwiseReg.refactor()
                    
                    
                    for itteration in np.arange(0, no_itterations):

                        GroupwiseReg.set__itteration(itteration)
                        GroupwiseReg.rigidGroupReg()
                        GroupwiseReg.avgAffine()
                        GroupwiseReg.invAffine()
                        GroupwiseReg.compAffine()
                        GroupwiseReg.resampleImages()
                        GroupwiseReg.avgImage()
                    
                    
                    GroupwiseReg.UpdateGroupSform()
                    GroupwiseReg.rigidpCTReg()
                    GroupwiseReg.UpdateSform()
                    
                    
                    
                    AtlasAlignment = AtlasRegs(patient, base_path, niftireg_path, atlas_path, onedrive_path)

                    AtlasAlignment.refactor()

                    AtlasAlignment.InitAlignment()
                    AtlasAlignment.RigidReg()
                    AtlasAlignment.AffineReg()
                    AtlasAlignment.DefReg()
                    AtlasAlignment.Calc_Tatlas()
                    

                    AtlasAlignment.ResampleImgs(CBCT_relative_timepoints)
                    
                    LongitudinalRegs = DefromableRegs(patient, base_path, niftireg_path, onedrive_path)
            
                    for CBCT_timepoint in CBCT_relative_timepoints[-2:]:
                        
                        LongitudinalRegs.set__CBCTtimepoint(CBCT_timepoint)
                        LongitudinalRegs.DefReg()
                except:
                    pass
                
                