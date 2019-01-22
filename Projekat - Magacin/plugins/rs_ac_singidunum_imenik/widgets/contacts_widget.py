from PySide2 import QtWidgets
from PySide2 import QtGui
from ..contacts_model import ContactsModel
from .dialogs.add_contact_dialog import AddContactDialog


class ContactsWidget(QtWidgets.QWidget):
    """
    Klasa koja predstavlja glavni widget plugina za kontakte.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator widgeta za kontakte.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.open_contacts = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/folder-open-document.png"), "Otvori", self)
        self.save_contacts = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/disk.png"), "Snimi", self)
        self.add_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj", self)
        self.remove_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Obrisi", self)
        self.hbox_layout.addWidget(self.open_contacts)
        self.hbox_layout.addWidget(self.save_contacts)
        self.hbox_layout.addWidget(self.add_button)
        self.hbox_layout.addWidget(self.remove_button)
        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        #self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)


        self.open_contacts.clicked.connect(self._on_open)
        self.save_contacts.clicked.connect(self._on_save)
        self.add_button.clicked.connect(self._on_add)
        self.remove_button.clicked.connect(self._on_remove)

        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

        self.actions_dict = {
            "add": QtWidgets.QAction(QtGui.QIcon("resources/icons/plus.png"), "Dodaj", self)
        }


    def set_model(self, model):
        """
        Postavlja novi model na tabelarni prikaz.

        :param model: model koji se prikazuje u tabeli.
        :type model: ContactsModel
        """
        self.table_view.setModel(model)

    def _on_open(self):
        """
        Metoda koja se poziva na klik dugmeta open.
        """
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Open contacts file", ".", "CSV Files (*.csv)")
        self.set_model(ContactsModel(path[0]))

    def _on_save(self):
        """
        Metoda koja se poziva na klik dugmeta save.
        """
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save contacts file", ".", "CSV Files (*.csv)")
        self.table_view.model().save_data(path[0])

    def _on_add(self):
        """
        Metoda koja se poziva na klik dugmeta add.
        Otvara dijalog sa formom za kreiranje novog korisnika u imeniku.
        """
        dialog = AddContactDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_view.model().add(dialog.get_data())

    def _on_remove(self):
        """
        Metoda koja se poziva na klik dugmeta remove.
        """
        self.table_view.model().remove(self.table_view.selectedIndexes())
