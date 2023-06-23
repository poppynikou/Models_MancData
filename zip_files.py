import os 
import nibabel as nib


def get_nifti_obj(path):

    niftiobj = nib.load(path)
    nifti_img = niftiobj.get_fdata()
    nifti_header = niftiobj.header
    nifti_affine = niftiobj.affine

    return nifti_img, nifti_header, nifti_affine

#\ the path which we want to search 
root = 'T:/Poppy/PatData/'

# find all files within a directory which are nifti files
for path, subdirs, files in os.walk(root):
    
    for name in files:

        file_path = os.path.join(path, name)
      
        if name[-4:] == '.nii':

           
            # read in nifti data
            nifti_img, nifti_header, nifti_affine = get_nifti_obj(file_path)

            # define new name
            zipped_path = file_path + '.gz'

            # resave
            NewNiftiObj = nib.Nifti1Image(nifti_img, nifti_affine, nifti_header)
            nib.save(NewNiftiObj, zipped_path)

            # remove old .nii obj 
            os.remove(file_path)

