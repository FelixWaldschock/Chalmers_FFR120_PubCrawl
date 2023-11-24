import numpy as np

class Ant:
    # has a tabo list of visited pubs
    taboList = None
    time = 0

    def __init__(self, taboList):
        self.taboList = taboList

    def getTaboList(self):
        return self.taboList

    def addToTaboList(self, pubID):
        self.taboList.append(pubID)

    def getTime(self):
        return self.time
    
    def setTime(self, time):
        self.time = time
