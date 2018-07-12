from utils import recon_utils
from utils import popup_utils
import config
import os
import time
import face_recognition
import numpy
from PIL import Image, ImageEnhance
from imgaug import augmenters

latest_image_name = ''


def capture_image(camera):
    global latest_image_name
    latest_image_name = get_next_temp_image_name()
    camera.export_to_png(latest_image_name)
    save_as_jpg(latest_image_name)
    if recon_utils.application_mode == 'RECOGNITION':
        edit_image(latest_image_name)
    if config.VERIFY_FACE_PRESENCE:
        if not recon_utils.is_face_present_in_image(latest_image_name):
            popup_utils.create_popup('No face detected', 'No face detected in captured image.\nTry again')
            return False
    print('Image {} saved to project directory'.format(latest_image_name))
    return True


def edit_image(image_name):
    image = read_as_pil_image(image_name)
    if config.IMAGE_SCALE != 1:
        image = apply_effect(image, augmenters.Scale(config.IMAGE_SCALE))
    if config.IMAGE_ROTATION != 0:
        image = image.rotate(config.IMAGE_ROTATION)
    if config.IMAGE_SHEAR != 0:
        image = apply_effect(image, augmenters.Affine(shear=config.IMAGE_SHEAR))
    if config.IMAGE_BLUR > 0:
        image = apply_effect(image, augmenters.GaussianBlur(sigma=config.IMAGE_BLUR))
    if config.IMAGE_SHARPEN != 0:
        image = apply_effect(image, augmenters.Sharpen(alpha=config.IMAGE_SHARPEN, lightness=1.0))
    if config.IMAGE_EMBOSS != 0:
        image = apply_effect(image, augmenters.Emboss(alpha=config.IMAGE_EMBOSS, strength=1.0))
    if config.IMAGE_DISTORTIONS != 0:
        image = apply_effect(image, augmenters.PiecewiseAffine(scale=config.IMAGE_DISTORTIONS))
    if config.IMAGE_PIXEL_DISPLACEMENT != 0:
        image = apply_effect(image, augmenters.ElasticTransformation(alpha=config.IMAGE_PIXEL_DISPLACEMENT, sigma=0.25))
    if config.IMAGE_BRIGHTNESS_INCREMENT != 1:
        image = ImageEnhance.Brightness(image).enhance(config.IMAGE_BRIGHTNESS_INCREMENT)
    if config.IMAGE_BRIGHTNESS_REDUCTION != 1:
        image = ImageEnhance.Brightness(image).enhance(config.IMAGE_BRIGHTNESS_REDUCTION)
    if config.IMAGE_CONTRAST_INCREMENT != 1:
        image = ImageEnhance.Contrast(image).enhance(config.IMAGE_CONTRAST_INCREMENT)
    if config.IMAGE_CONTRAST_REDUCTION != 1:
        image = ImageEnhance.Contrast(image).enhance(config.IMAGE_CONTRAST_REDUCTION)
    save_as_jpg(image_name, image)


def apply_effect(image, filter):
    image_as_ndarray = pil_image_to_ndarray(image)
    image_aug = filter.augment_image(image_as_ndarray)
    return ndarray_to_pil_image(image_aug)


def bytes_to_ndarray(image_as_bytes):
    file_name = get_next_temp_image_name()
    with open(file_name, 'wb') as output_file:
        output_file.write(image_as_bytes)
    return face_recognition.load_image_file(file_name)


def pil_image_to_ndarray(pil_image):
    return numpy.array(pil_image)


def ndarray_to_pil_image(ndarray):
    return Image.fromarray(numpy.uint8(ndarray))


def read_from_buffer(file_name):
    with open(config.TEMP_FOLDER_PATH + file_name, 'rb') as input_file:
        return input_file.read()


def read_as_pil_image(file_name):
    return Image.open(file_name)


def save_as_jpg(file_name, image=None):
    if image is None: image = Image.open(file_name)
    rgb_image = image.convert('RGB')
    rgb_image.save(file_name.strip('.png') + '.jpg')


def get_next_temp_image_name():
    time_as_string = time.strftime("%Y%m%d_%H%M%S")
    return config.TEMP_FOLDER_PATH + "IMG_{}.png".format(time_as_string)


def show_image(image_as_ndarray):
    pil_image = Image.fromarray(image_as_ndarray)
    pil_image.show()


def remove_temp_images():
    if config.CLEAR_TEMP_IMAGES:
        for parent, dir_names, file_names in os.walk(config.TEMP_FOLDER_PATH):
            for file_name in file_names:
                if file_name.endswith('.jpg') or file_name.endswith('.png'):
                    os.remove(os.path.join(parent, file_name))
                    print('Removed temporary image file: {}'.format(file_name))
