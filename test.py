name = 'BIN_PAROTIDL.nii.gz'
new_name = name

if name.__contains__('PAROTIDL'):
    new_name= new_name.replace('PAROTIDL','LPAROTID')
    
    print(new_name)   