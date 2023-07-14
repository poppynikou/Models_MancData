import numpy as np 
import nibabel as nib 
import os 
from Patient_Info_Functions import * 
from natsort import natsorted

def calc_average_image(imgs_path, imgs_prefix, avg_path):
    
    '''
    This function calculates the average image, ignoring nan voxels.
    The average is only calculated within the mask of the body within the CT.

    results_folder: the path where the results are saved
    j: the ith +1 itteration which you are on 
    '''

    imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
    img_obj, _, _ = get_image_objects(imgs[0])
    img_shape = np.shape(np.array(img_obj))
    del(img_obj)
    del(_)
    # create an array of nans for storage
    Nan_map = np.empty(shape=(img_shape[0],img_shape[1],img_shape[2],len(imgs)))
    del(img_shape)

    for index in np.arange(0,len(imgs)):
        
        # mask each image of the body
        # and replace the rest of the image with nans
        # then average over all patients using reg_average

        # define img and mask path 
        img_path = imgs[index]

        # imports the data 
        img = nib.load(img_path)
        img_obj = img.get_fdata().copy()

        #store
        Nan_map[:,:,:,index] = img_obj

    # calculate the average image, ignoring the nans
    Masked_Average = np.nanmean(Nan_map, axis = 3)
    Average = Masked_Average.copy()

    del(Nan_map)  

    # save 
    img_hdr = img.header
    img_affine = img.affine
    Avg_Niftiobj = nib.Nifti1Image(Average, img_affine, img_hdr)
    nib.save(Avg_Niftiobj, avg_path)

def calc_average_affine(path, prefix, results_path):

    '''
    path = location in which the affine matrixes to average are stored
    prefix = string of which the affine matrixes are storaged start with 
    results_path = where you want the average affine matrix to be stored 
    '''

    reg_average = 'T:/Poppy/niftireg_executables/reg_average.exe'

    Affine_Matrixes = natsorted([path + '/' + file for file in os.listdir(path) if (file.startswith(prefix) & file.endswith('txt'))])
    command = reg_average + ' ' + results_path + ' -avg ' 
    for i in np.arange(0,len(Affine_Matrixes)):

        command = command + Affine_Matrixes[i] + ' '

    os.system(command)


def calc_inv_affine(ref_img, affine, inv_affine):
    reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

    command = reg_transform + ' -ref ' + ref_img + ' -invAff ' + affine + ' ' +  inv_affine
    os.system(command)

def rigid_registration_to_ref(original_imgs_path, imgs_prefix, results_path, groupwisetarget_img, CBCTs):

    reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
    
    original_imgs = natsorted([original_imgs_path + '/' + file for file in os.listdir(original_imgs_path) if file.startswith(imgs_prefix)])
  
    # register each of the CBCTs to the reference 
    for rigid_reg in np.arange(0, len(original_imgs)):

        ref_img = groupwisetarget_img
        float_img = original_imgs[rigid_reg]
        transformation = results_path + '/affine_' + str(CBCTs[rigid_reg]) + '.txt'
        resampled_img = results_path + '/affine_CBCT_' + str(CBCTs[rigid_reg]) + '.nii.gz'

        command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img + ' -rigOnly -omp 12' 
        os.system(command)

        os.remove(resampled_img)
        
def affine_composition_to_ref(ref_img, ref_affine, path_to_affines, affine_prefix, path_to_composed_affines, CBCTs):
   
    reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
    affines = natsorted([path_to_affines + '/' + file for file in os.listdir(path_to_affines) if (file.startswith(affine_prefix) & file.endswith('txt'))])

    for composition in np.arange(0, len(affines)):

        # repeat using text files
        affine = affines[composition]
        composed_affine = path_to_composed_affines + '/comp_affine_' + str(CBCTs[composition]) + '.txt'

        command = reg_transform +  ' -ref ' + ref_img + ' -comp ' + ref_affine + ' ' + affine + ' ' + composed_affine
        os.system(command)
        
        os.remove(affine)


