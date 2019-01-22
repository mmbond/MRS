from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...item.item import Item
import sqlite3

class AddItemDialog(QtWidgets.QDialog):
    """ 
    Dijalog za dodavanje novog proizvoda.
    """
    def __init__(self, hall, parent=None):
        """ 
        Inicijalizator dijaloga za dodavanje novog proivoda.

        :param hall: selektovana hala
        :type hall: Hall
        :param parent: roditeljski widget.
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setWindowTitle("Dodaj proizvod")
        self.setWindowIcon(QIcon("resources/icons/plus.png")) 

        self.resize(350, 256)
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(200, 200, 140, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        
        self.hall = hall

        self.item = QtWidgets.QLabel(self)
        self.item.setText("Ime proizvoda")
        self.item.setGeometry(QtCore.QRect(10, 30, 111, 16))
        self.item_name_input = QtWidgets.QComboBox(self)        
        self.item_name_input.setGeometry(QtCore.QRect(200, 20, 110, 22))       
        self._available_items()

        self.expiration_date = QtWidgets.QLabel(self)
        self.expiration_date.setText("Rok upotrebe")
        self.expiration_date.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.expiration_date_input = QtWidgets.QDateEdit(self)
        self.expiration_date_input.setGeometry(QtCore.QRect(200, 60, 110, 22))
        self.expiration_date_input.setMaximumDate(QtCore.QDate(2090, 12, 31))
        self.expiration_date_input.setCalendarPopup(True)
        self.expiration_date_input.setDate(QtCore.QDate.currentDate())
        self.expiration_date_input.setDisplayFormat("dd.MM.yyyy")

        self.item_count = QtWidgets.QLabel(self)
        self.item_count.setGeometry(QtCore.QRect(10, 100, 55, 16))
        self.item_count.setText("Količina")
        self.item_count_input = QtWidgets.QSpinBox(self)
        self.item_count_input.setGeometry(QtCore.QRect(200, 100, 110, 22))
        self.item_count_input.setMaximum(self.num_of_places())

        self.temperature = QtWidgets.QLabel(self)
        self.temperature.setGeometry(QtCore.QRect(10, 140, 171, 16))
        self.temperature.setText("Temperatura za čuvanje")
        self.temperature_input = QtWidgets.QSpinBox(self)
        self.temperature_input.setGeometry(QtCore.QRect(200, 130, 110, 22))
        self._set_temperature()

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.new_item = None

    def _on_accept(self):
        """
        Metoda koja se poziva kada se pritisne na dugme ok.
        Prvo proverava popunjenost forme. 
        Ukoliko neko polje nije popunjeno korisniku se prikazuje upozorenje.
        """
        if int(self.item_count_input.text()) <= 0: 
            QtWidgets.QMessageBox.warning(self, 
            "Provera ukupno mesta", "Polje Količina mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return
        elif int(self.item_count_input.text()) > int(self.num_of_places()): 
            QtWidgets.QMessageBox.warning(self, 
            "Provera ukupno mesta", "Nema toliko mesta! Preostalo: "+str(self.num_of_places()), QtWidgets.QMessageBox.Ok)
            return
        self.new_item = self.get_item()
        self.accept()   

    def _set_temperature(self):
        """
        Metoda koja odrešuje limit za temperaturu čuvanja proizvoda.
        """
        hall_type = self.hall.hall_type
        if hall_type == 1:
            self.temperature_input.setMinimum(19)
            self.temperature_input.setMaximum(25)
        elif hall_type == 2:
            self.temperature_input.setMinimum(1)
            self.temperature_input.setMaximum(18)
        else:
            self.temperature_input.setMinimum(-10)
            self.temperature_input.setMaximum(0)
           
    def num_of_places(self):
        """
        Metoda koja vraća koliko ima slobodnih mesta.

        :returns: int -- slobodna mesta.
        """
        return self.hall.places_total - self.hall.places_filled

    def _available_items(self):
        """
        Metoda koja iz baze izvlači moguće proivode koje možemo dodati.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        for i in  c.execute('SELECT name FROM available_items WHERE hall_type = ? ORDER BY name', str(self.hall.hall_type)):
            i = str(i).replace("('","").replace("',)","")
            self.item_name_input.addItem(i)
        conn.commit()
        conn.close()
    
    def get_item(self):
        """
        Dobavlja podatke iz forme.

        :returns: Item -- novi proizvod.
        """   
        return Item(self.item_name_input.itemText(self.item_name_input.currentIndex()),
                self.expiration_date_input.text(),
                int(self.temperature_input.text()),
                int(self.item_count_input.text()),
                int(self.hall.name.split(" ")[1]))
    