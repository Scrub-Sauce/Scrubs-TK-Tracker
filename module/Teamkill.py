#!/usr/bin/env python3

__author__ = "Kyle Anderson"
__version__ = "0.0.1"
__email__ = "kyleandersontx@gmail.com"
__maintainer__ = "Kyle Anderson"
__status__ = "Alpha"

class Teamkill(object):
    # Constructs the Teamkill object
    def __init__(self, killer, victim, pDate):
        self.killer = killer
        self.victim = victim
        self.pDate = pDate

    # Gets the Killers name
    def getKiller(self):
        return self.killer
    # Gets the Victims name
    def getVictim(self):
        return self.victim

    # Gets the date of the kill
    def getPDate(self):
        return self.pDate

    # Sets the Killer's name
    def setKiller(self, killer):
        self.killer = killer

    # Sets the victims name
    def setVictim(self, victim):
        self.victim = victim

    # Sets the date of the kill
    def setPDate(self, pDate):
        self.pDate = pDate

    # Create a string representation of the teamkill
    def toString(self):
        return "\t- {0} killed {1} on {2}".format(self.killer, self.victim,self.pDate)