class Person:
    def __init__(self, firstname, lastname):
        self._firstname = firstname
        self._lastname = lastname

    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    @property
    def lastname(self):
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @property
    def name(self):
        return self._firstname + " " + self._lastname

    @name.setter
    def name(self, value):
        fl = value.split(" ")
        if len(fl) < 2:
            print("Nevalidno ime!")
            return
        self._firstname = fl[0]
        self._lastname = fl[1]