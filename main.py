from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from correction import *
import candidate
import statistiques
import impress
from form import *

from kivy.config import Config

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')


class WindowManager(ScreenManager):
    pass


class LoginScreen(Screen):
    def on_validate(self, widget):
        print("It works")
        widget.dismiss()


class CandidateScreen(Screen):
    my_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_text = "Deliberation" if self.my_text == "Correction" else "Correction"

    def refresh(self):
        self.clear_widgets()
        self.__init__()


class CorrectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DeliberationScreen(Screen):
    pass


class StatistiquesScreen(Screen):
    pass


class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()
