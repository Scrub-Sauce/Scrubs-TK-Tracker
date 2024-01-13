#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.2"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"


class User(object):
    # Constructs the User object
    def __init__(self, user_id, username, display_name, global_name, kill_count):
        self.__display_name = display_name
        self.__global_name = global_name
        self.__user_id = user_id
        self.__username = username
        self.__kill_count = kill_count

    # Gets the UserID
    def get_user_id(self):
        return self.__user_id

    # Gets the Username
    def get_username(self):
        return self.__username

    # Gets the display_name
    def get_display_name(self):
        return self.__display_name

    def get_global_name(self):
        return self.__global_name

    def get_kill_count(self):
        return self.__kill_count

    # Sets the UserID
    def set_user_id(self, user_id):
        self.__user_id = user_id

    # Sets the Username
    def set_username(self, username):
        self.__username = username

    # Sets the display name
    def set_display_name(self, display_name):
        self.__display_name = display_name

    def set_global_name(self, global_name):
        self.__global_name = global_name

    def set_kill_count(self, kill_count):
        self.__kill_count = kill_count

    # Creates a string representation of the User Object
    def __str__(self):
        user_ret = f"User ID: {self.get_user_id()}\nUsername: {self.get_username()}\nDisplay Name: {self.get_display_name()}\nGlobal Name: {self.get_global_name()}\nKill Count: {self.get_kill_count()}"
        return user_ret
