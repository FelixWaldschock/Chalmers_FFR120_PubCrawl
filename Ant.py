import numpy as np

class Ant:
    # has a tabo list of visited pubs
    taboList = None
    time = 0
    velocity = 83.3

    # variable to store the path
    path = None

    # variable to store when which pub was visited
    timedPath = None

    def __init__(self, velocity):
        self.time = 0
        self.path = []
        self.timedPath = []
        self.velocity = velocity

    def getTaboList(self):
        return self.taboList

    def addToTaboList(self, pubID):
        self.taboList.append(pubID)

    def getTime(self):
        return self.time
    
    def setTime(self, time):
        self.time = time

    def getVelocity(self):
        return self.velocity