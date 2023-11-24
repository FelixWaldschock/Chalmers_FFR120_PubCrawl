import numpy as np

class Pub:
    pubID = None
    pubName = None
    openingTime = None
    closingTime = None
    popularity = None
    posX = None
    posY = None
    peakTime = None

    def __init__(self, pubID, pubName, openingTime, closingTime, popularity, posX, posY, peakTime):
        self.pubID = int(pubID)
        self.pubName = str(pubName)
        self.openingTime = int(openingTime)
        self.closingTime = int(closingTime)
        self.popularity = int(popularity)
        self.posX = int(posX)
        self.posY = int(posY)
        self.peakTime = int(peakTime)

    def getQueueLength(self, currentTime):
        # gaussian distribution with the mean = peakTime
        sigma = 1
        mu = self.peakTime
        queueLength = self.popularity * 1/(np.sqrt(2)) * np.exp(-0.5 * ((currentTime - mu)/sigma)**2)

        return queueLength

        # # queue behaves exponentially decaying
        # queueMax = self.popularity

        # queueLength = queueMax * np.exp(-0.1 * (currentTime - self.openingTime))
        # if queueLength > queueMax:
        #     queueLength = queueMax

        # return queueLength
    
    def getWaitingTime(self, currentTime):
        # waiting time consists of queuelength and opening time
        waitingTime = 0
        if (self.openingTime > currentTime):
            waitingTime += self.openingTime - currentTime
        
        waitingTime += self.getQueueLength(currentTime)

        # if the pub is closed, the waiting time is infinite
        if (self.closingTime < currentTime):
            waitingTime = int(10**15)

        return int(waitingTime)
        
    def printPub(self):
        print("Pub ID: ", self.pubID)
        print("Pub Name: ", self.pubName)
        print("Opening Time: ", self.openingTime)
        print("Closing Time: ", self.closingTime)
        print("Popularity: ", self.popularity)
        print("Position X: ", self.posX)
        print("Position Y: ", self.posY)
        print("Peak Time: ", self.peakTime)
        print("")