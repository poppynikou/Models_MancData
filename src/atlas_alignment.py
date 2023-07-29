from classes import *
from functions import * 

base_path = 'T:/Poppy/PatData/test2/'
niftireg_path = 'T:/Poppy/niftireg_executables/'
atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'

patients = os.listdir(base_path)

for patient in patients:


    AtlasAlignment = AtlasRegs(patient, base_path, niftireg_path, atlas_path)

    AtlasAlignment.refactor()

    AtlasAlignment.InitAlignment()
    AtlasAlignment.RigidReg()
    AtlasAlignment.AffineReg()
    AtlasAlignment.DefReg()
    AtlasAlignment.Calc_Tatlas()

    AtlasAlignment.ResampleImgs()