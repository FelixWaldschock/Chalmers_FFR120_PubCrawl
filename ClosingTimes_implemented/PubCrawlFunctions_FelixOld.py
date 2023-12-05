import numpy as np
import matplotlib.pyplot as plt
import Pub

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


def getNextNode(pheromoneMatrix, visibilityMatrix, tabuList, alpha, beta, Pubs, Ant):
    # get current position
    currentPosition = tabuList[-1]
    probabilities = np.zeros(len(pheromoneMatrix))
    
    # calculate the numerator
    numerator = np.zeros(len(pheromoneMatrix))

    # loop over all nodes
    for i in range(len(probabilities)):
        # check if node is in tabu list
        if i not in tabuList:
            #numerator[i] = (pheromoneMatrix[currentPosition, i]**alpha)*(visibilityMatrix[currentPosition,i]**beta)*(waitingTimeVector[i]**gamma)
            # tmp1 -> pheromone level of the edge i->j
            pheromonePart = (pheromoneMatrix[currentPosition, i])
            # tmp2 -> visibility of the edge i->j
            visibilityPart = (visibilityMatrix[currentPosition,i])
                        
            # tmp3 -> waiting time at pub j
            # catch division by zero
            if (Pubs[i].getWaitingTime(Ant.getTime()) == 0):
                waitingTimePart = 1
            else:
                waitingTimePart = 1 / (Pubs[i].getWaitingTime(Ant.getTime()))

            if (debug):
                # inform user over the values
                print("pheromonePart", pheromonePart)
                print("visibilityPart", visibilityPart)
                print("waitingTimePart", waitingTimePart)

            tmp1 = pheromonePart ** alpha
            tmp2 = (visibilityPart + waitingTimePart) ** beta
            tmp3 = tmp1 * tmp2
            if (tmp3 == 0):
                " Print error in getNextNode calculation"
                exit()
            numerator[i] = tmp3

    # if (debug):
    #     if (np.sum(numerator) == 0):
    #         print("Numerator is zero", numerator)
    #         print("Current position is", currentPosition)
    #         print("i is", i)
    #         print("Tabu list is", tabuList)
    #         print("Pheromone level is", pheromoneMatrix[currentPosition, i])
    #         print("Visibility is", visibilityMatrix[currentPosition,i])
    #         exit


  
    # calculate the denominator
    denominator = np.sum(numerator)

    # calculate the probabilities
    probabilities = numerator/denominator

    # select the next node
    node = rouletteWheelSelection(probabilities)

    # update the time
    # waitingTime + travelTime + beerTime  
    waitingTime = Pubs[node].getWaitingTime(Ant.getTime())
    travelTime = (getDistance(Pubs[currentPosition], Pubs[node])) / 83.3
    beerTime = 5
    deltaTime = waitingTime + travelTime + beerTime
    # print(deltaTime)
    
    # update the time
    Ant.setTime(Ant.getTime() + deltaTime)

    # update the timedPath
    Ant.timedPath.append([node, Ant.getTime()])

    return node


def generatePath(pheromoneMatrix, visibilityMatrix, alpha, beta, Pubs, Ant):
    # start the time counter
    time = Ant.getTime()

    # init the tabu list
    tabuList = []

    # select a random starting node, which is a pub that has a opening time = 0
    # find all pubs that have an opening time = 0
    startingPubs = []
    for i in range(len(Pubs)):
        if (Pubs[i].openingTime == 0):
            startingPubs.append(i)

    # pick a random pub from the starting pubs
    currentNode = np.random.choice(startingPubs)
 
    # update the timedPath
    Ant.timedPath.append([currentNode, Ant.getTime()])

    # determine the waiting time vector
    waitingTimeVector = np.zeros(len(Pubs))
    for i, p in enumerate(Pubs):
        waitingTimeVector[i] = p.getWaitingTime(time)

    # add the starting node to the tabo list
    tabuList.append(currentNode)

    # build the tour
    for i in range(len(pheromoneMatrix)-1):
        nextNode = getNextNode(pheromoneMatrix, visibilityMatrix, tabuList, alpha, beta, Pubs, Ant)


        # update the tabu list
        tabuList.append(nextNode)


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

        # if(debug):
        #     print("Distance between pub", Path[i], "and pub", Path[i+1])

        distance = getDistance(pubs[Path[i]], pubs[Path[i+1]])
        # add the distance to the path length
        pathLength = pathLength + distance

    # RETURN TO ORIGIN NOT INCLUDING

    return pathLength

def getDeltaPheromoneMatrix(pathCollection, pathLengthCollection):
    deltaPheromones = np.zeros((pathCollection.shape[1], pathCollection.shape[1]))

    numberOfAnts = (pathCollection.shape)[0]

    # loop over each ant (k)
    for k in range(numberOfAnts):
        # get the tour length of the ant -> For distance optimization
        tourLength = pathLengthCollection[k]

        # get tour duration of the ant -> For time optimization


        # get the edges that the ant has visited
        edges = np.zeros((len(pathCollection[k]), 2), dtype=int)

        for i in range(len(pathCollection[k])-1):
            edges[i][0] = int(pathCollection[k][i])
            edges[i][1] = int(pathCollection[k][i+1])
        
        deltaPheromonesAnt = np.zeros((pathCollection.shape[1], pathCollection.shape[1]))

        # print("deltaPheromonesAnt shape", deltaPheromonesAnt.shape)

        # loop over all edges
        for m in range(len(edges)):
            i = edges[m][0]
            j = edges[m][1]

            deltaPheromonesAnt[i][j] = 1/tourLength
            deltaPheromonesAnt[j][i] = 1/tourLength

        deltaPheromones = deltaPheromones + deltaPheromonesAnt

    return deltaPheromones

def getPathDuration(ant):
    return ant.getTime()



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

def initPubs(filePath):
    pubsList = np.genfromtxt(filePath, delimiter=',', dtype=str, skip_header=1)
    # init the Pubs 
    Pubs = []
    for i in range(pubsList.shape[0]):
        pubID = pubsList[i][0]
        pubName = pubsList[i][1]
        openingTime = pubsList[i][2]
        closingTime = pubsList[i][3]
        popularity = pubsList[i][4]
        posX = pubsList[i][5]
        posY = pubsList[i][6]
        peakTime = pubsList[i][7]
        sigma = pubsList[i][8]
        # create the Pub
        pub = Pub.Pub(pubID, pubName, openingTime, closingTime, popularity, posX, posY, peakTime, sigma)
        Pubs.append(pub)

    return Pubs


def plotPath(path, Pubs):
    # create the figure that will be returned
    fig = plt.figure()
    
    # get the x and y coordinates of the path
    x = np.zeros(len(path))
    y = np.zeros(len(path))

    for i in range(len(path)):
        x[i] = Pubs[path[i]].posX
        y[i] = Pubs[path[i]].posY

    # plot the path
    plt.plot(x, y, '--b')

    # plot the pubs
    for i in range(len(Pubs)):
        plt.plot(Pubs[i].posX, Pubs[i].posY, 'ro')

    # return the figure
    return fig

