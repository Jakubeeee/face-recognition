from utils import image_utils
import config
import os.path
import sqlite3 as lite

connection = lite.connect('database.db')
cursor = connection.cursor()


def init_database():
    cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "username TEXT UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS images("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "file_name TEXT,"
                   "image BLOB,"
                   "user_id INTEGER,"
                   "FOREIGN KEY(user_id) REFERENCES users(id))")
    if config.CLEAR_USERS: purge_database()
    connection.commit()
    print("Database initialized")


def purge_database():
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM images")
    connection.commit()
    print("Database purged")


def save_user(user_data, user_images):
    username = user_data[0]
    insert_user_query = '''INSERT INTO users(username) VALUES(?);'''
    connection.execute(insert_user_query, [username])
    cursor.execute("SELECT id FROM users WHERE username = ?", [username])
    saved_user_id = cursor.fetchone()[0]
    for user_image in user_images:
        save_image(user_image, saved_user_id)
    print("User {} saved to database".format(username))
    connection.commit()


def save_image(file_name, user_id):
    file_name = os.path.basename(file_name)
    face_image_as_bytes = image_utils.read_from_buffer(file_name)
    insert_image_query = '''INSERT INTO images(file_name, image, user_id) VALUES(?, ?, ?);'''
    connection.execute(insert_image_query, [file_name, lite.Binary(face_image_as_bytes), user_id])
    image_utils.remove_temp_images()
    print("Image saved to database")


def fetch_all_images_data():
    print('Fetching all users data from db:')
    cursor.execute("SELECT u.username, i.image FROM users u, images i WHERE i.user_id = u.id ORDER BY u.username DESC")
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
    return rows
