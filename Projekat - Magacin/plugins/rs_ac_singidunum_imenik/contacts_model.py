from PySide2 import QtCore
import csv
import os


class ContactsModel(QtCore.QAbstractTableModel):
    """
    Klasa koja predstavlja specijalizaciju QAbstractTableModel-a.
    Koristimo tabelarni model, jer cemo podatke posmatrati kao tabelu, i u tabeli ih prikazivati.
    Svaki tabelarni model ima redove i kolone. Red je jedan korisnik u imeniku, a kolone predstavalju
    korisnikove pojedinacne podatke, poput imena, prezimena itd.
    Datoteka na osnovu koje se populise model je CSV datoteka, gde su redovi modela zapravo redovi
    iz datoteke, a kolone modela, su podaci koji su u redu u datoteci odvojeni separatorom (zarezom).
    """
    def __init__(self, path=""):
        """
        Inicijalizator modela za kontakte.
        Pri inicijalizaciji se na osnovu datoteke sa putanje path ucitavaju i populise se model.

        :param path: putanja do datoteke u kojoj su smesteni podaci.
        :type path: str
        """
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._data = []
        self.load_data(path)

    def rowCount(self, index):
        """
        Vraca broj redova u modelu.

        :param index: putanja do datoteke u kojoj su smesteni podaci.
        :type index: QModelIndex
        :returns: int -- broj redova modela.
        """
        return len(self._data)

    def columnCount(self, index):
        """
        Vraca broj kolona u modelu. Posto znamo da nas korisnik iz imenika je opisan sa pet
        podataka, vracamo fiksni broj kolona na osnovu datoteke.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: int -- broj kolona modela.
        """
        return 5

    def data(self, index, role):
        """
        Vraca podatak smesten na datom indeksu sa datom ulogom.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :param role: putanja do datoteke u kojoj su smesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: object -- podatak koji se nalazi na zadatom indeksu sa zadatom ulogom.
        """
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element
    
    def headerData(self, section, orientation, role):
        """
        Vraca podatak koji ce popuniti sekciju zaglavlja tabele.

        :param section: sekcija koja u zavisnosti od orijentacije predstavlja redni broj kolone ili reda.
        :type section: int
        :param orientation: odredjuje polozaj zaglavlja.
        :type orientation: QtCore.Qt.Vertical ili QtCore.Qt.Horizontal
        :param role: putanja do datoteke u kojoj su smesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: str -- naziv sekcije zaglavlja.
        """
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "Ime"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Prezime"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Telefon"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Email"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "Datum rodjenja"

    def setData(self, index, value, role):
        """
        Postavlja vrednost na zadatom indeksu.
        Ova metoda je vazna ako zelimo da nas model moze da se menja.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :param value: nova vrednost koju zelimo da postavimo.
        :type value: str -- vrednost koja ce biti dodeljena, za sada radimo samo sa stringovima
        :param role: putanja do datoteke u kojoj su smesteni podaci.
        :type role: QtCore.Qt.XXXRole (gde je XXX konkretna uloga)
        :returns: bool -- podatak o uspesnosti izmene.
        """
        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def flags(self, index):
        """
        Vraca flagove koji su aktivni za dati indeks modela.
        Ova metoda je vazna ako zelimo da nas model moze da se menja.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- flagovi koji treba da budu aktivirani.
        """
        # ne damo da menja datum rodjenja (primera radi)
        if index.column() != 4: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        # sve ostale podatke korisnik moze da menja
        else: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def get_element(self, index : QtCore.QModelIndex):
        """
        Dobavlja podatak smesten na zadatom indeksu, ako je indeks validan.
        Pomocna metoda nase klase.

        :param index: indeks elementa modela.
        :type index: QModelIndex
        :returns: object -- vrednost na indeksu.
        """
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def remove(self, indices):
        """
        Uklanja elemente iz modela na zadatim indeksima. Mozemo uklanjati vise redova (korisnika) iz imenika
        u jednom pozivu metode.
        Pomocna metoda nase klase.

        :param indices: indeks elementa modela.
        :type indices: list -- lista QModelIndex-a.
        """
        # za na osnovu indeksa, dobijamo njihove redove, posto za jedan red je vezano pet indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo od nazad, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()

    def add(self, data : dict):
        """
        Dodaje novog korisnika (red matrice) u model.
        Pomocna metoda nase klase.

        :param data: indeks elementa modela.
        :type data: dict -- podaci o novom korisniku.
        """
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data["name"], data["surname"], data["phone"], data["email"], data["birthday"]])
        self.endInsertRows()

    def load_data(self, path=""):
        """
        Ucitava podatke iz CSV datoteke na zadatoj path putanji uz pomoc CSV reader-a.
        Pomocna metoda nase klase.

        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "r", encoding="utf-8") as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def save_data(self, path=""):
        """
        Zapisuje podatke iz modela u datoteku na zadatoj path putanji uz pomoc CSV writer-a.
        Pomocna metoda nase klase.

        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for row in self._data:
                writer.writerow(row)
            #writer.writerows(self._data)
