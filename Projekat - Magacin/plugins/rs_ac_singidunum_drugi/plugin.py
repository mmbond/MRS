from plugin_framework.plugin import Plugin

class Main(Plugin):
    """
    Primer drugog plugina.
    """
    def __init__(self, spec):
        super().__init__(spec)

    def get_widget(self, parent=None):
        return None, None, None
