import numpy as np

class Pub:
    pubID = None
    openingTime = None
    closingTime = None
    popularity = None
    posX = None
    posY = None
<<<<<<< Updated upstream


    
    def __init__(self, pubID, openingTime, closingTime, popularity, posX, posY):
=======
    peakTime = None
    sigma = None
    peakTimeOpening = None
    sigmaOpeningTime = None
    openingPopularity = None

    def __init__(self, pubID, pubName, openingTime, closingTime, popularity, posX, posY, peakTime, sigma, peakTimeOpening, sigmaOpeningTime, openingPopularity):
>>>>>>> Stashed changes
        self.pubID = int(pubID)
        self.openingTime = int(openingTime)
        self.closingTime = int(closingTime)
        self.popularity = int(popularity)
        self.posX = int(posX)
        self.posY = int(posY)
<<<<<<< Updated upstream

=======
        self.peakTime = int(peakTime)
        self.sigma = int(sigma)
        self.peakTimeOpening = int(peakTimeOpening)
        self.sigmaOpeningTime = int(sigmaOpeningTime)
        self.openingPopularity = int(openingPopularity)
>>>>>>> Stashed changes

    def getQueueLength(self, currentTime):
        # queue behaves exponentially decaying
        queueMax = self.popularity

        queueLength = queueMax * np.exp(-0.1 * (currentTime - self.openingTime))
        if queueLength > queueMax:
            queueLength = queueMax

        return queueLength
    
    
    def getWaitingTime(self, currentTime):
        # waiting time consists of queuelength and opening time
        openingQueueTime = None
        waitingTime = 0
<<<<<<< Updated upstream
        if (self.openingTime > currentTime):
            waitingTime += self.openingTime - currentTime
=======
        sigmaOpening = self.sigmaOpeningTime
        muOpening = self.peakTimeOpening
        term1 = 100 * self.openingPopularity
        term2 = np.exp(-0.5 * ((currentTime - muOpening)/sigmaOpening)**2)
        openingQueueTime = term1*term2
        # if pub is not open yet, add the delta until the opening time
        # if (self.openingTime > currentTime):
        #     waitingTime += self.openingTime - currentTime
        waitingTime += openingQueueTime
>>>>>>> Stashed changes
        
        waitingTime += self.getQueueLength(currentTime)

        # if the pub is closed, the waiting time is infinite
        if (self.closingTime < currentTime):
            waitingTime = int(10**15)

        return int(waitingTime)
    
    