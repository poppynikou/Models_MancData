# find the top and centre of the skulls of both of the average atlas img
# and the pCT of a new patient
# and use those to perform an initial alignment

import nibabel as nib 
import numpy as np 
import os 
import pandas as pd
from utils import get_image_objects
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

hn_atlas_path = 'T:/Poppy/PatData/average_pCT.nii.gz'
pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/MASKED_rescaled_pCT.nii.gz'

hn_atlas_img, _, hn_atlas_hdr = get_image_objects(hn_atlas_path)
hn_atlas_img = np.array(hn_atlas_img)

srowx_atlas = hn_atlas_hdr['srow_x'][3]
srowy_atlas = hn_atlas_hdr['srow_y'][3]
srowz_atlas = hn_atlas_hdr['srow_z'][3]

print(srowx_atlas)
print(srowy_atlas)
print(srowz_atlas)

pCT_img, _, pCT_hdr = get_image_objects(pCT_hn_3_path)
pCT_img = np.array(pCT_img)

srowx_pCT = pCT_hdr['srow_x'][3]
srowy_pCT = pCT_hdr['srow_y'][3]
srowz_pCT = pCT_hdr['srow_z'][3]

pix_dim = pCT_hdr['pixdim'][1:4]

print(srowx_pCT)
print(srowy_pCT)
print(srowz_pCT)
print(pix_dim)

x_shift = (srowx_atlas - srowx_pCT)/pix_dim[0]
y_shift = (srowy_atlas - srowy_pCT)/pix_dim[1]
z_shift = (srowz_atlas - srowz_pCT)/pix_dim[2]
identity_matrix = np.identity(4)
identity_matrix[0][3] = -x_shift
identity_matrix[1][3] = -y_shift
identity_matrix[2][3] = z_shift


Sform_matrix_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment.txt'
identity_matrix = pd.DataFrame(identity_matrix)
np.savetxt(Sform_matrix_path, identity_matrix, fmt='%d')

img_to_be_updated = pCT_hn_3_path
affine = Sform_matrix_path
updated_img = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_MASKED_rescaled_pCT.nii.gz'

# update the Sform of the cropped image 
command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
os.system(command)