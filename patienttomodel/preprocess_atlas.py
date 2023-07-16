from utils import get_image_objects
import numpy as np 
import nibabel as nib 
import os
from utils import * 

pCT_hn_3_path = 'T:/Poppy/PatData/average_pCT.nii.gz'
img_obj, img_affine, img_header = get_image_objects(pCT_hn_3_path)

img_obj_copy = img_obj.copy()
img_obj_copy = np.array(img_obj_copy, dtype = np.float32)
img_obj_copy[:, 350:512, :] = np.NaN
img_obj_copy[:, 0:118, :] = np.NaN
img_obj_copy[:,:, 0:24] = np.NaN
img_obj_copy[0:189,:, :] = np.NaN
img_obj_copy[330:512,:, :] = np.NaN
img_header.set_data_dtype(np.float32)

NewNiftiObj = nib.Nifti1Image(img_obj_copy, img_affine, img_header)
new_pCT_hn_3_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
nib.save(NewNiftiObj, new_pCT_hn_3_path)

CT_path = new_pCT_hn_3_path
Sform_matrix_path = 'T:/Poppy/PatData/Sform.txt'
CT_CROPPED_path = 'T:/Poppy/PatData/cropped_MASKED_average_pCT.nii.gz'
updated_img_path = 'T:/Poppy/PatData/cropped_MASKED_average_pCT.nii.gz'
slice_cut = [75,101]
crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = False)
os.remove(Sform_matrix_path)


