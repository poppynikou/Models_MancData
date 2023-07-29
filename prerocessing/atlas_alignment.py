from classes import *
from functions import * 

structures = ['BRAINSTEM', 'BODY', 'CORD', 'CTVHIGH', 'CTVLOW', 'PAROTIDL', 'PAROTIDR']
base_path = 'T:/Poppy/PatData/test2/'
niftireg_path = 'T:/Poppy/niftireg_executables/'
atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'

patients = os.listdir(base_path)

for patient in patients:
    
    if patient[0:3] == 'HN_':

        AtlasAlignment = AtlasRegs(patient, structures, base_path, niftireg_path, atlas_path)

        AtlasAlignment.refactor()

        AtlasAlignment.InitAlignment()
        AtlasAlignment.RigidReg()
        AtlasAlignment.AffineReg()
        AtlasAlignment.DefReg()
        AtlasAlignment.Calc_Tatlas()

        AtlasAlignment.ResampleImgs()