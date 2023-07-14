'''
Script to preprocess pCT in this dataset since HUs are offset by -1000
and mask the CT images 
'''

from utils import *
import nibabel as nib 
import numpy as np 


# can loop over this in the future

# offset the HU so that they match the rest of the imaging we have
# and so that they can be aligned using block matching/intensity matching algorithms 
# with the average hn atlas 

pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/pCT.nii.gz'
pCT_img, pCT_affine, pCT_hdr = get_image_objects(pCT_hn_3_path)
pCT_img = np.array(pCT_img) -1024

NewNiftiObj = nib.Nifti1Image(pCT_img, pCT_affine, pCT_hdr)
new_path = 'T:/Poppy/PatData/HN_3/pCT/rescaled_pCT.nii.gz'
nib.save(NewNiftiObj, new_path)



# you can crop the couch bed out of the pCT
# I usually use the contours for this, so can edit accordingly later on 

pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/rescaled_pCT.nii.gz'
img_obj, img_affine, img_header = get_image_objects(pCT_hn_3_path)

img_obj_copy = img_obj.copy()
img_obj_copy = np.array(img_obj_copy, dtype = np.float32)
img_obj_copy[:, 322:512, :] = np.NaN
img_obj_copy[:, 0:87, :] = np.NaN
img_obj_copy[:,:, 128:151] = np.NaN
img_obj_copy[0:150,:, :] = np.NaN
img_obj_copy[370:512,:, :] = np.NaN
img_header.set_data_dtype(np.float32)

NewNiftiObj = nib.Nifti1Image(img_obj_copy, img_affine, img_header)
new_pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/MASKED_rescaled_pCT.nii.gz'
nib.save(NewNiftiObj, new_pCT_hn_3_path)


# flip the z axis by rotating image 180 degrees


# this is how my usual code works 
# but I dont have the couch or the body contours at the moment
'''
CT_img_path = 'CT_20151217.nii.gz'
Couch_mask_path = 'BIN_COUCH.nii.gz'
Body_mask_path = 'BIN_BODY.nii.gz'
mask_path = 'MASK.nii.gz'
masked_CT_path = 'MASKED_CT_20151217.nii.gz'

# creates the mask first 
create_mask(Couch_mask_path, Body_mask_path, mask_path)

# masks the image 
mask_img(CT_img_path, mask_path, masked_CT_path, masking_value = np.NaN)
'''