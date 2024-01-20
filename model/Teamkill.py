#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.2"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"


class Teamkill(object):
    # Constructs the Teamkill object
    def __init__(self, killer_id, victim_id, server_id, datetime):
        self.__auto_id = None
        self.__killer_id = killer_id
        self.__victim_id = victim_id
        self.__server_id = server_id
        self.__datetime = datetime
        self.__note = None

    def get_auto_id(self):
        return self.__auto_id

    def get_killer_id(self):
        return self.__killer_id

    def get_victim_id(self):
        return self.__victim_id

    def get_server_id(self):
        return self.__server_id

    # Gets the date of the kill
    def get_datetime(self):
        return self.__datetime

    def get_note(self):
        return self.__note

    def set_auto_id(self, auto_id):
        self.__auto_id = auto_id

    def set_killer_id(self, killer_id):
        self.__killer_id = killer_id

    def set_victim_id(self, victim_id):
        self.__victim_id = victim_id

    def set_server_if(self, server_id):
        self.__server_id = server_id

    # Sets the date of the kill
    def set_datetime(self, datetime):
        self.__datetime = datetime

    def set_note(self, note):
        self.__note = note

    def __str__(self):
        return f"Auto_id: {self.get_auto_id()}\nKiller_id: {self.get_killer_id()}\nVictim_id: {self.get_victim_id()}\nServer_id: {self.get_server_id()}\nDateTime: {self.get_datetime()}\nNote: {self.get_note()}\n"
