#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.2"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"


class Teamkill(object):
    # Constructs the Teamkill object
    def __init__(self, killer_id, victim_id, datetime):
        self.__killer_id = killer_id
        self.__victim_id = victim_id
        self.__datetime = datetime

    def get_killer_id(self):
        return self.__killer_id

    def get_victim_id(self):
        return self.__victim_id

    # Gets the date of the kill
    def get_occurrence_date(self):
        return self.__datetime

    def set_killer_id(self, killer_id):
        self.__killer_id = killer_id

    def set_victim_id(self, victim_id):
        self.__victim_id = victim_id

    # Sets the date of the kill
    def set_datetime(self, datetime):
        self.__datetime = datetime
