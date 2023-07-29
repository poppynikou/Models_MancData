import numpy as np 
from classes import GroupwiseRegs, MancData, Image
import os
import pandas as pd
from functions import * 

base_path = 'T:/Poppy/PatData/test2/'
niftireg_path = 'T:/Poppy/niftireg_executables/'
no_itterations = 2
# path to the file which contains all patient info
patients_csv_path = 'T:/Poppy/Anonymisation_Key.csv'
patients = os.listdir(base_path)

for patient in patients: 

        # if a certain path exists and is not empty 
        # check before you do it again 

        ImageObj = Image(patient, base_path, niftireg_path)

        GroupwiseReg = GroupwiseRegs(patient,no_itterations, base_path, niftireg_path)
        GroupwiseReg.get_CBCT_relative_timepoints(patients_csv_path)
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











            



