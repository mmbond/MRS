from PySide2 import QtWidgets, QtGui, QtCore 
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...hall.hall import Hall
import sqlite3 
class AddHallDialog(QtWidgets.QDialog):
    """
    Dijalog za dodavanje nove hale.
    """
    def __init__(self, parent=None):
        """ 
        Inicijalizator dijaloga za dodavanje novog hale.

        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj halu")
        self.setWindowIcon(QIcon("resources/icons/plus.png")) 
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.places_total_input = QtWidgets.QSpinBox(self)
        self.places_total_input.setGeometry(QtCore.QRect(400, 50, 101, 22))
        self.places_total_input.setMaximum(100000)
        self.places_total_input.setSingleStep(100)
        
        self.hall_type = QtWidgets.QComboBox(self)
        self.hall_type.addItem("sobna temperatura (19°C do 25°C)")
        self.hall_type.addItem("rashladna hala (1°C do 18°C)")
        self.hall_type.addItem("hala za zamrzavanje (-10°C do 0°C)")
        
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        
        
        self.form_layout.addRow("Mesta u hali:", self.places_total_input)
        
        self.form_layout.addRow("Tip Hale: ", self.hall_type)
        
        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)
        self.new_hall = None

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. 
        Ukoliko neko polje nije popunjeno korisniku se prikazuje upozorenje.
        """
        if self.places_total_input.text() == "0":
            QtWidgets.QMessageBox.warning(self, 
            "Provera ukupno mesta", "Polje mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return
        elif int(self.places_total_input.text()) > 100000:
            QtWidgets.QMessageBox.warning(self, 
            "Provera ukupno mesta", "Polje mora biti manje od 100000!", QtWidgets.QMessageBox.Ok)
            return
        elif int(self.places_total_input.text()) % 100 != 0:
            QtWidgets.QMessageBox.warning(self, 
            "Provera ukupno mesta", "Polje mora biti deljiv sa 100!", QtWidgets.QMessageBox.Ok)
            return
        self.new_hall = self.get_hall()
        self.accept()
        
    def _hall_type(self, hall_type):
        """
        Metoda koja dobavlja podatke tabele i vraća kojeg je tipa hala.

        :param type: tip hale može biti određeni tekst
        :type ps: str
        :returns: int -- tip hale 1,2,3
        """   
        if hall_type == "sobna temperatura (19°C do 25°C)":
            return 1
        elif hall_type == "rashladna hala (1°C do 18°C)":
            return 2
        else:
            return 3

    def get_hall(self):
        """
        Metoda koja dobavlja podatke tabele i inicializuje halu.

        :returns: Hall -- nova kreirana hala.
        """   
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        for i in  c.execute('SELECT seq FROM sqlite_sequence WHERE name = "halls"'):
            number = int(str(i).replace("(","").replace(",)","").replace("('","").replace("',)",""))
        conn.commit()
        conn.close() 

        return Hall("Hala " + str(number+1), 0, int(self.places_total_input.text()), self._hall_type(self.hall_type.currentText()))



