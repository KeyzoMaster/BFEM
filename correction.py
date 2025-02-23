from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel


class CorrectionTabItem(TabbedPanelItem):
    def __init__(self, name, matieres, **kwargs):
        super().__init__()
        self.text = name
        self.add_widget(CorrectionBox(matieres))


class CorrectionTabPanel(TabbedPanel):
    def __init__(self, nom_tab1, nom_tab2, matieres_premier_tour, matieres_second_tour, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.add_widget(CorrectionTabItem(nom_tab1, matieres_premier_tour))
        self.add_widget(CorrectionTabItem(nom_tab2, matieres_second_tour))


class CorrectionButton(Button):

    def candidats_non_notes(self):
        pass


class CorrectionBox(StackLayout):
    def __init__(self, matieres: dict, **kwargs):
        super().__init__(**kwargs)
        self.matieres = matieres
        for k, v in matieres.items():
            # Fonction qui retourne les anonymats des candidats n'ayant pas de notes
            self.add_widget(CorrectionButton(text=v, size_hint=(.25, .25)))


class CorrectionPopup(Popup):
    pass
