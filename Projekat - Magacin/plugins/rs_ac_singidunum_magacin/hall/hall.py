class Hall:
    """
    Ova klasa predstavlja osnovu za svaku konkretnu halu.
    """
    def __init__(self, name, places_filled, places_total, hall_type):
        """
        Inicijalizator.

        :param name: ime hale koje je naziv hala i id te hale
        :type name: str
        :param places_filled: popunjeno mesta u hali
        :type places_filled: int
        :param places_total: ukupno mesta u hali
        :type places_total: int
        :param hall_type: tip hale moze biti 1,2,3
        :type hall_type: int
        """
        self._name = name
        self._places_filled = places_filled
        self._places_total = places_total
        self._hall_type = hall_type
 
    @property
    def name(self):
        """
        Property za dobavljanje imena hale.
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def places_filled(self):
        """
        Property za dobavljanje koliko je popunjeno mesta u hali.
        """
        return self._places_filled

    @places_filled.setter
    def places_filled(self, value):
        """
        Setter za postavljanje koliko je popunjeno mesta u hali.
        """
        self._places_filled = value
    
    @property
    def places_total(self):
        """
        Property za dobavljanje ukupno mesta iz hale.
        """
        return self._places_total

    @places_total.setter
    def places_total(self, value):
        """
        Setter za postavljanje ukupno mesta iz hale.
        """
        self._places_total = value

    @property
    def hall_type(self):
        """
        Property za dobavljanje tipa hale.
        """
        return self._hall_type

    @hall_type.setter
    def hall_type(self, value):
        """
        Setter za postavljanje tipa hale.
        """
        self._hall_type = value
    
    def __eq__(self, other):
        """
        Equal metoda za rad prilikom poređenja hala. Porede se po imenu.
        """
        return self._name == other._name
    
    def __hash__(self):
        """
        Hash metoda za rad prilikom poređenja.
        """
        return hash((self._name))

    def get_db_data(self):
        """
        Metoda koja daje vrednosti za dobavljanje podataka iz baze.
        """
        return (self.name, self.places_filled, self.places_total, self.hall_type)