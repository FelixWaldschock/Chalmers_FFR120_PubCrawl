import numpy as np

class Ant:
    # has a tabo list of visited pubs
    taboList = None

    def __init__(self, taboList):
        self.taboList = taboList

    def getTaboList(self):
        return self.taboList

    def addToTaboList(self, pubID):
        self.taboList.append(pubID)

