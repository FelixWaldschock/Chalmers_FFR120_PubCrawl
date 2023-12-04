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
    sigma = None

    def __init__(self, pubID, pubName, openingTime, closingTime, popularity, posX, posY, peakTime, sigma):
        self.pubID = int(pubID)
        self.pubName = str(pubName)
        self.openingTime = int(openingTime)
        self.closingTime = int(closingTime)
        self.popularity = int(popularity)
        self.posX = int(posX)
        self.posY = int(posY)
        self.peakTime = int(peakTime)
        self.sigma = int(sigma)

    def getQueueLength(self, currentTime):
        # gaussian distribution with the mean = peakTime
        sigma = self.sigma
        mu = self.peakTime
        term1 = self.popularity
        term2 = np.exp(-0.5 * ((currentTime - mu)/sigma)**2)
        queueLength = term1 * term2
        # print("Term1: ", term1)
        # print("Term2: ", term2)
        # print("Queue Length: ", queueLength)
        return int(queueLength)
    
    def getWaitingTime(self, currentTime):
        # waiting time consists of queuelength and opening time
        waitingTime = 0

        # if pub is not open yet, add the delta until the opening time
        if (self.openingTime > currentTime):
            waitingTime += self.openingTime - currentTime
        
        # add the waiting time of the queue
        waitingTime += self.getQueueLength(currentTime)

        # if the pub is closed, the waiting time is infinite
        if (self.closingTime < currentTime):
            waitingTime = 7200

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