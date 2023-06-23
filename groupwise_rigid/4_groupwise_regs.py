import os
import shutil 
from Patient_Info_Functions import *
from Groupwise_Rigid_Functions import * 

no_iterations = 2
patients = [3]
base_path = 'T:/Poppy/PatData'
# first you need copy all the original CBCT images which you want to use
# and put them into a folder 'affine_0' to start off with 

for patient in patients:

    CBCTs = get_time_points(base_path, patient)
    print(CBCTs)
    results_folder = base_path + '/HN_'+str(patient)+'/CBCT_GROUPWISE'
    initial_folder = results_folder + '/affine_0'

    # for each iteration in the number of itterations of the groupwise 
    for iteration in np.arange(0,no_iterations):

        original_imgs_path = results_folder + '/affine_' + str(iteration)
        original_imgs = natsorted([original_imgs_path + '/' + file for file in os.listdir(original_imgs_path) if file.startswith("CBCT_")])

        result_path = results_folder + '/affine_' + str(iteration+1)
        if not os.path.exists(result_path):
            os.mkdir(result_path)

        # define the target/ reference img for that iteration 
        if iteration == 0:
            groupwisetarget_img = original_imgs[0]
        else:
            groupwisetarget_img = original_imgs_path + '/average_CBCT.nii.gz'

        # rigidly register each CBCT to the groupwise reference 
        rigid_registration_to_ref(original_imgs_path, 'CBCT', result_path, groupwisetarget_img, CBCTs)
        
        # calculate average affine
        average_affine_path = result_path + '/average_affine.txt'
        calc_average_affine(result_path, 'affine', average_affine_path)
        
        # calculate inverse average affine
        average_inv_affine_path = result_path + '/inv_average_affine.txt'
        calc_inv_affine(groupwisetarget_img, average_affine_path, average_inv_affine_path)
    
        # compose list of affines with ref affine
        affine_composition_to_ref(groupwisetarget_img, average_inv_affine_path, result_path, 'affine_', result_path, CBCTs)

        #resample list of images with a single transformation
        resampled_imgs_with_transformations(groupwisetarget_img, original_imgs_path, 'CBCT', result_path, 'comp_affine_', result_path, CBCTs)

        # calculate the average image 
        avg_path = result_path + '/average_CBCT.nii.gz'
        calc_average_image(result_path, 'CBCT_',  avg_path)
        
        
