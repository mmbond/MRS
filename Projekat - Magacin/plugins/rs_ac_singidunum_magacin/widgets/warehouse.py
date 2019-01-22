from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from .dialogs.add_hall_dialog import AddHallDialog
from .dialogs.item_dialog import ItemDialog
from ..hall.hall import Hall

class Warehouse(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor dodatka (magacin)

    """
    def __init__(self, halls, parent: QtWidgets.QWidget=None):
        """
        Inicijalizator za prozor.

        :param halls: hall servis koji nam obezbedjuje operacije nad halama.
        :type halls: HallService
        :param parent: roditelj glavnog prozora (default: None).
        :type parent: QWidget
        """
        # pozivanje super inicijalizatora
        super().__init__(parent) 
        
        # cuvanje atributa za hall servise
        self.hall_service = halls

        # centralni widget je mesto deo glavnog prozora u koji treba da se smesti glavni widget aplikacije
        self.centralwidget = QtWidgets.QWidget(self)

        # layout kako bi namestili table        
        self.halls_dialog_layout = QtWidgets.QGridLayout(self.centralwidget)
        # table widget
        self.halls_table = QtWidgets.QTableWidget(self.centralwidget)
        self.halls_table.verticalHeader().setVisible(False)
        self.halls_table.horizontalHeader().setVisible(True)
        self.halls_table.horizontalHeader().setSortIndicatorShown(True)
        self.halls_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.halls_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.halls_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.halls_table.setGridStyle(Qt.SolidLine)
        self.halls_table.setAlternatingRowColors(True)

        # popunjavamo tabelu sa podacima
        self._populate_table()
        self.halls_table.horizontalHeader().setStretchLastSection(True)

        self.halls_dialog_layout.addWidget(self.halls_table, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.halls_table.setSortingEnabled(True)

        # popunjavamo toolbar
        self._set_toolbar()
        # pozivanje sopstvenih privatnih metoda
        self._bind_actions()
        self.halls_table.setFocusPolicy(Qt.ClickFocus)

    def _set_toolbar(self):
        """
        Populiše toolbar sa korisnim funkcijama.
        """
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.add_hall = QtWidgets.QAction(self)
        self.add_hall.setIcon(QIcon("resources/icons/plus.png"))
        self.delete_hall = QtWidgets.QAction(self)
        self.delete_hall.setIcon(QIcon("resources/icons/minus.png"))
        self.item_hall = QtWidgets.QAction(self)
        self.item_hall.setIcon(QIcon("resources/icons/category-item.png"))
        self.toolBar.addAction(self.add_hall)
        self.toolBar.addAction(self.delete_hall)
        self.toolBar.addAction(self.item_hall)
        self.add_hall.setText("Dodaj Halu")
        self.add_hall.setToolTip("Dodaj Halu")
        self.delete_hall.setText("Obriši Halu")
        self.delete_hall.setToolTip("Obriši Halu")
        self.item_hall.setText("Otvori listu proizvoda")
        self.item_hall.setToolTip("Otvori listu proizvoda")

    def _populate_table(self):
        """
        Populiše tabelu sa podacima za halu.
        """
        self.halls_table.clear()
        self.halls_table.setColumnCount(4)
        self.halls_table.setHorizontalHeaderLabels(
               ["Ime hale", "Popunjena Mesta", "Kapacitet hale", "Tip hale"])
        self.halls_table.setColumnWidth(1, 150)
        self.halls_table.setColumnWidth(2, 150)
        self.halls_table.setRowCount(len(self.hall_service.halls))
        for i, hall in enumerate(self.hall_service.halls):
            name = QtWidgets.QTableWidgetItem(hall.name)
            places_total = QtWidgets.QTableWidgetItem(str(hall.places_total))
            places_filled = QtWidgets.QTableWidgetItem(str(hall.places_filled))
            hall_type =  self._hall_type(hall.hall_type)
            hall_type = QtWidgets.QTableWidgetItem(hall_type)

            self.halls_table.setItem(i, 0, name)
            self.halls_table.setItem(i, 1, places_filled)
            self.halls_table.setItem(i, 2, places_total)
            self.halls_table.setItem(i, 3, hall_type)

    def _bind_actions(self):
        """
        Uvezuje akcije sa funkcijama koje se izvršavaju na njihovo pokretanje.
        """
        self.add_hall.triggered.connect(self._on_add)
        self.delete_hall.triggered.connect(self._on_delete)
        self.item_hall.triggered.connect(self._on_item)
    
    def _on_add(self):
        """
        Metoda koja dodaje halu.
        """
        self.halls_table.setSortingEnabled(False)
        dialog = AddHallDialog()
        answer = dialog.exec_()
        if answer != 0:
            provera = self.hall_service.create(dialog.new_hall)
            if provera:
                self._populate_table()
                self.hall_service.add_hall(dialog.new_hall)
                QtWidgets.QMessageBox.information(self, "Obaveštenje", "Hala uspešno uneta", QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Hala nije uneta", QtWidgets.QMessageBox.Ok)            
        self.halls_table.setSortingEnabled(True)    
        
    def _on_item(self):
        """
        Metoda koja poziva odgovarajuću listu proizvoda u zavisnosti od hale.
        """
        self.halls_table.setSortingEnabled(False)   
        selected_hall = self.halls_table.selectedItems()
        if len(selected_hall) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite halu", QtWidgets.QMessageBox.Ok)
        hall = self.get_hall(selected_hall)
        index = self.hall_service.halls.index(hall)
        selected_hall = self.hall_service.halls[index]
        dialog = ItemDialog(selected_hall)
        dialog.exec_()
        self.hall_service.edit_hall(dialog.hall)
        self._populate_table()
        self.halls_table.setSortingEnabled(True)   


    def _on_delete(self):
        """
        Metoda koja briše halu koja je odabrana iz tabele hala.
        """
        self.halls_table.setSortingEnabled(False)
        selected_hall = self.halls_table.selectedItems()
        if len(selected_hall) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite halu", QtWidgets.QMessageBox.Ok)
        hall = self.get_hall(selected_hall)
        provera = self.hall_service.delete(hall)
        if provera:
            self._populate_table()
            self.hall_service.delete_hall(hall)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Hala uspešno obrisana", QtWidgets.QMessageBox.Ok)
        self.halls_table.setSortingEnabled(True)    
        

    def _hall_type(self, type):
        """
        Metoda koja vraća tačan tip hale u tabelu.

        :returns: str -- tip hale u celom nazivu.
        """
        if type == 1:
            return "sobna temperatura (19°C do 25°C)" 
        elif type == 2:
            return "rashladna hala (1°C do 18°C)"
        else:
            return "hala za zamrzavanje (-10°C do 0°C)"

    def get_hall(self, hall):
        """
        Metoda koja dobavlja podatke iz tabele.

        :returns: Hall -- inicializuje halu.
        """ 
        return Hall(hall[0].text(), int(hall[1].text()), int(hall[2].text()), hall[3].text())
        



