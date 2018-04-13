#!/usr/bin/env python

# GIMP Python-fu plugin to crop and resize multiple BPs as part of the CSP Standardization project
# Feedback to tryptech#8049 on Discord

from gimpfu import *
import os

def crop_csp_process(file_inpath, file_outpath, file_mask, hd_resize) :
	
	files =[]
	if os.path.isdir(file_inpath) == True:
		files = [f for f in os.listdir(file_inpath) if os.path.isfile(os.path.join(file_inpath,f))]
	for element in files:
		filename = os.path.splitext(element)[0]
		
		# Get image location
		image = pdb.file_png_load(os.path.join(file_inpath,element),element)
		
		# Add mask to new layer over image
		layer_mask = pdb.gimp_file_load_layer(image,file_mask)
		pdb.gimp_image_insert_layer(image,layer_mask,None,0)
		
		# Mask layer alpha to selection
		pdb.gimp_image_select_item(image,2,pdb.gimp_image_get_active_layer(image))
		pdb.gimp_image_remove_layer(image,layer_mask)
		
		# Invert Selection
		pdb.gimp_selection_invert(image)
		
		# Crop to selection
		dimensions = pdb.gimp_selection_bounds(image)
		pdb.gimp_image_crop(image,dimensions[3]-dimensions[1],dimensions[4]-dimensions[2],dimensions[1],dimensions[2])
		
		# Resize and output CSPs

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
	"python-fu-BATCH-BP-CROPPER",
	"Crops images for BPs (Make sure mask matches image dimensions). Results go to user-defined folder.",
	"Using a user-defined mask, crops all images in a user-defined folder to a certain size, and offers resize options. The final result is then saved with the appropriate suffix to a user-defined folder",
	"tryptech",
	"tryptech",
	"2017",
	"<Toolbox>/Tools/BP Cropper (Batch)",
	"",
	[
		(PF_DIRNAME, "file_inpath", "Input Image Folder", "/tmp"),
		(PF_DIRNAME, "file_outpath", "Output Image Folder", "/tmp"),
		(PF_FILE, "file_mask", "BP Crop File", None),
		(PF_TOGGLE, "hd_resize", "Include HD assets: ", 1)
	],
	[],
	crop_csp_process
)
	
main()