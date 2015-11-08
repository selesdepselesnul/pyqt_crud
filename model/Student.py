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

    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @property
    def address(self):
        return self.__address


