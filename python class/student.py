from person import Person

class Student(Person):
    def __init__(self, firsname, lastname, index_number):
        super().__init__(firsname, lastname)
        self.index_number = index_number
