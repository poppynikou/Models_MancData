import nibabel as nib 
import numpy as np 

path_to_CBCT = 'T:/Poppy/PatData/HN_3/CBCT_pCT/CBCT/CBCT_0.nii.gz'

CBCT_obj = nib.load(path_to_CBCT)
CBCT_img = CBCT_obj.get_fdata()
CBCT_affine = CBCT_obj.affine
CBCT_header = CBCT_obj.header

CBCT_img_ = CBCT_img.copy()
CBCT_img_ = np.array(CBCT_img_, dtype = np.float32)

# index at top corner 
masking_HU = CBCT_img_[0,0,0]

CBCT_img_[CBCT_img_ == masking_HU] = np.NaN

CBCT_header.set_data_dtype(np.float32)
NewNiftiObj = nib.Nifti1Image(CBCT_img_, CBCT_affine, CBCT_header)
nib.save(NewNiftiObj, 'T:/Poppy/PatData/HN_3/CBCT_pCT/CBCT/MASKED_CBCT_0.nii.gz')

import nibabel as nib 
import numpy as np 

path_to_CBCT = 'T:/Poppy/PatData/HN_3/CBCT_pCT/CBCT/CBCT_0.nii.gz'

CBCT_obj = nib.load(path_to_CBCT)
CBCT_img = CBCT_obj.get_fdata()
CBCT_affine = CBCT_obj.affine
CBCT_header = CBCT_obj.header

CBCT_img_ = CBCT_img.copy()
CBCT_img_ = np.array(CBCT_img_, dtype = np.float32)

# index at top corner 
masking_HU = CBCT_img_[0,0,0]

CBCT_img_[CBCT_img_ == masking_HU] = np.NaN

CBCT_header.set_data_dtype(np.float32)
NewNiftiObj = nib.Nifti1Image(CBCT_img_, CBCT_affine, CBCT_header)
nib.save(NewNiftiObj, 'T:/Poppy/PatData/HN_3/CBCT_pCT/CBCT/MASKED_CBCT_0.nii.gz')

