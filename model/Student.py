# author : Moch Deden (https://github.com/selesdepselesnul)
class Student(object):

    ACTIVE = 'Aktif'
    DEACTIVE = 'Tidak'

    def __init__(self, student_id, name, address, status=ACTIVE):
        self.__student_id = str(student_id)
        self.__name = str(name)
        self.__address = str(address)
        self.__status = str(status)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        self.__address = address


