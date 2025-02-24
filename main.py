from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from correction import *
import candidate
import statistiques
import impress
from database import BrevetDB
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
    tour = StringProperty("PREMIER TOUR")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_text = "Deliberation" if not BrevetDB().liste_copies_non_notees(self.tour) else "Correction"

    def refresh(self, tour="PREMIER TOUR"):
        self.tour = tour
        self.clear_widgets()
        self.__init__()


class FormScreen(Screen):
    is_valid = BooleanProperty()
    def on_submit(self, name_widget, sex_widget, birth_widget, nat_widget, opt_widget, type_widget, ability_widget,
                  attempts_widget):
        if name_widget and birth_widget and nat_widget and attempts_widget:
            print("Valid Form")
            (first_name, last_name) = name_widget
            sex = sex_widget
            (birth_date, birth_place) = birth_widget
            (nationality, school) = nat_widget
            option = opt_widget
            type = type_widget
            ability = ability_widget
            (attempts, moy_6e, moy_5e, moy_4e, moy_3e) = attempts_widget
            id_livret = BrevetDB().ajouter_livret(attempts, moy_6e, moy_5e, moy_4e, moy_3e)
            BrevetDB().ajouter_candidat(None, first_name, last_name, birth_date, birth_place, sex, nationality, school,
                                        option, ability, type, id_livret)
            num = BrevetDB().liste_num()[-1]
            matieres = BrevetDB().matieres_a_faire()
            BrevetDB().ajouter_toutes_copies_et_notes(num, matieres, note=None)
            self.is_valid = True
        else:
            self.is_valid = False


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
