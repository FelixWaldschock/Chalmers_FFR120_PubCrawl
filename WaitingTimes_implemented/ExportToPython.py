# %% [markdown]
# PubCrawl Simulation Developer Notebook

# %%
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import psutil
import tqdm
plt.style.use(['science','grid'])

# import custom modules
import Pub
import PubCrawlFunctions as PCF
import Ant
import Logger
import randomPubsInit

# %%

# %%
# Use the random pubs
Pubs = PCF.initPubs('pubs.csv')

waitingTimes = PCF.getWaitingVector(Pubs, 0)

# %%
# simulation paramters
tau0 = 1
alpha = 1
beta = 3
gamma = 1 
rho = 0.2

# simulation counters
time = 0
timeMax = int(60*12)            # 12 hours in minutes - 3pm to 3am 
iter = 0
maxIter = 10000
# population size of ants
popSize = 5

# velocity of an ant
velAnt = 1


# %%
# init the pheromone matrix which is a 2D array with the size of the number of pubspheromoneMatrix = np.ones((len(Pubs), len(Pubs)))
pheromoneMatrix = np.ones((len(Pubs), len(Pubs)))
pheromoneMatrix = pheromoneMatrix * tau0


# the visibility matrix is in this case not only the distance between the pubs, but also takes into consideration
# the waiting time at the next pub
# we inititalize the matrix at time = 0

# init the distance matrix D
distanceMatrix = np.zeros((len(Pubs), len(Pubs)))
for i in range(len(Pubs)):
    for j in range(i, len(Pubs)):
        distanceMatrix[i][j] = PCF.getDistance(Pubs[i], Pubs[j])
        #  print("i and j: ", i, j, " distance: ", distanceMatrix[i][j])

        distanceMatrix[j][i] = distanceMatrix[i][j]

# set the diagonal to 10e15
for i in range(len(Pubs)):
    distanceMatrix[i][i] = 10e15

# init the visibility matrix
visibilityMatrix = 1 / distanceMatrix

# %%


def print_memory_usage():
    memory = psutil.virtual_memory()
    print(f"Used Memory: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Total Memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Memory Usage Percentage: {memory.percent:.2f}%")


# %%
pathCollection = np.zeros((popSize, len(Pubs)))
pathLengthCollection = np.zeros((popSize, 1))

minimumPathLength = int(10e15)
minimumPath = np.zeros(len(Pubs))
bestAnt = None

Plotting = True

if Plotting:
    # create a figure with 2 subplots, left the path, right the pheromone matrix


    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Pub Crawl')

    # create a scatter plot of the pubs
    x = [pub.posX for pub in Pubs]
    y = [pub.posY for pub in Pubs]
    pubs_scatter = axs[0].scatter(x, y)

    # place the names of the pubs
    # for i in range(len(Pubs)):
    #     axs[0].annotate(Pubs[i].pubName, (Pubs[i].posX, Pubs[i].posY))

    axs[0].set_title('Pubs')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y')
    axs[0].axis('equal')

    # plot the connections between the pubs
    connection_lines, = axs[0].plot([], [], 'k-')

    # create a second figure where the pheromone matrix is plotted
    axs[1].imshow(pheromoneMatrix, cmap='hot', interpolation='nearest')
    axs[1].set_title('Pheromone Matrix')

    # create a third figure where the pathLength is y and the iteration is x
    pathLengthPlot, = axs[2].plot([], [], '--x')
    axs[2].set_title('Path Length')
    axs[2].set_xlabel('Iteration')
    axs[2].set_ylabel('Path Length')
    LengthMax = 0



# clear the log file
Logger.clearLog()


## Main algorithm

while(iter < maxIter):
    iter += 1

    # give heartbeat
    if iter % 100 == 0:
        print("Iteration: ", iter)
        print_memory_usage()


    # Generate paths
    for i in range(popSize):
        # create an Ant
        ant = Ant.Ant(velocity=1)
        path = PCF.generatePath(pheromoneMatrix, visibilityMatrix, alpha, beta, gamma, Pubs, ant)
        #pathLength = PCF.getPathLength(path, Pubs)
        pathLength = PCF.getPathDuration(ant)
        # pathDuration = PCF.getPathDuration(path, Pubs, ant)
        

        # update the minimal path
        if pathLength < minimumPathLength:
            minimumPathLength = pathLength
            minimumPath = path
            minimumPathTimeTrajectory = ant.timedPath
            bestAnt = ant

            # inform the user
            # print('New minimum path found, in iteration: ', minimumPathLength, iter)
            # print("Path: ", minimumPath)

            # log the new minimum path
            Logger.logBestPath(minimumPath, minimumPathTimeTrajectory, minimumPathLength)

            if Plotting:
                # update scatter plot
                x = [Pubs[pubID].posX for pubID in minimumPath]
                y = [Pubs[pubID].posY for pubID in minimumPath]
                pubs_scatter.set_offsets(np.column_stack((x, y)))

                # update connection lines
                connection_lines.set_xdata(x)
                connection_lines.set_ydata(y)

                # update the pheromone matrix
                axs[1].imshow(pheromoneMatrix, cmap='hot', interpolation='nearest')

                # update the path length plot
                pathLengthPlot.set_xdata(np.append(pathLengthPlot.get_xdata(), iter*(popSize)+(i+1)))
                pathLengthPlot.set_ydata(np.append(pathLengthPlot.get_ydata(), minimumPathLength))
                axs[2].set_xlim(0, iter*(popSize)+(i+1))
                if minimumPathLength > LengthMax:
                    LengthMax = minimumPathLength
                    axs[2].set_ylim(0, int(minimumPathLength*1.1))


                # update the figure title to the minimal path length and iteration
                fig.suptitle('Pub Crawl, iteration: ' + str(iter) + ', path length: ' + str(minimumPathLength))

                plt.pause(0.01)





        pathCollection[i,:] = path
        pathLengthCollection[i] = pathLength

    # update the pheromone matrix
    deltaPheromoneMatrix = PCF.getDeltaPheromoneMatrix(pathCollection, pathLengthCollection)
    pheromoneMatrix = PCF.updatePheromoneMatrix(pheromoneMatrix, deltaPheromoneMatrix, rho)


# save the figure
if Plotting:
    plt.savefig('PubCrawl.png')


# while no keyboard interrupt
try:
    while(True):

        # close the figure
        plt.close(fig)

        # create a fig where the best ant is used. Horizontal axis is time, vertical axis is the pubs
        fig, axs = plt.subplots(1, 1, figsize=(15, 5))
        fig.suptitle('Pub Crawl')

        # plot a scatter with y axis is the pub ID and x axis is the time. Data can be extracted from the bestAnt object, 
        # where the timedPath is stored. First element of timedPath is the pubID, second element is the time
        x = [pubID[1] for pubID in bestAnt.timedPath]
        y = [pubID[0] for pubID in bestAnt.timedPath]


        axs.scatter(x, y)
        
        plt.show()


except KeyboardInterrupt:
    print("Keyboard interrupt")





# %%
