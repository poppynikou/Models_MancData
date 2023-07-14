
CT_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT.nii.gz'
Sform_matrix_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT_Sform.txt'
CT_CROPPED_path = 'T:/Poppy/PatData/HN_3/pCT/cropped_InitAlignment_pCT.nii.gz'
updated_img_path = 'T:/Poppy/PatData/HN_3/pCT/InitAlignment_pCT_cropped.nii.gz'
crop_shift_CT(CT_path, Sform_matrix_path, CT_CROPPED_path, updated_img_path, slice_cut = slice_cut, Manc = True)
os.remove(Sform_matrix_path)
os.remove(CT_CROPPED_path)