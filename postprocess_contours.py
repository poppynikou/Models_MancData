#contours need rotating by 90 degrees in the xy direction 
from flip_utils import *
import numpy as np 

img_shape = (512,512,155)

T1 = create_traslational_affine(512/2, 512/2, 144/2)
T2 = create_rotation_affine(1, -np.pi)
T3 = create_traslational_affine(-512/2, -512/2, -144/2)

T_Comp = T1@T2@T3

np.savetxt('test.txt', T_Comp)

img = 'T:/Poppy/PatData/test/155054082/BIN_BODY.nii'
resampled_img = 'T:/Poppy/PatData/test/155054082/rotated_BIN_BODY.nii'
resample_binary(img, img, 'test.txt', resampled_img)