def resampled_imgs_with_transformations(ref_img, imgs_path, imgs_prefix, transformation_path, transformation_prefix, results_path, CBCTs):
    
    reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'

    '''
    resample a group of images given in the imgs_path with a group of transformations given in transformation_path
    '''
    CBCT_imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
    transformations  = natsorted([transformation_path + '/' + file for file in os.listdir(transformation_path) if (file.startswith(transformation_prefix) & file.endswith('.txt'))])

    
    for img in np.arange(0, len(CBCT_imgs)):
        
        float_img = CBCT_imgs[img]
        resampled_img = results_path + '/CBCT_' + str(CBCTs[img]) + '.nii.gz'
        transformation = transformations[img]
        command = reg_resample + ' -ref ' + ref_img +  ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -omp 10'
        os.system(command)


def upd_Sform_with_transformations(ref_img, imgs_path, imgs_prefix, transformation_path, transformation_prefix, results_path, CBCTs):

        reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

        '''
        resample a group of images given in the imgs_path with a group of transformations given in transformation_path
        '''
        CBCT_imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
        transformations  = natsorted([transformation_path + '/' + file for file in os.listdir(transformation_path) if (file.startswith(transformation_prefix) & file.endswith('.txt'))])
        print(CBCT_imgs)
        print(transformations)
        
        for img in np.arange(0, len(CBCT_imgs)):

            img_to_update = CBCT_imgs[img]
            updated_img = results_path + '/CBCT_' + str(CBCTs[img]) + '.nii.gz'
            transformation = transformations[img]
            command = reg_transform + ' -updSform ' + img_to_update + ' ' + transformation + ' ' + updated_img
            os.system(command) 



import numpy as np 
import nibabel as nib 
import os 
from Patient_Info_Functions import * 
from natsort import natsorted

def calc_average_image(imgs_path, imgs_prefix, avg_path):
    
    '''
    This function calculates the average image, ignoring nan voxels.
    The average is only calculated within the mask of the body within the CT.

    results_folder: the path where the results are saved
    j: the ith +1 itteration which you are on 
    '''

    imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
    img_obj, _, _ = get_image_objects(imgs[0])
    img_shape = np.shape(np.array(img_obj))
    del(img_obj)
    del(_)
    # create an array of nans for storage
    Nan_map = np.empty(shape=(img_shape[0],img_shape[1],img_shape[2],len(imgs)))
    del(img_shape)

    for index in np.arange(0,len(imgs)):
        
        # mask each image of the body
        # and replace the rest of the image with nans
        # then average over all patients using reg_average

        # define img and mask path 
        img_path = imgs[index]

        # imports the data 
        img = nib.load(img_path)
        img_obj = img.get_fdata().copy()

        #store
        Nan_map[:,:,:,index] = img_obj

    # calculate the average image, ignoring the nans
    Masked_Average = np.nanmean(Nan_map, axis = 3)
    Average = Masked_Average.copy()

    del(Nan_map)  

    # save 
    img_hdr = img.header
    img_affine = img.affine
    Avg_Niftiobj = nib.Nifti1Image(Average, img_affine, img_hdr)
    nib.save(Avg_Niftiobj, avg_path)

def calc_average_affine(path, prefix, results_path):

    '''
    path = location in which the affine matrixes to average are stored
    prefix = string of which the affine matrixes are storaged start with 
    results_path = where you want the average affine matrix to be stored 
    '''

    reg_average = 'T:/Poppy/niftireg_executables/reg_average.exe'

    Affine_Matrixes = natsorted([path + '/' + file for file in os.listdir(path) if (file.startswith(prefix) & file.endswith('txt'))])
    command = reg_average + ' ' + results_path + ' -avg ' 
    for i in np.arange(0,len(Affine_Matrixes)):

        command = command + Affine_Matrixes[i] + ' '

    os.system(command)


