import sqlite3
from ..item.item import Item

class ItemService:
    """
    Klasa koja manipulise nad proizvodima (item) u prosirivom okviru.
    """
    def __init__(self):
        """
        Inicijalizator servisne klase za proizvode.
        """
        self._items = list()
        

    def create(self, item, index):
        """
        Kreira proizvod. Zavisnosti da li je vec postoji kreira se ili se samo povecava količina.

        :param item: instanca item koju dodajemo.
        :type item: Item
        :param index: id hale u kojoj se dodaje proizvod.
        :type ps: int
        :returns: bool -- podatak da li je kreiran ili promenjen proizvod.
        """
        if item.hall_id == int(index) and item in self._items:
            index = self._items.index(item)
            self._items[index].item_count += item.item_count
            return False
        elif item.hall_id == int(index) and item not in self._items:
            self._items.append(item)
            return True

    def delete(self, item):
        """
        Brise proizvod. Isti proizvod se ne moze brisati dva puta.

        :param item: instanca item koju brisemo.
        :type item: Item
        :returns: bool -- podatak o uspesnosti brisanja.
        """
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def edit(self, item):
        """
        Menja količinu proizovda.

        :param item: instanca item koju menjamo.
        :type item: Item
        """
        index = self._items.index(item)
        self._items[index].item_count = item.item_count

        
    @property
    def items(self):
        """
        Property za dobavljanje liste proizvoda.
        """
        return self._items 

    def load_items(self, index):
        """
        Očitava sve podatke iz sqlite baze. 
        Pravi instance proizvoda koje se dodaju u listu proizvoda za određenu halu.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        for iid,name, expiration_date, temperature, item_count, hall_id in c.execute('SELECT * FROM items'):
            obj = Item(name, expiration_date, temperature, item_count, hall_id)
            self.create(obj,index)   
        conn.close()

    def add_item(self, item):
        """
        Dodaje proizvod u sqlite baze. Takođe, azurira popunjenost hale u kojoj se porizvod nalazi.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('INSERT INTO items (name, expiration_date, temperature, item_count, hall_id) VALUES (?,?,?,?,?)', item.get_db_data()) 
        c.execute('UPDATE halls SET places_filled = places_filled + ? WHERE hall_id = ?', (item.item_count, item.hall_id)) 
        conn.commit()
        conn.close()
    
    def delete_item(self, item):
        """ed
        Briše proizvod iz sqlite baze. Takođe, azurira popunjenost hale u kojoj se porizvod nalazi.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('DELETE FROM items WHERE name = ? and temperature = ? and expiration_date = ?', (item.name,item.temperature,item.expiration_date)) 
        c.execute('UPDATE halls SET places_filled = places_filled - ? WHERE hall_id = ?', (item.item_count, item.hall_id)) 
        conn.commit()
        conn.close()

    def edit_item(self, item):
        """
        Menja broj proizvoda u sqlite bazi.  
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('UPDATE items SET item_count = ? WHERE name = ? and expiration_date = ? and temperature = ? ', (item.item_count, item.name,item.expiration_date, item.temperature)) 
        conn.commit()
        conn.close()

    