import os 
import nibabel as nib 

CBCT = 'T:/Poppy/PatData/test/HN_0/pCT/model_space/AFFINE_pCT.nii.gz'

CBCT_obj = nib.load(CBCT)

print(CBCT_obj.get_fdata()[0,0,0])
