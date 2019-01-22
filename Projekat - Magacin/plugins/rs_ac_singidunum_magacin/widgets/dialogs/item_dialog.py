from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...item.item_service import ItemService
from .add_item_dialog import AddItemDialog
from ...item.item import Item

class ItemDialog(QtWidgets.QDialog):
    """ 
    Klasa koja predstavlja dialog u kojoj se prikazuje lista proizvoda
    """
    def __init__(self, selected_hall, parent=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz proizvoda.

        :param selected_hall: selektovana hala
        :type hall: Hall
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle("Proizvodi")
        # prosiriv ekran velicina
        self.resize(800,750)
        # postavljanje ikonice prozora
        self.setWindowIcon(QIcon("resources/icons/address-book-blue.png")) 

        items = ItemService()
        self.index = selected_hall.name.split(" ")[1]
        items.load_items(self.index)
        self.item_service = items
        self.hall = selected_hall

        self.item_dialog_layout = QtWidgets.QVBoxLayout()

        self.items_table = QtWidgets.QTableWidget(self)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.horizontalHeader().setVisible(True)
        self.items_table.horizontalHeader().setSortIndicatorShown(True)
        self.items_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.items_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.items_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.items_table.setGridStyle(Qt.SolidLine)
        self.items_table.setAlternatingRowColors(True)

        # popunjavamo toolbar
        self._set_toolbar()

        self._populate_table()

        self.items_table.horizontalHeader().setStretchLastSection(True)
        
        self.item_dialog_layout.addLayout(self.item_options_layout)
        self.item_dialog_layout.addWidget(self.items_table)
        
        
        self.setLayout(self.item_dialog_layout)

        self._bind_actions()
        self.items_table.setSortingEnabled(True)

    def _set_toolbar(self):
        """
        Populise toolbar sa korisnim funkcijama.
        """
        self.item_options_layout = QtWidgets.QHBoxLayout()
        
        self.add_item = QtWidgets.QPushButton(QIcon("resources/icons/application-plus.png"), "Dodaj proizvod")
        self.delete_item = QtWidgets.QPushButton(QIcon("resources/icons/minus-circle.png"), "Ukloni")
        self.plugin_dialog_layout = QtWidgets.QVBoxLayout()

        self.item_options_layout.addWidget(self.add_item)
        self.item_options_layout.addWidget(self.delete_item)
        
    def _populate_table(self):
        """
        Populiše tabelu sa podacima za proivod.
        """
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(
            ["Ime proizvoda", "Rok upotrebe", "Temperatura za cuvanje", "Kolicina", "Hala"])
        self.items_table.setRowCount(len(self.item_service.items))
        self.items_table.setColumnWidth(0, 200)
        self.items_table.setColumnWidth(2, 220)
        for i, item in enumerate(self.item_service.items):
            name = QtWidgets.QTableWidgetItem(item.name)
            expiration_date = QtWidgets.QTableWidgetItem(item.expiration_date)
            item_count = QtWidgets.QTableWidgetItem(str(item.item_count))
            temperature = QtWidgets.QTableWidgetItem(str(item.temperature))
            hall_id = QtWidgets.QTableWidgetItem(str(item.hall_id))

            self.items_table.setItem(i, 0, name)
            self.items_table.setItem(i, 1, expiration_date)
            self.items_table.setItem(i, 2, temperature)
            self.items_table.setItem(i, 3, item_count)
            self.items_table.setItem(i, 4, hall_id)

    def _bind_actions(self):
        """
        Uvezuje akcije sa funkcijama koje se izvrsavaju na njihovo okidanje.
        """
        self.add_item.clicked.connect(self._on_add)
        self.delete_item.clicked.connect(self._on_delete)

    def _on_add(self):
        """
        Metoda koja dodaje proizvod.
        Može da daoda novi proivod ili samo da poveća količinu tog proizvoda.
        """
        self.items_table.setSortingEnabled(False)
        dialog = AddItemDialog(self.hall)
        answer = dialog.exec_()
        if answer != 0:
            obj = dialog.new_item
            provera = self.item_service.create(obj,self.index)
            if provera:
                self.item_service.add_item(obj)
            else:
                index = self.item_service.items.index(obj)
                self.item_service.edit_item(self.item_service.items[index])
            self.hall.places_filled += obj.item_count
            self._populate_table()
            QtWidgets.QMessageBox.information(self, "Proizvod unet", "Proizvod uspešno unet", QtWidgets.QMessageBox.Ok)
        self.items_table.setSortingEnabled(True)

    def _on_delete(self):
        """
        Metoda koja briše proivod koji je odabran.
        Može da obriše ceo proivod ili samo da smanji količinu tog proizvoda.
        """
        self.items_table.setSortingEnabled(False)
        selected_item = self.items_table.selectedItems()
        if len(selected_item) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obavestenje", "Odaberite proizvod", QtWidgets.QMessageBox.Ok)
        item = self.get_item(selected_item)
        item_reduce, ok = QtWidgets.QInputDialog.getInt(self, "Ukloni kolicinu","Kolicina:", 1, 0, item.item_count, 1)
        if ok:
            if item_reduce == item.item_count:
                provera = self.item_service.delete(item)
                if provera:
                    self.item_service.delete_item(item)
                    self.hall.places_filled -= item.item_count
                    self._populate_table()
                    QtWidgets.QMessageBox.information(self, "Proizvod obrisan", "Proizvod uspešno obrisana", QtWidgets.QMessageBox.Ok)
            else:
                item.item_count -= item_reduce
                self.item_service.edit(item)
                self.item_service.edit_item(item)
                self.hall.places_filled -= item_reduce
                self._populate_table()
        self.items_table.setSortingEnabled(True)
        
    def get_item(self, item):
        """
        Dobavlja podatke iz tabele.
        
        :param item: selektovan red, proizvod
        :type item: QItem
        :returns: Item -- inicializuje proizvod.
        """   
        name = item[0].text()
        expiration_date = item[1].text()
        temperature = int(item[2].text())
        item_count = int(item[3].text())
        hall_id = int(item[4].text())

        return Item(name, expiration_date, temperature, item_count, hall_id)
    