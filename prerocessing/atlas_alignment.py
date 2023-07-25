from classes import *
from functions import * 

structures = []
base_path = ''
niftireg_path = ''
atlas_path = ''

Data = MancData(structures, base_path)
Data.set_niftireg_path()
Data.set_atlas_path()

patients = os.listdir(base_path)

for patient in patients:

    AtlasAlignment = AtlasRegs(patient)

    AtlasAlignment.refactor()

    AtlasAlignment.InitAlignment()
    AtlasAlignment.RigidReg()
    AtlasAlignment.AffineReg()
    AtlasAlignment.DefReg()
    AtlasAlignment.Calc_Tatlas()

    AtlasAlignment.ResampleImgs()