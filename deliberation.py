from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanel


class DeliberationTabPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_tab = False
        self.add_widget(DeliberationTabItem("Premier Tour"))
        self.add_widget(DeliberationTabItem("Second Tour"))


class DeliberationTabItem(TabbedPanelItem):
    def __init__(self, tour, **kwargs):
        super().__init__(**kwargs)
        self.text = tour
        self.add_widget(DeliberationStack(tour.upper()))


class DeliberationTabHeader(BoxLayout):
    pass


class DeliberationLine(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class DeliberationStack(StackLayout):
    def __init__(self, tour, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(DeliberationTabHeader)

