# %%
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from tqdm import trange
plt.style.use(['science','grid'])

# import custom modules
import Pub
import PubCrawlFunctions as PCF
import Ant
import Logger
# import randomPubsInit

# %%


# %%
# simulation paramters
tau0 = 1
alpha = 1
beta = 2
rho = 0.01

# simulation counters
time = 0
timeMax = int(60*12)            # 12 hours in minutes - 3pm to 3am 
iter = 0
maxIter = 1000000
# population size of ants
popSize = 50

# velocity of an ant
velAnt = int(5000 / 60)         # 5km/h in m/min


# %%
Pubs = PCF.initPubs('pubs.csv')


# init the pheromone matrix which is a 2D array with the size of the number of pubs
pheromoneMatrix = np.ones((len(Pubs), len(Pubs)))
pheromoneMatrix = pheromoneMatrix * tau0

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
# Ant colony

pathCollection = np.zeros((popSize, len(Pubs)))
pathLengthCollection = np.zeros((popSize, 1))
pathDurationCollection = np.zeros((popSize, 1))

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
    # pathLengthPlot, = axs[2].plot([], [], '--x')
    pathLengthPlot, = axs[2].semilogy([], [], '--x')
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
    if iter % 500 == 0:
        print("Iteration: ", iter)
        print("Pheromone  max: ", np.max(pheromoneMatrix))


    # Generate paths
    for i in range(popSize):
        # create an Ant
        ant = Ant.Ant(velocity=1)
        # set ant timer to 0
        ant.setTime(0)
        path = PCF.generatePath(pheromoneMatrix, visibilityMatrix, alpha, beta, Pubs, ant)
        #pathLength = PCF.getPathLength(path, Pubs)
        pathLength = PCF.getPathDuration(ant)
        pathDuration = PCF.getPathDuration(ant)

        # update the minimal path
        if pathLength < minimumPathLength:
            minimumPathLength = pathLength
            minimumPath = path
            minimumPathTimeTrajectory = ant.timedPath
            bestAnt = ant

            # # inform the user
            print('New minimum path found, in iteration: ', minimumPathLength, iter)
            # print("Path: ", minimumPath)
            # print("Name of pubs: ", [Pubs[pubID].pubName for pubID in minimumPath])
            # print("Pheromone  min: ", np.min(pheromoneMatrix))
            # print("Pheromone  max: ", np.max(pheromoneMatrix))
            # print("Pheromone  mean: ", np.mean(pheromoneMatrix))

            
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
        pathDurationCollection[i] = pathDuration

    # update the pheromone matrix
    #deltaPheromoneMatrix = PCF.getDeltaPheromoneMatrix(pathCollection, pathLengthCollection)
    deltaPheromoneMatrix = PCF.getDeltaPheromoneMatrix(pathCollection, pathDurationCollection)
    pheromoneMatrix = PCF.updatePheromoneMatrix(pheromoneMatrix, deltaPheromoneMatrix, rho)




# %%
# scatter plot to show the trajectory of the best ant over time, x-> time y-> pubID
fig, ax = plt.subplots(figsize=(10, 10))

bestPath = np.array(bestAnt.timedPath)


x = bestPath[:,1]
y = bestPath[:,0]
# convert to integer
x = x.astype(int)
y = y.astype(int)

print(bestPath)


ax.plot(x, y, c='r', marker="o")
ax.set_xlabel('time')
ax.set_ylabel('pubID')
ax.set_xlim(0, 720)

# %%
# inform the user over the best found ant
print("Best ant: ", bestAnt)
print("Best path: ", minimumPath)
print("Best path length: ", minimumPathLength)
print("Best path time trajectory: ", minimumPathTimeTrajectory)

# %%
# calculate 

# set diagonal to 0
for i in range(len(distanceMatrix)):
    distanceMatrix[i][i] = 0

plt.imshow(distanceMatrix)
print(np.max(distanceMatrix))

# %%



