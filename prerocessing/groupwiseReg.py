import numpy as np 
from classes import GroupwiseRegs, MancData, Image
import os
import pandas as pd
from functions import * 

structures = ['BRAINSTEM', 'BODY', 'CORD', 'CTVHIGH', 'CTVLOW', 'PAROTIDL', 'PAROTIDR']
base_path = 'T:/Poppy/PatData/test2/'
niftireg_path = 'T:/Poppy/niftireg_executables/'
no_itterations = 2

# create instance of manchester data class 
Data = MancData(structures, base_path, niftireg_path)

patients = os.listdir(base_path)

for patient in patients:
    if patient[0:3] == 'HN_':

        # if a certain path exists and is not empty 
        # check before you do it again 

        ImageObj = Image(patient)

        GroupwiseReg = GroupwiseRegs(patient,no_itterations)
        GroupwiseReg.get_CBCT_relative_timepoints()
        GroupwiseReg.refactor()

        for itteration in np.arange(0, no_itterations):

            GroupwiseReg.__init__itteration(itteration)
            GroupwiseReg.rigidGroupReg()
            GroupwiseReg.avgAffine()
            GroupwiseReg.invAffine()
            GroupwiseReg.compAffine()
            GroupwiseReg.resampleImages()
            GroupwiseReg.avgImage()

        GroupwiseReg.UpdateGroupSform()
        GroupwiseReg.rigidpCTReg()
        GroupwiseReg.UpdateSform()











            



