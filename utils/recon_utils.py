from utils import image_utils
from utils import popup_utils
from utils import db_utils
from utils import lang_utils
import config
import face_recognition
import numpy

# possible values are: RECOGNITION, ADDING_USER
application_mode = ''

cached_encodings_list = []


def change_mode(new_mode):
    global application_mode
    application_mode = new_mode
    print('Application mode changed to: {} '.format(application_mode))


def is_face_present_in_image(image_name):
    image = face_recognition.load_image_file(image_name)
    if face_recognition.face_locations(image):
        return True
    else:
        return False


def compare_faces(unknown_image_name=None, face_images_data=None, tolerance=None):
    unknown_image_name = lang_utils.nvl(unknown_image_name, image_utils.latest_image_name)
    print(image_utils.latest_image_name)
    print(unknown_image_name)
    unknown_image = face_recognition.load_image_file(unknown_image_name)
    unknown_face_encoding = get_face_encodings(unknown_image)

    return_value = 'UNKNOWN'
    if unknown_face_encoding is None:
        print('Cannot read encodings from the face')
        image_utils.remove_temp_images()
        return return_value

    face_images_data = lang_utils.nvl(face_images_data, db_utils.fetch_all_images_data())
    encodings_from_db = {}

    for face_image_data in face_images_data:
        username, image_as_bytes = face_image_data
        image_from_db = image_utils.bytes_to_ndarray(image_as_bytes)
        encoding_from_db = get_face_encodings(image_from_db, username)
        if encoding_from_db is None:
            image_utils.remove_temp_images()
            return return_value
        encodings_from_db[username] = encoding_from_db

    all_results = get_faces_distances(list(encodings_from_db.values()), unknown_face_encoding)
    print('All comparision results: {}'.format(all_results))
    best_result = min(all_results)
    print('Best result: {}'.format(best_result))
    best_result_index = all_results.index(best_result)
    matching_username = list(encodings_from_db.keys())[best_result_index]
    print('Best guess: {}'.format(matching_username))

    tolerance = lang_utils.nvl(tolerance, config.TOLERANCE)
    if best_result <= tolerance:
        comparision_message = 'This face belongs to {}'.format(matching_username)
        return_value = matching_username
    else:
        comparision_message = 'Cannot find user with face from image'
    print(comparision_message)
    popup_utils.create_popup('Face recognition result:', comparision_message)
    image_utils.remove_temp_images()
    return return_value


def get_faces_distances(face_encodings_from_db, unknown_face_encoding):
    if len(face_encodings_from_db) == 0:
        return numpy.empty((0))
    return list(numpy.linalg.norm(face_encodings_from_db - unknown_face_encoding, axis=1))


def get_face_encodings(image, username=None):
    face_encodings = None

    if config.CACHING_ENABLED and username is not None:
        for cached_encodings in cached_encodings_list:
            if cached_encodings[0] == username:
                return cached_encodings[1]

    face_image = cut_faces_from_image(image)
    try:
        face_encodings = face_recognition.face_encodings(face_image)[0]
    except:
        popup_utils.create_popup('Error occurred:', 'An error has occurred while encoding face. Try again')

    if config.CACHING_ENABLED and username is not None:
        cache_tuple = (username, face_encodings)
        if cache_tuple not in cached_encodings_list:
            cached_encodings_list.append(cache_tuple)

    return face_encodings


def cut_faces_from_image(image):
    try:
        top, right, bottom, left = detect_faces_locations(image)[0]
        face_image = image[top:bottom, left:right]
        if config.SHOW_FACE_IMAGES_IN_EXTERNAL_WINDOW:
            image_utils.show_image(face_image)
        return face_image
    except IndexError:
        print('Cannot find any face in the image!')


def detect_faces_locations(image=None):
    face_locations = face_recognition.face_locations(image)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        print("A face located at pixel loaction Top: {}, Left: {}, Bottom: {}, Right: {}".format(
            top, left, bottom, right))
        print("Total amount of faces found in this image: {}".format(len(face_locations)))
    return face_locations
