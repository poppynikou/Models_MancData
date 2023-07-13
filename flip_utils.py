import nibabel as nib
import numpy as np 
import os 

def get_metadata(nifti_path):

    nifti_obj = nib.load(nifti_path)
    nifti_img = nifti_obj.get_fdata()
    nifti_affine = nifti_obj.affine
    nifti_header = nifti_obj.header

    return nifti_img, nifti_affine, nifti_header


def create_traslational_affine(x_shift, y_shift, z_shift):

    T = np.matrix([[1,0,0,x_shift], [0,1,0,y_shift], [0,0,1,z_shift], [0,0,0,1]])

    return T

def create_translation_affine(axis, angle):

    # angle must be in radians
    # axis = 0 is x rotation
    # axis = 1 is y rotation 
    # axis = 2 is z rotation 
    cos = np.cos(angle)
    sin = np.sin(angle)
    if axis == 0:
        T = np.matrix([[1,0,0,0], [0, cos, -sin, 0], [0,sin, cos, 0], [0,0,0,1]])
    elif axis ==1:
        T = np.matrix([[cos,0,sin,0],[0,1,0,0], [-sin, 0,cos,0], [0,0,0,1]])
    elif axis ==2:
        T= np.matrix([[cos,-sin,0,0],[sin,cos,0,0],[0,0,1,0], [0,0,0,1]])

    return T


def resample_CT(ref_img, float_img, transformation, resampled_img):

    reg_resample = ' C:/Users/poppy/Documents/Nifty/niftyreg_install/bin/reg_resample.exe'

    command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -pad -1000 -omp 12'
    os.system(command)