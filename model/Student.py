class Student(object):

    def __init__(self, student_id, name, address):
        self.__student_id = str(student_id)
        self.__name = str(name)
        self.__address = str(address)

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address
