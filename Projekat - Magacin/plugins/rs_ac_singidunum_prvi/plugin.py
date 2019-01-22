from plugin_framework.plugin import Plugin
from PySide2 import QtWidgets

class Main(Plugin):
    """
    Primer prvog plugina.
    """
    def __init__(self, spec):
        super().__init__(spec)

    def get_widget(self, parent=None):
        return QtWidgets.QTextEdit(parent), None, None
