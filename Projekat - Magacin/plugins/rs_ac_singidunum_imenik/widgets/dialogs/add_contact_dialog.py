from PySide2 import QtWidgets, QtCore, QtGui

class AddContactDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje novog kontakta u imenik.
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za dodavanje novog kontakta u imenik.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj kontakt")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.name_input = QtWidgets.QLineEdit(self)
        self.surname_input = QtWidgets.QLineEdit(self)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.email_input = QtWidgets.QLineEdit(self)
        self.birthday_input = QtWidgets.QDateEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        self.email_re = QtCore.QRegExp(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", QtCore.Qt.CaseInsensitive)
        self.email_validator = QtGui.QRegExpValidator(self.email_re)
        self.email_input.setValidator(self.email_validator)
        self.email_input.textChanged.connect(self.adjust_text_color)

        self.birthday_input.setDate(QtCore.QDate.currentDate())
        self.birthday_input.setCalendarPopup(True)
        self.form_layout.addRow("Ime:", self.name_input)
        self.form_layout.addRow("Prezime:", self.surname_input)
        self.form_layout.addRow("Telefon:", self.phone_input)
        self.form_layout.addRow("Email:", self.email_input)
        self.form_layout.addRow("Datum rodjenja:", self.birthday_input)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def adjust_text_color(self):
        """
        Metoda koja spram validnosti email inputa menja boju njegovog oboda i teksta.
        Crveno kada je nevalidan input, crno kada je validan.
        """
        if not self.email_input.hasAcceptableInput():
            self.email_input.setStyleSheet("QLineEdit { color: red;}")
        else:
            self.email_input.setStyleSheet("QLineEdit { color: black;}")

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. Ukoliko neko polje nije popunjeno korisniku se 
        prikazuje upozorenje.
        """
        if self.name_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provera imena", "Ime mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return
        if self.surname_input.text() == "":
            QtWidgets.QMessageBox.warning(self, 
            "Provera prezimena", "Prezime mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return
        if not self.email_input.hasAcceptableInput():
            QtWidgets.QMessageBox.warning(self, 
            "Provera emaila", "Format emaila nije korektan!", QtWidgets.QMessageBox.Ok)
            return
        self.accept()
    def get_data(self):
        """
        Dobavlja podatke iz forme.

        :returns: dict -- recnik sa podacima iz forme.
        """
        return {
            "name": self.name_input.text(),
            "surname": self.surname_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "birthday": self.birthday_input.text()
        }
    



