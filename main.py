from utils import image_utils
from utils import recon_utils
from utils import db_utils
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen


class ScreenManagement(ScreenManager):
    @staticmethod
    def switch_screen(screen_name):
        app.root.current = screen_name
        print('Screen changed to: {}'.format(screen_name))


class MainScreen(Screen):
    pass


class MainLayout(BoxLayout):
    def on_recognize_button_pressed(self):
        recon_utils.change_mode('RECOGNITION')

    def on_add_new_user_button_pressed(self):
        recon_utils.change_mode('ADDING_USER')


class CameraScreen(Screen):
    pass


class CameraLayout(BoxLayout):
    def on_capture_image_button_pressed(self):
        camera = self.ids['camera']
        if not image_utils.capture_image(camera):
            image_utils.remove_temp_images()
            return
        if recon_utils.application_mode == 'RECOGNITION':
            recon_utils.compare_faces()
        elif recon_utils.application_mode == 'ADDING_USER':
            ScreenManagement.switch_screen('input_username_screen')


class InputUsernameScreen(Screen):
    pass


class InputUsernameLayout(BoxLayout):
    def save_user(self, username):
        user_data = [username]
        user_images_names = [image_utils.latest_image_name]
        db_utils.save_user(user_data, user_images_names)


class ComparingScreen(Screen):
    pass


class FaceImage(Image):
    pass


class ComparingLayout(BoxLayout):
    pass


presentation = Builder.load_file('view\\faceRecon.kv')


class FaceReconApp(App):
    def build(self):
        return presentation


if __name__ == "__main__":
    app = FaceReconApp()
    db_utils.init_database()
    app.run()
