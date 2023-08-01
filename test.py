import nibabel as nib
import numpy as np 

path_to_body_mask = 'T:/Poppy/PatData/batch1/176662567/BIN_BODY.nii'
path_to_mouth_mask = 'T:/Poppy/PatData/batch1/176662567/BIN_MOUTH.nii'

def get_img_objects(img_path):
    
    img_obj = nib.load(img_path)
    img_data = np.array(img_obj.get_fdata())
    img_affine = img_obj.affine
    img_header = img_obj.header

    return img_data, img_affine, img_header


img_data_body, img_affine_body, img_header_body = get_img_objects(path_to_body_mask)
img_data_body_copy = img_data_body.copy()
(x,y,z) = np.shape(img_data_body_copy)

img_data_mouth, img_affine_mouth, img_header_mouth = get_img_objects(path_to_mouth_mask)

img_data_mouth = np.array(img_data_mouth, dtype=np.bool8)
z_slices = np.sum(np.sum(img_data_mouth, axis =0), axis=0)
nonzero_z_slices = np.nonzero(z_slices)

img_data_body_copy[:,:,0:nonzero_z_slices[0][0]] = False
img_data_body_copy[:,:,nonzero_z_slices[0][-1]:z] = False

for index, z_slice in enumerate(nonzero_z_slices[0]):

    y_slices = np.sum(np.squeeze(img_data_mouth[:,:,z_slice]), axis =0)
    nonzero_y_slices = np.nonzero(y_slices)[0][-1]
    img_data_body_copy[:,nonzero_y_slices:y,z_slice] = False
    
NewNiftiObj = nib.Nifti1Image(img_data_body_copy, img_affine_body, img_header_body)
nib.save(NewNiftiObj, 'T:/Poppy/PatData/batch1/176662567/BIN_MOUTH_MASK.nii')
    
    