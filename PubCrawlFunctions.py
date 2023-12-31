import numpy as np

debug = False

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


def getNextNode(pheromoneMatrix, visibilityMatrix, waitingTimeVector, tabuList, alpha, beta, gamma, Pubs):

    # get current position
    currentPosition = tabuList[-1]
    probabilities = np.zeros(len(pheromoneMatrix))
    
    # calculate the numerator
    numerator = np.zeros(len(pheromoneMatrix))
    # loop over all nodes

    # print the tabi list
    # if(debug):
    #     print("Tabu list is", tabuList)
    #     print("Current position is", currentPosition)


    for i in range(len(probabilities)):
        # check if node is in tabu list
        if i not in tabuList:
            #numerator[i] = (pheromoneMatrix[currentPosition, i]**alpha)*(visibilityMatrix[currentPosition,i]**beta)*(waitingTimeVector[i]**gamma)
            tmp1 = (pheromoneMatrix[currentPosition, i]**alpha)
            tmp2 = (visibilityMatrix[currentPosition,i]**beta)
            tmp3 = tmp1 * tmp2
            if (tmp3 == 0):
                " Print error in getNextNode calculation"
                exit()
            numerator[i] = tmp3

    if (debug):
        if (np.sum(numerator) == 0):
            print("Numerator is zero", numerator)
            print("Current position is", currentPosition)
            print("i is", i)
            print("Tabu list is", tabuList)
            print("Pheromone level is", pheromoneMatrix[currentPosition, i])
            print("Visibility is", visibilityMatrix[currentPosition,i])
            exit


        # if (debug):
        #     print("Shape of numerator is", numerator.shape)
        #     print("Numerators are", numerator)

    # calculate the denominator
    denominator = np.sum(numerator)

    # calculate the probabilities
    probabilities = numerator/denominator

    # if(debug):
    #     print("Denominator is", denominator)
    #     print("Shape of numerator is", numerator.shape)
    #     print("Numerator is", numerator)
    #     print("Shape of probabilities is", probabilities.shape)
    #     print("Probabilities are", probabilities)

    # select the next node
    node = rouletteWheelSelection(probabilities)
    
    return node


def generatePath(pheromoneMatrix, visibilityMatrix, waitingTimeVector, alpha, beta, gamma, Pubs):
    # start the time counter
    time = 0

    # init the tabu list
    tabuList = []

    # select a random starting node
    currentNode = np.random.randint(len(pheromoneMatrix))

    # add the starting node to the tabo list
    tabuList.append(currentNode)

    # build the tour
    for i in range(len(pheromoneMatrix)-1):
        nextNode = getNextNode(pheromoneMatrix, visibilityMatrix, waitingTimeVector, tabuList, alpha, beta, gamma, Pubs)

        if(debug):
            print("Next node is", nextNode)

        # update the tabu list
        tabuList.append(nextNode)

        if (debug):
            print("Tabu list is", tabuList)

    Path = tabuList

    return Path

def rouletteWheelSelection(Vector):
    # make a cumsum of the vector
    cumsum = np.cumsum(Vector)
    # normalize the cumsum
    cumsum = cumsum / np.sum(Vector)

    # generate a random number between 0 and 1
    r = np.random.rand()

    # if(debug):
    #     print("r =", r)
    #     print("cumsum =", cumsum)

    # find the index of the cumsum using searchsorted
    index = np.searchsorted(cumsum, r)

    return index

def getPathLength(Path, pubs):
    # init the path length
    pathLength = 0

    # loop over all nodes in the path
    for i in range(len(Path)-1):
        # get the distance between the two pubs

        # if(debug):
        #     print("Distance between pub", Path[i], "and pub", Path[i+1])

        distance = getDistance(pubs[Path[i]], pubs[Path[i+1]])
        # add the distance to the path length
        pathLength = pathLength + distance

    # RETURN TO ORIGIN NOT INCLUDING

    return pathLength

def getDeltaPheromoneMatrix(pathCollection, pathLengthCollection):
    deltaPheromones = np.zeros(pathCollection.shape)
    # print("deltaPheromones shape", deltaPheromones.shape)

    numberOfAnts = len(pathCollection)

    # loop over each ant (k)
    for k in range(numberOfAnts):
        tourLength = pathLengthCollection[k]
        # print("Tour length of ant", k, "is", tourLength)

        # get the edges that the ant has visited
        edges = np.zeros((len(pathCollection[k]), 2), dtype=int)
        for i in range(len(pathCollection[k])-1):
            edges[i][0] = int(pathCollection[k][i])
            edges[i][1] = int(pathCollection[k][i+1])
        
        deltaPheromonesAnt = np.zeros(pathCollection.shape)

        # loop over all edges
        for m in range(len(edges)):
            i = edges[m][0]
            j = edges[m][1]

            # print i and j
            # print("i =", i, "j =", j)

            deltaPheromonesAnt[i][j] = 1/tourLength
            deltaPheromonesAnt[j][i] = 1/tourLength

        deltaPheromones = deltaPheromones + deltaPheromonesAnt

    return deltaPheromones




def updatePheromoneMatrix(pheromoneMatrix, deltaPheromoneMatrix, rho):
    Threshold = int(10e-15)

    # print shapes of the matrices
    # print("pheromoneMatrix shape", pheromoneMatrix.shape)
    # print("deltaPheromoneMatrix shape", deltaPheromoneMatrix.shape)


    for i in range(len(pheromoneMatrix)):
        for j in range(len(pheromoneMatrix)):
            if(pheromoneMatrix[i][j] < Threshold):
                pheromoneMatrix[i][j] = Threshold
            pheromoneMatrix[i][j] = (1-rho)*pheromoneMatrix[i][j] + deltaPheromoneMatrix[i][j]

        
    return pheromoneMatrix

