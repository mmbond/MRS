import sqlite3
from ..hall.hall import Hall

class HallService:
    """
    Klasa koja manipulise nad halama (halls) u prosirivom okviru. Sluzi kao service sloj.
    """
    def __init__(self):
        """
        Inicijalizator servisne klase za hale.
        """
        self._halls = list()

    def create(self, hall):
        """
        Dodaje halu.
        
        :param hall: instanca hale koju
        :type hall: Hall
        :returns: bool -- podatak o uspesnosti dodavanja.
        """
        if hall not in self._halls:
            self._halls.append(hall)
            return True
        
        return False

    def delete(self, hall):
        """
        Briše halu.

        :param hall: instanca hale koju dodajemo.
        :type hall: Hall
        :returns: bool -- podatak o uspesnosti dodavanja.
        """
        if hall in self._halls:
            self._halls.remove(hall)
            return True
        return False

    @property
    def halls(self):
        """
        Property za dobavljanje liste hala.
        """
        return self._halls
             
    def load_halls(self):
        """
        Očitava sve podatke iz sqlite baze. 
        Pravi instance hala koje se dodaju u listu hala.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        for hid,name,places_filled,places_total,hall_type in c.execute('SELECT * FROM halls'):
            obj = Hall(name,places_filled,places_total,hall_type)
            self.create(obj)  
        conn.close()

    def add_hall(self, hall):
        """
        Dodaje halu u sqlite baze. 
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('INSERT INTO halls (name,places_filled,places_total,hall_type) VALUES (?,?,?,?)', hall.get_db_data()) 
        conn.commit()
        conn.close()

    def delete_hall(self, hall):
        """
        Briše halu iz sqlite baze. Takođe, briše i sve proizvode koji se nalaze u hali.
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('DELETE FROM halls WHERE name = ?', (hall.name,)) 
        c.execute('DELETE FROM items WHERE hall_id = ?', (hall.name.split(" ")[1],)) 
        conn.commit()
        conn.close()
        
    def edit_hall(self, hall):
        """
        Menja popunjenost hale u sqlite bazi.  
        """
        conn = sqlite3.connect('plugins\\rs_ac_singidunum_magacin\\db\\warehouse.db')
        c = conn.cursor()
        c.execute('UPDATE halls SET places_filled = ? WHERE name = ?', (hall.places_filled, hall.name)) 
        conn.commit()
        conn.close()
    
