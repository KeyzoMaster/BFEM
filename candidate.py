from kivy import app
from kivy.metrics import dp
from kivy.properties import NumericProperty, DictProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput


class CandidateLine(BoxLayout):
    num = NumericProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    status = StringProperty("")

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        # fonction qui récupère les autres informations
        self.first_name = "First Name"
        self.last_name = "Last Name"
        self.status = "---"


class DetailsLine(BoxLayout):
    label = StringProperty()
    value = StringProperty()

    def __init__(self, label, value, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.value = value


class PersonalDetails(GridLayout):
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.details = {"num": num, "first_name": "First Name", "last_name": "Name", "birth_date": "01/01/2000",
                        "birth_place": "Dakar", "sex": "M", "nationality": "senegalese", "optional_test_choice": True,
                        "optional_test": "Drawing", "can_do_sport": True, "status": "---"}
        for k, v in self.details.items():
            self.add_widget(DetailsLine(label=str(k), value=str(v)))


class NotesDetails(GridLayout):
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.details = {"num": num, "first_name": "First Name", "last_name": "Name", "birth_date": "01/01/2000",
                        "birth_place": "Dakar", "sex": "M", "nationality": "senegalese", "optional_test_choice": True,
                        "optional_test": "Drawing", "can_do_sport": True, "status": "---"}
        for k, v in self.details.items():
            self.add_widget(DetailsLine(label=str(k), value=str(v)))


class DetailsContent(PageLayout):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(PersonalDetails(num))
        self.add_widget(NotesDetails(num))


class DetailsPopup(Popup):
    num = NumericProperty()
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        self.title = "Détails sur le candidat"
        self.title_size = dp(25)
        self.content = DetailsContent(num)


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
        for i in range(0, 10):
            self.add_widget(CandidateLine(i))
