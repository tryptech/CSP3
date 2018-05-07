#!/usr/bin/env python

# GIMP Python-fu plugin to crop and resize BPs as part of the CSP Standardization project
# Feedback to tryptech#8049 on Discord

from gimpfu import *
import os

def crop_csp_process(file_input, file_mask, hd_resize) :

	filename = os.path.splitext(os.path.split(file_input)[1])[0]
	filepath = os.path.split(file_input)[0]

# Get image location
	image = pdb.file_png_load(file_input,os.path.basename(file_input))
# Open image
	display = pdb.gimp_display_new(image);
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
# Resize image
	reWidth = 48
	reHeight = 56
	if hd_resize == 1:
		reWidth = 144
		reHeight = 168
	pdb.gimp_image_scale(image,reWidth,reHeight)
# Output image
	suffix = "_BP.png"
	if hd_resize == 1:
		suffix = "_BP_HD.png"
	pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(filepath,filename + suffix), filename + suffix)
	pdb.gimp_display_delete(display);
	return

register(
	"python-fu-BP-CROPPER",
	"Crops images for BPs (Make sure mask matches image dimensions). Results go to the BP image folder.",
	"Using a user-defined mask, crops a user-defined image to a certain size, and offers resize options. The final result is then saved with the appropriate suffix to the same folder as the source image.",
	"tryptech",
	"tryptech",
	"2017",
	"<Toolbox>/Tools/BP Cropper",
	"",
	[
		(PF_FILE, "file_input", "BP Image File", None),
		(PF_FILE, "file_mask", "BP Crop File", None),
		(PF_RADIO, "hd_resize", "Set Resize Scale: ", 0,
			(
				("SD (48x56)", 0),
				("HD (144x168)", 1)
			)
		)
	],
	[],
	crop_csp_process
)
	
main()
