import numpy as np

def getDistance(pub1, pub2):
    x1 = pub1.posX
    y1 = pub1.posY
    x2 = pub2.posX
    y2 = pub2.posY
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)


def getWaitingVector(pubs, time):
    waitingVector = np.zeros(len(pubs))
    for i in range(len(pubs)):
        waitingVector[i] = pubs[i].getWaitingTime(time)
    return waitingVector