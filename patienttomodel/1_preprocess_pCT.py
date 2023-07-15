import numpy as np 
from utils import * 

patients = np.arange(0,10)

for patient in patients:

    # masks the image 
    mask_img(CT_img_path, mask_path, masked_CT_path, masking_value = np.NaN)
