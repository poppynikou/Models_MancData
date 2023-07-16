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



