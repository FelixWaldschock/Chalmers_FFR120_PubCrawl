import numpy as np

class Pub:
    pubID = None
    openingTime = None
    closingTime = None
    popularity = None
    posX = None
    posY = None


    
    def __init__(self, pubID, openingTime, closingTime, popularity, posX, posY):
        self.pubID = int(pubID)
        self.openingTime = int(openingTime)
        self.closingTime = int(closingTime)
        self.popularity = int(popularity)
        self.posX = int(posX)
        self.posY = int(posY)


    def getQueueLength(self, currentTime):
        # queue behaves exponentially decaying
        queueMax = self.popularity

        queueLength = queueMax * np.exp(-0.1 * (currentTime - self.openingTime))
        if queueLength > queueMax:
            queueLength = queueMax

        return queueLength
    
    
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
    
    