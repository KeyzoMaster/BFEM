from kivy import app
from kivy.metrics import dp
from kivy.properties import NumericProperty, DictProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput

from database import BFEMDB


class CandidateLine(BoxLayout):
    num = NumericProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    status = StringProperty("")

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        basic_infos = BFEMDB().basic_information_candidat(num)
        self.num = int(num)
        # fonction qui récupère les autres informations
        self.first_name = basic_infos[0]
        self.last_name = basic_infos[1]
        self.status = "---"


class DetailsLine(BoxLayout):
    label = StringProperty()
    value = StringProperty()

    def __init__(self, label, value, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.value = value


class PersonalDetails(TabbedPanelItem):
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.text = "Informations personnelles"
        self.content = GridLayout(cols=2, spacing=dp(15))
        self.details = {"num": num, "first_name": "First Name", "last_name": "Name", "birth_date": "01/01/2000",
                        "birth_place": "Dakar", "sex": "M", "nationality": "senegalese", "optional_test_choice": True,
                        "optional_test": "Drawing", "can_do_sport": True, "status": "---"}
        for k, v in self.details.items():
            self.content.add_widget(DetailsLine(label=str(k), value=str(v)))


class NotesDetails(TabbedPanelItem):
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.text = "Informations sur les notes"
        self.width = self.texture_size[0]
        self.padding = (10, 0)
        self.size_hint_x = None
        self.content = GridLayout(cols=2, spacing=dp(15))
        self.details = {"num": num, "first_name": "First Name", "last_name": "Name", "birth_date": "01/01/2000",
                        "birth_place": "Dakar", "sex": "M", "nationality": "senegalese", "optional_test_choice": True,
                        "optional_test": "Drawing", "can_do_sport": True, "status": "---"}
        for k, v in self.details.items():
            self.content.add_widget(DetailsLine(label=str(k), value=str(v)))


class DetailsContent(TabbedPanel):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.add_widget(PersonalDetails(num))
        self.add_widget(NotesDetails(num))


class CloseButton(Button):
    def __init__(self, popup, **kwargs):
        super().__init__(**kwargs)
        self.popup = popup
        self.on_release = self.popup.dismiss


class DetailsPopup(Popup):
    num = NumericProperty()
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        self.title = "Détails sur le candidat"
        self.title_size = dp(25)
        self.content = BoxLayout(orientation="vertical")
        self.content.add_widget(DetailsContent(num, size_hint_y=.9))
        self.b = CloseButton(popup=self, text="Fermer", size_hint_y=.1)
        self.content.add_widget(self.b)


class UpdateContent(PageLayout):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(PersonalUpdate(num))


class PersonalUpdate(BoxLayout):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)


class NotesUpdate(BoxLayout):
    pass


class UpdatePopup(Popup):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.title = "Modifications candidat"
        self.title_size = dp(30)
        self.content = UpdateContent(num)


class FormScreen(Screen):
    def on_reset(self):
        print("Form reset")

    def on_submit(self):
        print("Form submitted")


class CandidatesStack(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nums = BFEMDB().liste_num()
        for num in nums:
            self.add_widget(CandidateLine(num))
