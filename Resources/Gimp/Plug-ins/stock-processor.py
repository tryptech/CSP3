#!/usr/bin/env python

# GIMP Python-fu plugin to make stock icons as part of the CSP Standardization project
# Feedback to tryptech#8049 on Discord

from gimpfu import *
import os

def crop_csp_process(file_input, file_mask, file_crop, hd_resize) :

	filename = os.path.splitext(os.path.split(file_input)[1])[0]
	filepath = os.path.split(file_input)[0]

# Get image location
	image = pdb.file_png_load(file_input,os.path.basename(file_input))
# Open image
	display = pdb.gimp_display_new(image)
# Add mask to new layer over image
	if (bool(file_mask and file_mask.strip())):
		layer_mask = pdb.gimp_file_load_layer(image,file_mask)
	else:
		layer_mask = pdb.gimp_file_load_layer(image,file_crop)
	pdb.gimp_image_insert_layer(image,layer_mask,None,0)
# Mask layer alpha to selection
	pdb.gimp_image_select_item(image,2,pdb.gimp_image_get_active_layer(image))
	pdb.gimp_image_remove_layer(image,layer_mask)
# Apply mask
	pdb.gimp_edit_clear(pdb.gimp_image_get_active_layer(image))
# Add crop to new layer over image
	layer_crop = pdb.gimp_file_load_layer(image,file_crop)
	pdb.gimp_image_insert_layer(image,layer_crop,None,0)
# Mask layer alpha to selection
	pdb.gimp_image_select_item(image,2,pdb.gimp_image_get_active_layer(image))
	pdb.gimp_image_remove_layer(image,layer_crop)
# Invert Selection
	pdb.gimp_selection_invert(image)
# Crop to selection
	dimensions = pdb.gimp_selection_bounds(image)
	pdb.gimp_image_crop(image,dimensions[3]-dimensions[1],dimensions[4]-dimensions[2],dimensions[1],dimensions[2])
# Resize image
	reSize = 28
	if (hd_resize == 1):
	    reSize = 224
	pdb.gimp_image_scale(image,reSize,reSize)
# Add padding
	newSize = 32
	if (hd_resize == 1):
		newSize = 256
	off = round((newSize-reSize)/2)
	pdb.gimp_image_resize(image,newSize,newSize,off,off)
# Clear Selection
	pdb.gimp_selection_none(image)
# Resize layer to new bounds
	pdb.gimp_layer_resize_to_image_size(pdb.gimp_image_get_active_layer(image))
# Reselect image
	pdb.gimp_image_select_item(image,2,pdb.gimp_image_get_active_layer(image))
# Add layer for stroke
	stroke = pdb.gimp_layer_new(image,newSize,newSize,1,"stroke",100,0)
	pdb.gimp_image_insert_layer(image,stroke,None,1)
# Create stroke and fill
	strokeWidth = 1.3
	if (hd_resize == 1):
		strokeWidth = 8
	pdb.gimp_context_set_default_colors()
	pdb.gimp_edit_fill(stroke,0)
	pdb.gimp_context_set_brush("2. Hardness 100")
	pdb.gimp_context_set_brush_size(strokeWidth)
	pdb.gimp_context_set_opacity(100)
	pdb.gimp_edit_stroke(pdb.gimp_image_get_active_layer(image))
	pdb.gimp_selection_none(image)
	pdb.gimp_item_transform_2d(stroke,newSize/2,newSize/2,1,1,0,(newSize/2)-0.5,(newSize/2)-0.5)
	pdb.gimp_image_merge_visible_layers(image,1)
# Index colors if not HD
	if (hd_resize == 0):
		pdb.gimp_image_convert_indexed(image,0,0,16,0,1,"")
		pdb.gimp_image_convert_rgb(image)
# Resize if HD
	if (hd_resize == 1):
		pdb.gimp_image_scale(image, newSize/2,newSize/2)
# Output image
	suffix = "_STC.png"
	if (hd_resize == 1):
		suffix = "_STC_HD.png"
	pdb.gimp_file_save(image,pdb.gimp_image_get_active_drawable(image),os.path.join(filepath,filename + suffix), filename + suffix)
	pdb.gimp_display_delete(display);
	return

register(
	"python-fu-STOCK-PROCESSOR",
	"Crops images for stock icons (Make sure mask matches image dimensions). Results go to the stock image folder. \n MAKE SURE THAT THE PAINTBRUSH TOOL IS SELECTED BEFORE YOU START!",
	"Using a user-defined mask, crops a user-defined image to a certain size, and offers resize options. The final result is then saved with the appropriate suffix to the same folder as the source image.",
	"tryptech",
	"tryptech",
	"2018",
	"<Toolbox>/Tools/Stock Processor",
	"",
	[
		(PF_FILE, "file_input", "Stock Image File", None),
		(PF_FILE, "file_mask", "Stock Mask File", None),
		(PF_FILE, "file_crop", "Stock Crop File", None),
		(PF_RADIO, "hd_resize", "Set Resize Scale: ", 0,
			(
				("SD (32x32)", 0),
				("HD (128x128)", 1)
			)
		)
	],
	[],
	crop_csp_process
)

main()
