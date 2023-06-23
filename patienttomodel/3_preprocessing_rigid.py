import numpy as np 
import pandas as pd 
import os
from utils import crop_shift_CT

lower_slice_cut = 75
upper_slice_cut = 102
slice_cut = [lower_slice_cut, upper_slice_cut]


CT_path = 'T:/Poppy/PatData/average_pCT.nii.gz'
Sform_matrix_path = 'T:/Poppy/PatData/average_pCT_Sform.txt'
CT_CROPPED_path = 'T:/Poppy/PatData/cropped_average_pCT.nii.gz'
updated_img_path = 'T:/Poppy/PatData/average_pCT_cropped.nii.gz'
crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = False)
os.remove(Sform_matrix_path)
os.remove(CT_CROPPED_path)

lower_slice_cut = 48
upper_slice_cut = 74
slice_cut = [lower_slice_cut, upper_slice_cut]


CT_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT.nii.gz'
Sform_matrix_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT_Sform.txt'
CT_CROPPED_path = 'T:/Poppy/PatData/HN_3/pCT/cropped_InitAlignment_pCT.nii.gz'
updated_img_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT_cropped.nii.gz'
crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = True)
os.remove(Sform_matrix_path)
os.remove(CT_CROPPED_path)