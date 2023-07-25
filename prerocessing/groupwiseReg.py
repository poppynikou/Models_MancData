import numpy as np 
from classes import GroupwiseRegs, MancData, Image
import os
import pandas as pd
from functions import * 

structures = []
base_path = ''
niftireg_path = ''
no_itterations = 2

# create instance of manchester data class 
Data = MancData(structures, base_path)
Data.set_niftireg_path(niftireg_path)

patients = os.listdir(base_path)

for patient in patients:

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











        



