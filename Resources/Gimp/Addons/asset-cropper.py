#!/usr/bin/env python

# GIMP Python-fu plugin to crop and resize multiple BPs and CSPs as part of the CSP Standardization project
# Feedback to tryptech#8049 on Discord

from gimpfu import *
import os

def crop_asset_process(file_inpath, file_outpath, file_bp_mask, file_csp_mask, hd_resize) :
	
	files =[]
	if os.path.isdir(file_inpath) == True:
		files = [f for f in os.listdir(file_inpath) if os.path.isfile(os.path.join(file_inpath,f))]
	for element in files:
		filename = os.path.splitext(element)[0]
		
		# Get image location
		image = pdb.file_png_load(os.path.join(file_inpath,element),element)
		
		# Add mask to new layer over image
		layer_csp_mask = pdb.gimp_file_load_layer(image,file_csp_mask)
		pdb.gimp_image_insert_layer(image,layer_csp_mask,None,0)
		
		# Mask layer alpha to selection
		pdb.gimp_image_select_item(image,2,pdb.gimp_image_get_active_layer(image))
		pdb.gimp_image_remove_layer(image,layer_csp_mask)
		
		# Invert Selection
		pdb.gimp_selection_invert(image)
		
		# Crop to selection
		dimensions = pdb.gimp_selection_bounds(image)
		pdb.gimp_image_crop(image,dimensions[3]-dimensions[1],dimensions[4]-dimensions[2],dimensions[1],dimensions[2])
		
		# Resize and output CSPs

		if hd_resize == True:
			reWidth = 384
			reHeight = 480
			pdb.gimp_image_scale(image,reWidth,reHeight)
			suffix = "_CSP_HD.png"
			pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(file_outpath,filename + suffix), filename + suffix)

		reWidth = 128
		reHeight = 160
		pdb.gimp_image_scale(image,reWidth,reHeight)
		suffix = "_CSP.png"
		pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(file_outpath,filename + suffix), filename + suffix)
		pdb.gimp_image_delete(image)

		#Repeaat for BP
		image = pdb.file_png_load(os.path.join(file_inpath,element),element)
		layer_bp_mask = pdb.gimp_file_load_layer(image,file_bp_mask)
		pdb.gimp_image_insert_layer(image,layer_bp_mask,None,0)
		pdb.gimp_selection_layer_alpha(layer_bp_mask)
		pdb.gimp_image_remove_layer(image,layer_bp_mask)
		pdb.gimp_selection_invert(image)
		dimensions = pdb.gimp_selection_bounds(image)
		pdb.gimp_image_crop(image,dimensions[3]-dimensions[1],dimensions[4]-dimensions[2],dimensions[1],dimensions[2])
		if hd_resize == True:
			reWidth = 144
			reHeight = 168
			pdb.gimp_image_scale(image,reWidth,reHeight)
			suffix = "_BP_HD.png"
			pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(file_outpath,filename + suffix), filename + suffix)
		reWidth = 48
		reHeight = 56
		pdb.gimp_image_scale(image,reWidth,reHeight)
		suffix = "_BP.png"
		pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(file_outpath,filename + suffix), filename + suffix)
		pdb.gimp_image_delete(image)
	return

register(
	"python-fu-ASSET-CROPPER",
	"Crops images for BPs and CSPs (Make sure mask matches image dimensions). Results go to user-defined folder.",
	"Using a user-defined mask, crops all images in a user-defined folder to a certain size, and offers resize options. The final result is then saved with the appropriate suffix to a user-defined folder",
	"tryptech",
	"tryptech",
	"2017",
	"<Toolbox>/Tools/Asset Cropper",
	"",
	[
		(PF_DIRNAME, "file_inpath", "Input Image Folder", "/tmp"),
		(PF_DIRNAME, "file_outpath", "Output Image Folder", "/tmp"),
		(PF_FILE, "file_bp_mask", "BP Crop File", None),
		(PF_FILE, "file_csp_mask", "CSP Crop File", None),
		(PF_TOGGLE, "hd_resize", "Include HD assets: ", 1)
	],
	[],
	crop_asset_process
)
	
main()