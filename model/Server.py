class Server(object):
    def __init__(self, server_name, server_id, owner_id):
        self.__auto_id = None
        self.__server_name = server_name
        self.__server_id = server_id
        self.__owner_id = owner_id

    def get_auto_id(self):
        return self.__auto_id

    def get_server_name(self):
        return self.__server_name

    def get_server_id(self):
        return self.__server_id

    def get_owner_id(self):
        return self.__owner_id

    def set_auto_id(self, auto_id):
        self.__auto_id = auto_id

    def set_server_name(self, server_name):
        self.__server_name = server_name

    def set_server_id(self, server_id):
        self.__server_id = server_id

    def set_owner_id(self, owner_id):
        self.__owner_id = owner_id

    def __str__(self):
        return f'Auto_id: {self.get_auto_id()}\nServer Name: {self.get_server_name()}\nServer ID: {self.get_server_id()}\nOwner ID: {self.get_owner_id()}\n'
