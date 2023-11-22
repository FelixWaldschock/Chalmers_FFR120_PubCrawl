# %% [markdown]
# PubCrawl Simulation Developer Notebook

# %%
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
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
Pubs = PCF.initPubs('RandomPubs.csv')

waitingTimes = PCF.getWaitingVector(Pubs, 0)

# %%
# simulation paramters
tau0 = 1
alpha = 1
beta = 1
gamma = 1 
rho = 0.2

# simulation counters
time = 0
timeMax = int(60*12)            # 12 hours in minutes - 3pm to 3am 
iter = 0
# population size of ants
popSize = 20

# velocity of an ant
velAnt = 1


# %%
# init the pheromone matrix which is a 2D array with the size of the number of pubs
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


# %% [markdown]
# ## Test the ACO without time dependecy, for this set timeMatrix = ones and gamma = 1

# %%


# %%
pathCollection = np.zeros((popSize, len(Pubs)))
pathLengthCollection = np.zeros((popSize, 1))

minimumPathLength = int(10e15)
minimumPath = np.zeros(len(Pubs))

Plotting = True

if Plotting:
    # create a figure with 2 subplots, left the path, right the pheromone matrix


    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Pub Crawl')

    # create a scatter plot of the pubs
    x = [pub.posX for pub in Pubs]
    y = [pub.posY for pub in Pubs]
    pubs_scatter = axs[0].scatter(x, y)
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


while(iter < 10000):
    iter += 1

    # give heartbeat
    if iter % 100 == 0:
        print("Iteration: ", iter)


    # Generate paths
    for i in range(popSize):
        path = PCF.generatePath(pheromoneMatrix, visibilityMatrix, waitingTimes, alpha, beta, gamma, Pubs)
        pathLength = PCF.getPathLength(path, Pubs)

        # update the minimal path
        if pathLength < minimumPathLength:
            minimumPathLength = pathLength
            minimumPath = path

            # inform the user
            # print('New minimum path found, in iteration: ', minimumPathLength, iter)
            # print("Path: ", minimumPath)

            # log the new minimum path
            Logger.logBestPath(minimumPath, minimumPathLength)

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



# # %%
# # plot the best path
# # load the best path from the log files

# counter = 4

# bestPathPath = "Logs/BestPath_" + str(counter) + ".csv"
# # read the last line of the file
# with open(bestPathPath, 'r') as f:
#     lines = f.readlines()
#     last_line = lines[-1]
#     bestPath = last_line


# # parse the bestPath, the first element is before the "," the second after
# bestPathOrigin = bestPath.split(',')
# # convert the first element to an array of intergers, delimited by ;
# bestPath = np.array(bestPathOrigin[0].split(';')).astype(int)
# bestPathLength = bestPathOrigin[1]

# # plot the best path
# fig = PCF.plotPath(bestPath, Pubs)
# plt.title('Best Path')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()



# # %%
# print('Distance Matrix: ', distanceMatrix)

# print('Pheromone Matrix: ', pheromoneMatrix)

# print('Waiting vector: ', PCF.getWaitingVector(Pubs, time))

# print('Waiting vector: ', PCF.getWaitingVector(Pubs, 100))




