from kivy.uix.popup import Popup
from kivy.uix.label import Label


def create_popup(title_text, content_text):
    popup = Popup(title=title_text,
                  content=Label(text=content_text),
                  size=(120, 120),
                  size_hint=(0.4, 0.4))
    popup.open()
