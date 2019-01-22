from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from gui.dialogs.plugin_dialog import PluginDialog

class MainWindow(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor aplikacije.
    """
    def __init__(self, ps, parent: QtWidgets.QWidget=None):
        """
        Inicijalizator glavnog prozora

        :param ps: plugin servis koji nam obezbedjuje operacije nad pluginovima.
        :type ps: PluginService
        :param parent: roditelj glavnog prozora (default: None).
        :type parent: QWidget
        """
        # pozivanje super inicijalizatora
        super().__init__(parent) 
        # podesavanje naslova prozora
        self.setWindowTitle("Univerzitet Singidunum") 
        # menjanje velicine prozora
        self.resize(800, 600) 
        # postavljanje ikonice prozora
        self.setWindowIcon(QIcon("resources/icons/abacus.png")) 
        # cuvanje atributa za plugin servis
        self.plugin_service = ps
        # atribut za cuvanje svih akcija u sistemu, ideja je da ove akcije mogu da se dele sa drugim widget-ima
        self.action_dict = {
            "open":  QtWidgets.QAction(QIcon("resources/icons/folder-open-document.png"), "&Open document"),
            "plugin_settings": QtWidgets.QAction(QIcon("resources/icons/puzzle.png"), "&Plugin settings")
        }
        # atribut za meni
        self.menu_bar = QtWidgets.QMenuBar(self)
        # atribut za toolbar
        self.tool_bar = QtWidgets.QToolBar("Toolbar", self)
        # pojedinacni meniji
        self.file_menu = QtWidgets.QMenu("&File", self.menu_bar)
        self.view_menu = QtWidgets.QMenu("&View", self.menu_bar)
        self.tools_menu = QtWidgets.QMenu("&Tools", self.menu_bar)
        self.help_menu = QtWidgets.QMenu("&Help", self.menu_bar)
        # centralni widget je mesto deo glavnog prozora u koji treba da se smesti glavni widget aplikacije
        self.central_widget = QtWidgets.QTextEdit(self)
        # pozivanje sopstvenih privatnih metoda
        self._bind_actions()
        self._populate_menu_bar()
        self._populate_tool_bar()

        # postavljanje centralnog widgeta i postavljanje toolbara i menija
        self.setCentralWidget(self.central_widget)
        self.addToolBar(self.tool_bar)
        self.setMenuBar(self.menu_bar)

    def _populate_menu_bar(self):
        """
        Populise akcije u menije
        """
        self.file_menu.addAction(self.action_dict["open"])
        self.view_menu.addAction(self.tool_bar.toggleViewAction())
        self.tools_menu.addAction(self.action_dict["plugin_settings"])
        self.menu_bar.addMenu(self.file_menu)
        self.menu_bar.addMenu(self.view_menu)
        self.menu_bar.addMenu(self.tools_menu)
        self.menu_bar.addMenu(self.help_menu)

    def _populate_tool_bar(self):
        """
        Populise akcije u toolbar
        """
        self.tool_bar.addAction(self.action_dict["open"])

    def _bind_actions(self):
        """
        Uvezuje akcije sa funkcijama koje se izvrsavaju na njihovo okidanje.
        """
        self.action_dict["open"].triggered.connect(self.on_open)
        self.action_dict["plugin_settings"].triggered.connect(self.on_open_plugin_settings_dialog)

    def on_open(self):
        """
        Kreira sistemski dialog za otvaranje fajlova i podesava sadrzaj tekstualnog editora, ucitanim tekstom.
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open python file", ".", "Python Files (*.py)")
        with open(file_name[0], "r") as fp:
            text_from_file = fp.read()
            self.central_widget.setText(text_from_file)

    def on_open_plugin_settings_dialog(self):
        """
        Kreira dialog za podesavanje pluginova, kako bi se nad njima mogla vrsiti manipulacija.
        """
        dialog = PluginDialog("Plugin settings", self, self.plugin_service)
        dialog.exec_()

    def set_central_widget(self, symbolic_name: str):
        """
        Podesava centralni widget glavnog prozora, na osnovu simboličkog imena se dobija plugin
        koji će se smestiti u centralni deo glavnog prozora.

        :param symbolic_name: Simbolicko ime plugina koji želimo da instanciramo.
        """
        # try:

        plugin = self.plugin_service.get_by_symbolic_name(symbolic_name)
        widgets = plugin.get_widget()
        self.setCentralWidget(widgets[0])
        if widgets[1] is not None:
            self.tool_bar.addSeparator()
            self.tool_bar.addActions(widgets[1].actions())
        self.menu_bar.addMenu(widgets[2]) if widgets[2] is not None else None
        # except IndexError:
        #     print("Ne postoji ni jedan plugin sa zadatim simboličkim imenom!")
