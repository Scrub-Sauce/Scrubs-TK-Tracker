#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.1"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

import csv
from module.User import User
from module.Teamkill import Teamkill

class Scoreboard:
    # Constructs the Scoreboard
    def __init__(self):
        self.userList = []

    # Gets the Scoreboards list of users
    def getUserList(self):
        return self.userList

    # Sets the Scoreboards list of users
    def setUserList(self, userList):
        self.userList = userList

    # Loads the Scoreboard by reading in information from data.csv
    def LoadScoreboard(self):
        with open('data.csv', 'r') as scoreboardData:
            scan = csv.reader(scoreboardData)
            for line in scan:
                tmpUser = User(line[0],line[1],line[2])
                for x in range(3,len(line)):
                    entry = line[x].split('\\')
                    tmpTK = Teamkill(line[2],entry[0],entry[1])
                    tmpUser.addTK(tmpTK)
                self.addUser(tmpUser)

    # Adds a new Team Kill to a User's history and score
    def newTK(self, userID, userName, nickname, victim, pDate):
        userFound = False
        for user in self.userList:
            if user.getUserID() == userID:
                tmpTK = Teamkill(nickname, victim, pDate)
                userFound = True
                user.addTK(tmpTK)
                print(userFound)
        if userFound == False:
            tmpUser = User(userID,userName,nickname)
            tmpUser.addTK(Teamkill(nickname,victim,pDate))
            self.addUser(tmpUser)
            print(tmpUser)
        self.updateCSV()

    # Removes a Team kill from a User's history and score
    def removeTK(self, userID, nickname, victim, pDate):
        for user in self.userList:
            if userID == user.getUserID():
                for kill in user.getKillList():
                    if nickname == kill.getKiller() and victim == kill.getVictim() and pDate == kill.getPDate():
                        user.getKillList().remove(kill)
                        self.updateCSV()
                        return "" + kill.toString() + " was removed."
                return "Teamkill not found. Check date syntax. For more information check !help"

    # Updates data.csv with all the stored scoreboard information
    def updateCSV(self):
        with open('data.csv','w', newline='') as scoreboardData:
            write = csv.writer(scoreboardData)
            for user in self.userList:
                tmpList = []
                tmpList.append(user.getUserID())
                tmpList.append(user.getUserName())
                tmpList.append(user.getNickName())
                for tk in user.getKillList():
                    tmpTK = "{0}\\{1}".format(tk.getVictim(),tk.getPDate())
                    tmpList.append(tmpTK)
                write.writerow(tmpList)

    # Adds a user to the scoreboard
    def addUser(self, user):
        self.userList.append(user)

    # Creates a string representation of the user's teamkill history
    def printUserStats(self, userID):
        userFound = False
        for user in self.userList:
            if userID == user.getUserID():
                userFound = True
                return user.toString()
        if userFound == False:
            return "You have no TKs yet."

    # Creates a string representation of the teamkill Score for use in discord
    def printScore(self):
        scoreRet = "\t\tTeam Kill Scoreboard!\n\n"
        for user in self.userList:
            scoreRet += "{0}".format(user.userScore())
        return scoreRet

    # Creates a string representation of the Scoreboard object *Easily exceeds 2,000 characters. Dont use to post in discord
    def toString(self):
        scoreboardRet = "\t\tTop Teamkiller Scoreboard!\n\n"
        for user in self.userList:
            scoreboardRet += "\n{0}".format(user.toString())
        return scoreboardRet
