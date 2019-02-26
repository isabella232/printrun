ROOT_PATH = '/home/lumen/Volumetric/TouchPrint/App'
SLICE_OUTPUT_PATH = '/home/lumen/Volumetric/3dp'

# *NOTE: This assume the program is run from ROOT_PATH.

# Tried using the global path and changing the working directory for os.path (python), but this 
# caused issues with pronsole.
SLICE_OUTPUT_RELATIVE = './Sliced_Files'

PROJECTOR_IMG_WIDTH = 1280
PROJECTOR_IMG_HEIGHT = 800

BOUNDING_BOX_SCALING = 20

# Set motor axis
MOTOR_AXIS = 'X'