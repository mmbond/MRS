from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

class PluginDialog(QtWidgets.QDialog):
    """
    Klasa koja predstavlja dialog u kojem se vrsi manipulacija nad prosirenjima.
    """
    def __init__(self, title="Plugin settings", parent=None, plugin_service=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz pluginova.

        :param title: naslov dijaloga.
        :type title: str
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        :param plugin_service: servis za pluginove
        :type plugin_service: PluginService
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)

        self.plugin_service = plugin_service

        self.plugin_options_layout = QtWidgets.QHBoxLayout()

        self.set_button = QtWidgets.QPushButton(QIcon("resources/icons/application-plus.png"), "Set as central")
        self.uninstall_button = QtWidgets.QPushButton(QIcon("resources/icons/minus-circle.png"), "Uninstall")
        self.enable_button = QtWidgets.QPushButton(QIcon("resources/icons/tick.png"), "Enable")
        self.disable_button = QtWidgets.QPushButton(QIcon("resources/icons/minus.png"), "Disable")
        self.plugin_dialog_layout = QtWidgets.QVBoxLayout()

        self.plugins_table = QtWidgets.QTableWidget(self)
        self.plugins_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.plugins_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.plugin_options_layout.addWidget(self.set_button)
        self.plugin_options_layout.addWidget(self.uninstall_button)
        self.plugin_options_layout.addWidget(self.enable_button)
        self.plugin_options_layout.addWidget(self.disable_button)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.on_reject)

        self.set_button.clicked.connect(self.on_set)

        self._populate_table()

        self.plugin_dialog_layout.addLayout(self.plugin_options_layout)
        self.plugin_dialog_layout.addWidget(self.plugins_table)
        self.plugin_dialog_layout.addWidget(self.button_box)

        self.setLayout(self.plugin_dialog_layout)

    def on_set(self):
        """
        Metoda koja se poziva kada se pritisne na dugme set central.
        """
        # FIXME: dobavi selekciju i aktiviraj widget
        selected_items = self.plugins_table.selectedItems()
        if len(selected_items) == 0:
            return
        symbolic_name = selected_items[3].text()
        self.parent().set_central_widget(symbolic_name)
        
    def on_accept(self):
        """
        Metoda koja se poziva na prihvatanje dijaloga.
        """
        return self.accept()

    def on_reject(self):
        """
        Metoda koja se poziva na odbijanje dijaloga.
        """
        return self.reject()

    def _populate_table(self):
        """
        Populise tabelu metapodacima plugina.
        """
        self.plugins_table.setColumnCount(5)
        self.plugins_table.setHorizontalHeaderLabels(
            ["Name", "Version", "Description", "Symbolic name", "Enabled"])
        # TODO: list all plugins
        self.plugins_table.setRowCount(len(self.plugin_service.plugins))
        for i, plugin in enumerate(self.plugin_service.plugins):
            name = QtWidgets.QTableWidgetItem(plugin.name)
            version = QtWidgets.QTableWidgetItem(plugin.version)
            description = QtWidgets.QTableWidgetItem(plugin.description)
            symbolic_name = QtWidgets.QTableWidgetItem(plugin.symbolic_name)
            enabled = QtWidgets.QTableWidgetItem("Enabled" if plugin.enabled else "Disabled")

            name.setFlags(name.flags() ^ Qt.ItemIsEditable)
            version.setFlags(version.flags() ^ Qt.ItemIsEditable)
            description.setFlags(description.flags() ^ Qt.ItemIsEditable)
            symbolic_name.setFlags(symbolic_name.flags() ^ Qt.ItemIsEditable)

            self.plugins_table.setItem(i, 0, name)
            self.plugins_table.setItem(i, 1, version)
            self.plugins_table.setItem(i, 2, description)
            self.plugins_table.setItem(i, 3, symbolic_name)
            self.plugins_table.setItem(i, 4, enabled)


