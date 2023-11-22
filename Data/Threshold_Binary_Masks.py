'''
Binary masks from Eliana come in the form of 0, 100 not 0,1. 
Need to fix this. 
'''

import os 
import nibabel as nib 
import numpy as np 
from copy import deepcopy 

base_path = 'D:/CHRISTIE_HN/Masks/Masks/'
patients = os.listdir(base_path)


def get_img_objects(img_path):
        
        img_obj = nib.load(img_path)
        img_data = np.array(img_obj.get_fdata(), dtype=np.int16)
        img_affine = img_obj.affine
        img_header = img_obj.header

        return img_data, img_affine, img_header

for patient in patients:
    print(patient)

    path = str(base_path) +str(patient)+'/pCT/'

    structures = os.listdir(path)

    for structure in structures:
        print(structure)

        structure_path = path + str(structure) 
        
        if os.path.exists(path):


            img_data, img_affine, img_header = get_img_objects(structure_path)
            new_img_data = deepcopy(img_data)

            print(np.sum([new_img_data == 99]))

            new_img_data[new_img_data == 99] = 1
            print(np.sum([new_img_data == 99]))


            img_header.set_data_dtype(np.int16)


            NewNiftiObj = nib.Nifti1Image(new_img_data, img_affine, img_header)
            nib.save(NewNiftiObj, structure_path)



