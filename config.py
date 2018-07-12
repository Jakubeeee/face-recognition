import os

# general configuration
PROJECT_LOCATION = os.path.dirname(os.path.realpath(__file__))
TEMP_FOLDER_PATH = PROJECT_LOCATION + '\\temp\\'
SHOW_FACE_IMAGES_IN_EXTERNAL_WINDOW = False
CACHING_ENABLED = True
CLEAR_TEMP_IMAGES = True
VERIFY_FACE_PRESENCE = True
CLEAR_USERS = False

# default: 0.6
TOLERANCE = 0.6

# default: 1
IMAGE_SCALE = 1
# default: 0
IMAGE_ROTATION = 0
# default: 0
IMAGE_SHEAR = 0
# default: 0
IMAGE_BLUR = 0
# default: 0
IMAGE_SHARPEN = 0
# default: 0
IMAGE_EMBOSS = 0
# default: 0
IMAGE_DISTORTIONS = 0
# default: 0
IMAGE_PIXEL_DISPLACEMENT = 0
# default: 1
IMAGE_BRIGHTNESS_INCREMENT = 1
# default: 1
IMAGE_BRIGHTNESS_REDUCTION = 1
# default: 1
IMAGE_CONTRAST_INCREMENT = 1
# default: 1
IMAGE_CONTRAST_REDUCTION = 1

