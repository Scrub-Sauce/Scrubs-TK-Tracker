#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.1"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

from module.Teamkill import Teamkill

class User(object):
    # Constructs the User object
    def __init__(self, userID, userName, nickname):
        self.userID = userID
        self.userName = userName
        self.nickname = nickname
        self.killList = []

    # Gets the UserID
    def getUserID(self):
        return self.userID

    # Gets the Username
    def getUserName(self):
        return self.userName

    # Gets the Nickname
    def getNickName(self):
        return self.nickname

    # Gets the list of past teamkills
    def getKillList(self):
        return self.killList

    # Sets the UserID
    def setUserID(self, userID):
        self.userID = userID

    # Sets the Username
    def setUserName(self, userName):
        self.userName = userName

    # Sets the Nickname
    def setNickname(self, nickname):
        self.nickname = nickname

    # Sets the list of past kills
    def setKillList(self, killList):
        self.killList = killList

    # Adds a Team kill to the list of Team kills
    def addTK(self, teamkill):
        self.getKillList().append(teamkill)

    # Checks the User's personal score
    def userScore(self):
        userScoreRet = "{0} - {1} has a total of {2} TKs.\n" \
            .format(self.getUserName(),self.nickname,len(self.killList))
        return userScoreRet

    # Creates a string representation of the User Object
    def toString(self):
        user_ret = "{0} - {1} has a total of {2} TKs.\n" \
            .format(self.getUserName(),self.nickname,len(self.killList))
        for teamkill in self.killList:
             user_ret += teamkill.toString() + "\n"
        return user_ret