from plugin_framework.plugin import Plugin
from .widgets.contacts_widget import ContactsWidget

class Main(Plugin):
    """
    Klasa koja predstavlja konkretni plugin. Nasledjujemo "apstraktnu" klasu Plugin.
    Ova klasa predstavlja plugin za aplikaciju kontakti (imenik).
    """
    def __init__(self, spec):
        """
        Inicijalizator imenik plugina.

        :param spec: specifikacija metapodataka o pluginu.
        :type spec: dict
        """
        super().__init__(spec)

    def get_widget(self, parent=None):
        """
        Ova metoda vraca konkretni widget koji ce biti smesten u centralni deo aplikacije i njenog 
        glavnog prozora. Može da vrati toolbar, kao i meni, koji će biti smešten u samu aplikaciju.
        
        :param parent: bi trebao da bude widget u koji će se smestiti ovaj koji naš plugin omogućava.
        :returns: QWidget, QToolbar, QMenu
        """
        return ContactsWidget(parent), None, None 