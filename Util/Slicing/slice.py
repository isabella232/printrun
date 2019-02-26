import os
import shlex, subprocess
from multiprocessing import Process

from Util.Slicing.parse_svg import parse_svg

def slice_file(filepath, output_dir_path, curr_png_ref, total_png_ref, thickness):
    """
    Manages file slicing.
    Uses slic3r to slice a .STL file @filepath, storing the 
    resulting .gcode file in the directory @output_dir_path

    Args:
        - String filepath: Path to the file to slice.
        - String output_dir_path: Location to save the output of slicing.
        - Multiprocessing Value curr_png_ref: Used during SVG conversion to inform the parent of 
            the current png being converted.
        - Multiprocessing Value total_png_ref: Used during SVG conversion to inform the parent of 
            the total number of pngs to be converted.
        - String thickness: layer thickness in mm
    Return:
        0 on success and 1 on error
    """
    #  Error handling
    suffix = filepath.split('.')[-1]
    if (suffix != 'stl'):
        print('Only STL file slicing is currently supported')
        return
    
    # Extract the filename
    filename = filepath.split('.')[0].split('/')[-1]

    print('Calling slic3r on ', '\n filepath:', filepath, '\n and output path:', output_dir_path)
    
    # Create a child process to execute slicing and create GCODE.
    # GCODE is no longer necessary

    # gcode_slice_command = 'slic3r ' + filepath + ' --layer-height ' + thickness + ' --output ' + output_dir_path
    # print(gcode_slice_command)
    # subprocess.Popen(gcode_slice_command, shell=True)

    # Slice again to generate a SVG file containing the images.
    svg_slice_command = 'slic3r ' + filepath + ' --layer-height ' + thickness + ' --export-svg' + ' --output ' + output_dir_path
    subprocess.run(svg_slice_command, shell=True)

    svg_path = output_dir_path + '/' + filename + '.svg'
    print("slic3r should've put the svg here: ", svg_path, len(svg_path))
    
    # with subprocess.Popen(svg_slice_command, shell=True) as process:
    # Launch a separate process here to stop blocking - handle synchronization later.
    p = Process(target=parse_svg, args=(svg_path, curr_png_ref, total_png_ref))
    
    # Return a reference to the process. The parent will join the process on completion
    return p
    
    
