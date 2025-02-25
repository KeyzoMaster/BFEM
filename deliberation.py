from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel

from database import BrevetDB


class DeliberationTabPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.add_widget(DeliberationTabItem("Premier Tour"))
        self.add_widget(DeliberationTabItem("Second Tour"))


class DeliberationTabItem(TabbedPanelItem):
    def __init__(self, tour, **kwargs):
        super().__init__(**kwargs)
        self.text = tour
        scroll_view = ScrollView()
        stack = DeliberationStack(tour.upper(), size_hint_y=None)
        stack.height = stack.minimum_height
        scroll_view.add_widget(stack)
        self.add_widget(scroll_view)


class DeliberationTabHeader(BoxLayout):
    pass


class DeliberationLine(BoxLayout):
    def __init__(self, candidat, rang, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text=str(candidat["Numéro de table"])))
        self.add_widget(Label(text=str(candidat["Prénom(s)"])))
        self.add_widget(Label(text=str(candidat["Nom"])))
        self.add_widget(Label(text=str(candidat["Sexe"])))
        self.add_widget(Label(text=str(candidat["Etablissement"])))
        self.add_widget(Label(text=str(candidat["Statut"])))


class DeliberationStack(StackLayout):
    def __init__(self, tour, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(DeliberationTabHeader())
        resultats = BrevetDB().resultats(tour=tour)
        i = 1
        if resultats:
            for r in resultats:
                self.add_widget(DeliberationLine(r, i))
                i += 1
