from kivy import app
from kivy.metrics import dp
from kivy.properties import NumericProperty, DictProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput
from setools import Boolean

from database import BrevetDB


class CandidateLine(BoxLayout):
    num = NumericProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    status = StringProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        basic_infos = BrevetDB().basic_information_candidat(num)
        self.num = int(num)
        self.first_name = basic_infos[0]
        self.last_name = basic_infos[1]
        self.status = basic_infos[2]


class DetailsLine(BoxLayout):
    label = StringProperty()
    value = StringProperty()
    inactive = BooleanProperty(True)

    def __init__(self, label, value, inactive=True, **kwargs):
        super().__init__(**kwargs)
        self.inactive = inactive
        self.label = label
        self.value = value


class PersonalDetails(TabbedPanelItem):
    details = DictProperty()

    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.text = "Informations personnelles"
        self.content = GridLayout(spacing=10, cols=4)
        self.details = BrevetDB().personal_information_candidat(num)
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
        self.content = GridLayout(spacing=10, cols=4)
        self.details = BrevetDB().notes_information_candidat(num)
        for k, v in self.details.items():
            self.content.add_widget(DetailsLine(label=str(k), value=str(v)))


class DetailsContent(TabbedPanel):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.add_widget(PersonalDetails(num))
        self.add_widget(NotesDetails(num))


class DeleteButton(Button):
    def __init__(self, popup, **kwargs):
        super().__init__(**kwargs)
        self.popup = popup
        self.on_release = self.popup.delete


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
        self.b = CloseButton(popup=self, text="Fermer")
        self.b2 = DeleteButton(popup=self, text="Supprimer")
        box = BoxLayout(size_hint_y=.1)
        box.add_widget(self.b)
        box.add_widget(self.b2)
        self.content.add_widget(box)

    def delete(self):
        BrevetDB().supprimer_candidat(self.num)
        self.dismiss()


class UpdateContent(BoxLayout):
    def __init__(self, num, popup, **kwargs):
        super().__init__(**kwargs)
        self.popup = popup
        self.grid = GridLayout(cols=4, size_hint_y=.9)
        self.infos = BrevetDB().personal_information_candidat(num)
        self.grid.add_widget(DetailsLine("Prénom(s)", self.infos["Prénom(s)"], inactive=False))
        self.grid.add_widget(DetailsLine("Nom", self.infos["Nom"], inactive=False))
        self.grid.add_widget(DetailsLine("Date de naissance", self.infos["Date de naissance"], inactive=False))
        self.grid.add_widget(DetailsLine("Lieu de naissance", self.infos["Lieu de naissance"], inactive=False))
        self.grid.add_widget(DetailsLine("Sexe", self.infos["Sexe"], inactive=False))
        self.grid.add_widget(DetailsLine("Nationalité", self.infos["Nationalité"], inactive=False))
        self.grid.add_widget(DetailsLine("Etablissement", self.infos["Etablissement"], inactive=False))
        self.grid.add_widget(DetailsLine("Epreuve Facultative", self.infos["Epreuve Facultative"], inactive=False))
        self.grid.add_widget(DetailsLine("Aptitude sportive", self.infos["Aptitude sportive"], inactive=False))
        self.grid.add_widget(DetailsLine("Type de candidat", self.infos["Type de candidat"], inactive=False))
        self.grid.add_widget(DetailsLine("Nombre de tentatives", self.infos["Nombre de tentatives"], inactive=False))
        self.grid.add_widget(DetailsLine("Moyenne 6e", self.infos["Moyenne 6e"], inactive=False))
        self.grid.add_widget(DetailsLine("Moyenne 5e", self.infos["Moyenne 5e"], inactive=False))
        self.grid.add_widget(DetailsLine("Moyenne 4e", self.infos["Moyenne 4e"], inactive=False))
        self.grid.add_widget(DetailsLine("Moyenne 3e", self.infos["Moyenne 3e"], inactive=False))
        self.button_box = BoxLayout(size_hint_y=.1)
        self.button_box.add_widget(Button(text="Quitter", on_release=self.popup.dismiss))
        self.button_box.add_widget(Button(text="Modifier"))
        self.button_box.children[-1].on_release = self.update
        self.add_widget(self.grid)
        self.add_widget(self.button_box)

    def update(self):
        (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o) = self.grid.children
        BrevetDB().modifier_candidat(a.value, b.value, c.value, d.value, e.value, f.value, g.value, h.value, i.value,
                                     j.value, k.value, l.value, m.value, n.value, o.value,
                                     int(self.infos["ID Livret"]), self.infos["Numéro de table"])
        self.popup.dismiss()


class UpdatePopup(Popup):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.title = "Modifications candidat"
        self.title_size = dp(30)
        self.content = UpdateContent(num, self)


class CandidatesStack(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nums = BrevetDB().liste_num()
        for num in nums:
            self.add_widget(CandidateLine(num))