def calc_inv_affine(ref_img, affine, inv_affine):
    reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

    command = reg_transform + ' -ref ' + ref_img + ' -invAff ' + affine + ' ' +  inv_affine
    os.system(command)

def rigid_registration_to_ref(original_imgs_path, imgs_prefix, results_path, groupwisetarget_img, CBCTs):

    reg_aladin = 'T:/Poppy/niftireg_executables/reg_aladin.exe'
    
    original_imgs = natsorted([original_imgs_path + '/' + file for file in os.listdir(original_imgs_path) if file.startswith(imgs_prefix)])
  
    # register each of the CBCTs to the reference 
    for rigid_reg in np.arange(0, len(original_imgs)):

        ref_img = groupwisetarget_img
        float_img = original_imgs[rigid_reg]
        transformation = results_path + '/affine_' + str(CBCTs[rigid_reg]) + '.txt'
        resampled_img = results_path + '/affine_CBCT_' + str(CBCTs[rigid_reg]) + '.nii.gz'

        command = reg_aladin + ' -ref ' + ref_img + ' -flo ' + float_img + ' -aff ' + transformation + ' -res ' + resampled_img + ' -rigOnly -omp 12' 
        os.system(command)

        os.remove(resampled_img)
        
def affine_composition_to_ref(ref_img, ref_affine, path_to_affines, affine_prefix, path_to_composed_affines, CBCTs):
   
    reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'
    affines = natsorted([path_to_affines + '/' + file for file in os.listdir(path_to_affines) if (file.startswith(affine_prefix) & file.endswith('txt'))])

    for composition in np.arange(0, len(affines)):

        # repeat using text files
        affine = affines[composition]
        composed_affine = path_to_composed_affines + '/comp_affine_' + str(CBCTs[composition]) + '.txt'

        command = reg_transform +  ' -ref ' + ref_img + ' -comp ' + ref_affine + ' ' + affine + ' ' + composed_affine
        os.system(command)
        
        os.remove(affine)


def resampled_imgs_with_transformations(ref_img, imgs_path, imgs_prefix, transformation_path, transformation_prefix, results_path, CBCTs):
    
    reg_resample = 'T:/Poppy/niftireg_executables/reg_resample.exe'

    '''
    resample a group of images given in the imgs_path with a group of transformations given in transformation_path
    '''
    CBCT_imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
    transformations  = natsorted([transformation_path + '/' + file for file in os.listdir(transformation_path) if (file.startswith(transformation_prefix) & file.endswith('.txt'))])

    
    for img in np.arange(0, len(CBCT_imgs)):
        
        float_img = CBCT_imgs[img]
        resampled_img = results_path + '/CBCT_' + str(CBCTs[img]) + '.nii.gz'
        transformation = transformations[img]
        command = reg_resample + ' -ref ' + ref_img +  ' -flo ' + float_img + ' -trans ' + transformation + ' -res ' + resampled_img + ' -inter 3 -omp 10'
        os.system(command)


def upd_Sform_with_transformations(ref_img, imgs_path, imgs_prefix, transformation_path, transformation_prefix, results_path, CBCTs):

        reg_transform = 'T:/Poppy/niftireg_executables/reg_transform.exe'

        '''
        resample a group of images given in the imgs_path with a group of transformations given in transformation_path
        '''
        CBCT_imgs = natsorted([imgs_path + '/' + file for file in os.listdir(imgs_path) if file.startswith(imgs_prefix)])
        transformations  = natsorted([transformation_path + '/' + file for file in os.listdir(transformation_path) if (file.startswith(transformation_prefix) & file.endswith('.txt'))])
        print(CBCT_imgs)
        print(transformations)
        
        for img in np.arange(0, len(CBCT_imgs)):

            img_to_update = CBCT_imgs[img]
            updated_img = results_path + '/CBCT_' + str(CBCTs[img]) + '.nii.gz'
            transformation = transformations[img]
            command = reg_transform + ' -updSform ' + img_to_update + ' ' + transformation + ' ' + updated_img
            os.system(command) 



