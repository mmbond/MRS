class Item:
    """
    Ova klasa predstavlja osnovu za svaki konkretan proizvod.
    """
    def __init__(self, name, expiration_date, temperature, item_count, hall_id):
        """
        Inicijalizator.

        :param name: ime proizvoda
        :type name: str
        :param expiration_date: rok upotrebe proizvoda
        :type expiration_date: str
        :param temperature: temperatura na kojoj se čuva proizvod
        :type temperature: int
        :param item_count: količina proizvoda
        :type item_count: int
        :param hall_id: hala u kojoj se nalazi proizvod
        :type hall_id: int
        """
        self._name = name
        self._expiration_date = expiration_date
        self._temperature = temperature
        self._item_count = item_count
        self._hall_id = hall_id

    @property
    def hall_id(self):
        """
        Property za dobavljanje hale u kojoj se nalazi proizvod.
        """
        return self._hall_id

    @hall_id.setter
    def hall_id(self, value):
        """
        Setter za postavljanje hale u kojoj se nalazi proizvod.
        """
        self._hall_id = value
    
    @property
    def name(self):
        """
        Property za dobavljanje imena proizvoda.
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Setter za postavljanje imena proizvoda.
        """
        self._name = value
    

    @property
    def expiration_date(self):
        """
        Property za dobavljanje roka upotrebe proizvoda.
        """
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        """
        Setter za postavljanje roka upotrebe proizvoda.
        """
        self._expiration_date = value
    
    @property
    def temperature(self):
        """
        Property za dobavljanje temperature proizvoda.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """
        Setter za postavljanje temperature proizvoda.
        """
        self._temperature = value

    @property
    def item_count(self):
        """
        Property za dobavljanje količine proizvoda.
        """
        return self._item_count
    
    @item_count.setter
    def item_count(self, value):
        """
        Setter za postavljanje količine proizvoda.
        """
        self._item_count = value
    
    def __eq__(self, other):
        """
        Equal metoda za rad prilikom poređenja proizvoda. Porede se po imenu, roku upotrebe i temperaturi za čuvanje.
        """
        return self._name == other._name and self._expiration_date == other._expiration_date and self._temperature == other._temperature
    
    def __hash__(self):
        """
        Hash metoda za rad prilikom poređenja.
        """
        return hash((self._name,self._expiration_date))

    def get_db_data(self): 
        """
        Metoda koja daje vrednosti za dobavljanje podataka iz baze.
        """
        return (self.name, self.expiration_date, self.temperature, self.item_count, self.hall_id)