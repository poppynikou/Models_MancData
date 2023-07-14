local outfolder = [[T:\Poppy\PatData\test\]]
local infolder = [[T:\HnN\CBCTPacks\]]

patid = '155054082'
wm = loadpackdata(infolder .. patid .. '.pack')

delineation = wm.Scan[1]:burn(wm.Delineation[13]);
delineation.Data:toshort();
structure_name = 'CORD'
delineation:write_nifty(outfolder .. patid..[[\BIN_]].. structure_name ..'.nii',false)