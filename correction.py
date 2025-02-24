import re

from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel
from kivy.uix.textinput import TextInput

from database import BrevetDB


class CorrectionLine(BoxLayout):
    anonymat = StringProperty()
    note = StringProperty()

    def __init__(self, anonymat, **kwargs):
        super().__init__(**kwargs)
        self.anonymat = anonymat

    def is_valid(self):
        motif_avg = r"^(20(\.0{1,2})?|1?\d(\.\d{1,2})?)$"
        return re.match(motif_avg, self.note)

    def correct(self):
        if self.is_valid():
            BrevetDB().correction_copie(self.anonymat, float(self.note))


class CorrectionTabItem(TabbedPanelItem):
    def __init__(self, tour, **kwargs):
        super().__init__()
        self.text = tour
        self.add_widget(CorrectionBox(tour.upper()))


class CorrectionTabPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.add_widget(CorrectionTabItem("Premier Tour"))
        self.add_widget(CorrectionTabItem("Second Tour"))


class CorrectionBox(StackLayout):
    def __init__(self, tour, **kwargs):
        self.tour = tour
        self.matieres = BrevetDB().liste_copies_non_notees(self.tour)
        super().__init__(**kwargs)
        for k, v in self.matieres.items():
            self.add_widget(Button(text=k, size_hint=(.25, .25),
                                   on_release=Factory.CorrectionPopup(v, self).open))

    def reset(self):
        self.clear_widgets()
        self.__init__(self.tour)


class CorrectionPopup(Popup):
    def __init__(self, liste_copies, parent_box, **kwargs):
        super().__init__(**kwargs)
        self.parent_box = parent_box
        self.title = "Correction"
        self.liste_copies = liste_copies
        container = BoxLayout(orientation="vertical")
        self.scroll_view = ScrollView()
        self.corr_box = StackLayout(size_hint_y=None)
        self.corr_box.height = self.corr_box.minimum_height
        for copie in liste_copies:
            self.corr_box.add_widget(CorrectionLine(str(copie)))
        self.scroll_view.add_widget(self.corr_box)
        self.button_container = BoxLayout()
        self.button = Button(size_hint_y=None, height=dp(40), pos_hint={"x": 0}, text="Corriger")
        self.button.on_release = self.correction
        self.button_container.add_widget(self.button)
        self.button_container.add_widget(Button(size_hint_y=None, height=dp(40), pos_hint={"x": 0}, text="Quitter",
                                           on_release=self.dismiss))
        container.add_widget(self.scroll_view)
        container.add_widget(self.button_container)
        self.content = container

    def correction(self):
        for line in self.corr_box.children:
            if not line.is_valid():
                return

        for line in self.corr_box.children:
            line.correct()
        self.parent_box.reset()
        self.dismiss()
