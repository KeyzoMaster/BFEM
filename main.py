from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from correction import *
import candidate
import statistiques
import impress

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


class FormScreen(Screen):
    pass


class CorrectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        liste_matieres_premier_tour = {"Compo_Franc": "Composition française", "Dictee": "Dictée",
                                       "Etude_de_texte": "Etude de texte", "Instruction_Civique": "Instruction Civique",
                                       "Histoire_Geographie": "Histoire/Géographie", "Mathematiques": "Mathématiques",
                                       "PC_LV2": "PC LV2", "SVT": "SVT", "Anglais1": "Anglais 1",
                                       "Anglais_orale": "Orale d'Anglais", "EPS": "EPS",
                                       "Epreuve_Facultative": "Epreuve Facultative"}
        liste_matieres_second_tour = {"": ""}
        self.add_widget(CorrectionTabPanel("Premier tour", "Second tour", liste_matieres_premier_tour,
                                           liste_matieres_second_tour))


class DeliberationScreen(Screen):
    pass


class StatistiquesScreen(Screen):
    pass


class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()
