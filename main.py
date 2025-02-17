from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import candidate
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
    pass


class FormScreen(Screen):
    pass


class DeliberationScreen(Screen):
    pass


class CorrectionScreen(Screen):
    pass


class StatistiquesScreen(Screen):
    pass


class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()
