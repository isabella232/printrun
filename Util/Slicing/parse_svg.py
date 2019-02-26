"""
slic3r outputs a single SVG containing all of the layers.

This script traverses the file, and converts each layer to a PNG.
The conversion is executed by writting the layer to layer_help.svg and using inkspace 
to convert the individaul layer to a PNG.

The generated PNGs are saved to a directory named after the input SVG.
"""

import xml.etree.ElementTree as ET
import os
import subprocess

# jmil insert timer
from timeit import default_timer as timer

# import global constants
from Util.constants import PROJECTOR_IMG_WIDTH, PROJECTOR_IMG_HEIGHT, SLICE_OUTPUT_PATH, ROOT_PATH

def parse_svg(filepath, curr_png_ref, total_png_ref):
    """
    Parses the layers from the file @ filepath and converts each layer to a PNG.
    Saves the resulting PNGs to a directory named "filename_imgs" in the 
    Sliced_Files directory.

    Args:
        - (String) filepath: Path to an SVG file.
        - (Multiprocessing Shared Variable) curr_png_ref: Pass information about current png in 
            conversion process to the parent.
        - (Multiprocessing Shared Variable) total_png_ref: Pass information about total pngs in 
            conversion process to the parent.
    """
    # lower the priority of the parsing process
    # TODO I dont think this helped
    # os.system("renice -n %d %d" % (19, os.getpid()))
    
    suffix = filepath.split('.')[-1]
    # Check filetype - allow XML as well as SVG
    if (suffix != 'svg' and suffix != 'xml'):
        print('ERROR: non-svg file type. \nPlease provide a SVG file - this function is built to operate on SVG output from slic3r.')
        return
    
    # Extract the name of the file.
    filename = filepath.split('.')[0].split('/')[-1]
    
    # Make sure the file exists.
    
    # os.path cwd is set to where the program was launched. 
    # Thus, checking file existence requires converting the passed absolute path to a path relative 
    # to the os cwd. Also, reading and writing files require this relative path.
    # This confusion arises because subprocesses require absolute paths.
    print('parsing file @:', filepath)
    
    os.chdir('/home/lumen')

    # Ensure the SVG exists
    if (not os.path.isfile(filepath)):
        print('ERROR: File not found. \nPlease ensure you have provided the correct filepath')
        return


    # Parse the file and get the XML root
    tree = ET.parse(filepath)
    root = tree.getroot()
    # Parse the desired image dimensions from the SVG
    img_width = 287
    img_height = 287
    if (root.attrib['width']):
        # Convert width in mm to integer number of 50um pixels
        extracted_width = root.attrib['width']
        img_width = int(float(extracted_width)/(50*.001))
        print('new width ', img_width)
    else:
        print('COULD NOT EXTRACT WIDTH!!!!')
    
    if (root.attrib['height']):
        # Convert height in mm to integer number of 50um pixels
        extracted_height = root.attrib['height']
        img_height = int(float(extracted_height)/(50*.001))
        print('new width ', img_height)
    else:
        print('COULD NOT EXTRACT height!!!!')

    # Update the parent with the number of pngs to be converted.
    total_png_ref.value = len(root)
    curr_png_ref.value = 0
    
    # Number of places of largest image index
    img_places = len(str(len(root)))

    # Headers declaring the SVG file type
    header_1 = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    header_2 = "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.0//EN\" \"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd\">\n"
    header_3 = "<svg width=\"" + extracted_width + "\" height=\"" + extracted_height + "\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:svg=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:slic3r=\"http://slic3r.org/namespaces/slic3r\">\n"


    # Dimensions of the PNG files.
    png_dimensions = '-w ' + str(img_width) + ' -h ' + str(img_height)

    # Subprocess requires the absolute path.
    output_path = SLICE_OUTPUT_PATH + '/' + filename + '_imgs/'

    # Delete directory if it exists to clear out previous slicing
    subprocess.run('rm -rf ' + output_path ,shell = True)

    # Create a directory for the exported images
    subprocess.run('mkdir -p ' + output_path ,shell = True)

    # Start the timer
    timer_start = timer()
    print('timer started')
    
    
    # For each SVG layer within the parent SVG output:
    for layer_index,child in enumerate(root):

        # Update the parent with the index of the layer being converted.
        curr_png_ref.value = layer_index

        #Debug mode
        print(str(layer_index) + ' IS MY INDEX FOR THIS CHILD')

        # Path to svg_for_one_layer (relative to os.cwd)
        layer_index_str = str(layer_index)
        
        # Preface the layer_index with leading zeros
        filled_layer_index = layer_index_str.zfill(img_places)
        
        # set the full path and filename for a single svg for a single layer
        svg_for_one_layer = output_path + filled_layer_index + '.svg'

        # Debug mode
        print(svg_for_one_layer + ' is my svg for layer: ' + '%05d' % layer_index)

        # Write the SVG headers first - these can be reused for each image.
        with open(svg_for_one_layer, 'w') as layer_fd:
            # 'w' parameter opens the file - creates if it doesn't exist - and truncates.
            layer_fd.write(header_1)
            layer_fd.write(header_2)
            layer_fd.write(header_3)
            # Save the header end position.
            header_end = layer_fd.tell()
    
        # Open a fd to layer_helper to write XML as binary.
        with open(svg_for_one_layer, 'ab') as layer_fd:    
            # The file should be structured as a series of groups representing each layer.
            # Extract each layer to a PNG.

            # Debug mode
            print(str(layer_index) + " IS STILL MY INDEX FOR THIS CHILD\n\n")
            
            # Delete everything following the header.
            layer_fd.truncate(header_end)
        
            # Write the layer.
            layer_string = ET.tostring(child)
            layer_fd.write(layer_string)
        
            # Close the svg tag - must write in binary
            layer_fd.write("</svg>".encode('utf8'))
            

        # Convert the SVG for this one layer to a png.
        png_name = output_path + filled_layer_index + '.png '


        ##### TIME IT WITH INKSCAPE
        # Inkscape timer begin
        inkscape_timer_start = timer()

        # inkscape command to convert the svg to a png
        png_cmd = 'inkscape -z -e ' + png_name +  png_dimensions + ' ' + svg_for_one_layer

        subprocess.run(png_cmd, shell=True)

        inkscape_timer_end = timer()
        timer_duration_in_seconds = (inkscape_timer_end - inkscape_timer_start)
        print("\n\n#######\nIt took " + str(timer_duration_in_seconds) + ' seconds to convert one SVG into a PNG using inkscape.')


        ##### TIME IT WITH RSVG
        # rsvg-convert --width 287 --height 287 makerook.svg > makerook-TEST.png
        

        # Image has been created.
        # Set the canvas size to the projector size and the background to black.
        # Ex: 'convert -size 1280x800 xc:black makerook_imgs/52.png -gravity center -composite output.png'
        total_dimensions = 'convert -size ' + str(PROJECTOR_IMG_WIDTH) + 'x' + str(PROJECTOR_IMG_HEIGHT)
        png_bg_cmd = total_dimensions + ' xc:black ' + png_name + ' -gravity center -composite ' + png_name
        subprocess.run(png_bg_cmd, shell=True)





    # End Timer and write output
    timer_end = timer()
    timer_duration_in_seconds = (timer_end - timer_start)
    print("\n\n#######\nIt took " + str(timer_duration_in_seconds) + " seconds to convert one SVG into " + str(layer_index + 1) + ' SVGs and then into PNGs.')

    # Now we want to convert each one into a png

