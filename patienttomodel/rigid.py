# first align a patient rigidly 

import os

hn_atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/InitAlignment_MASKED_rescaled_pCT.nii.gz'


reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

ref_img = hn_atlas_path
float_img = pCT_hn_3_path
transformation = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/atlas_rigid.txt'
resampled_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/resampled_pCT_atlas_rigid.nii.gz'
command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img + ' -rigOnly -omp 12' 
os.system(command)

# delete resampled img, and update the Sform 
os.remove(resampled_img)
# update the Sform of the cropped image 
img_to_be_updated = pCT_hn_3_path
affine = transformation
updated_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/RIGID_pCT.nii.gz'
command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
os.system(command)


ref_img = hn_atlas_path
float_img = updated_img
transformation = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/atlas_affine.txt'
resampled_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/resampled_pCT_atlas_affine.nii.gz'
command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img +  ' -omp 12' 
os.system(command)

# delete resampled img, and update the Sform 
os.remove(resampled_img)

# update the Sform of the cropped image 
img_to_be_updated = updated_img
affine = transformation
updated_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/AFFINE_pCT.nii.gz'
command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
os.system(command)
# first align a patient rigidly 

import os

hn_atlas_path = 'T:/Poppy/PatData/MASKED_average_pCT.nii.gz'
pCT_hn_3_path = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/InitAlignment_MASKED_rescaled_pCT.nii.gz'


reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

ref_img = hn_atlas_path
float_img = pCT_hn_3_path
transformation = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/atlas_rigid.txt'
resampled_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/resampled_pCT_atlas_rigid.nii.gz'
command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img + ' -rigOnly -omp 12' 
os.system(command)

# delete resampled img, and update the Sform 
os.remove(resampled_img)
# update the Sform of the cropped image 
img_to_be_updated = pCT_hn_3_path
affine = transformation
updated_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/RIGID_pCT.nii.gz'
command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
os.system(command)


ref_img = hn_atlas_path
float_img = updated_img
transformation = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/atlas_affine.txt'
resampled_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/resampled_pCT_atlas_affine.nii.gz'
command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img +  ' -omp 12' 
os.system(command)

# delete resampled img, and update the Sform 
os.remove(resampled_img)

# update the Sform of the cropped image 
img_to_be_updated = updated_img
affine = transformation
updated_img = 'T:/Poppy/PatData/HN_3/pCT/UCLHAtlas_Alignment/AFFINE_pCT.nii.gz'
command = reg_transform + ' -ref ' + img_to_be_updated + ' -updSform ' + img_to_be_updated + ' ' + affine + ' ' + updated_img
os.system(command)
