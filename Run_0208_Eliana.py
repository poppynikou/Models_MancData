import numpy as np 
from src.utils.classes import *
import os
import pandas as pd
from src.utils.functions import * 

base_path = 'T:/Poppy/PatData/batch2/'
niftireg_path = 'T:/Poppy/niftireg_executables/'
no_itterations = 2
# path to the file which contains all patient info
patients_csv_path = 'T:/Poppy/Anonymisation_Key.csv'
patients = os.listdir(base_path)
atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'

for patient in patients: 
    
        if patient[0:3] == 'HN_':
    
            try:

                # if a certain path exists and is not empty 
                # check before you do it again 
                ImageObj = Image(patient, base_path, niftireg_path)

                GroupwiseReg = GroupwiseRegs(patient,no_itterations, base_path, niftireg_path)
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
                
                AtlasAlignment = AtlasRegs(patient, base_path, niftireg_path, atlas_path)

                
                AtlasAlignment.refactor()

                AtlasAlignment.InitAlignment()
                AtlasAlignment.RigidReg()
                AtlasAlignment.AffineReg()
                AtlasAlignment.DefReg()
                AtlasAlignment.Calc_Tatlas()
                

                AtlasAlignment.ResampleImgs(CBCT_relative_timepoints)

                
            except:
                pass
                
                    
'''LongitudinalRegs = DefromableRegs(patient, base_path, niftireg_path)

for CBCT_timepoint in CBCT_relative_timepoints:
    
    LongitudinalRegs.set__CBCTtimepoint(CBCT_timepoint)
    LongitudinalRegs.mask_CBCT()
    #LongitudinalRegs.DefReg()

'''
                