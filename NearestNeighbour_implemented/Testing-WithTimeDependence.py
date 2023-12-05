# %%
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import scienceplots
plt.style.use(['science', 'grid'])


# import custom modules
import Pub
import PubCrawlFunctions as PCF
import Ant
import Logger
# import randomPubsInit

# population size of ants
popSize = 19
NNDistance = 18.47

# simulation paramters
tau0 = popSize/(NNDistance)
alpha = 1
beta = 2
rho = 0.02

# simulation counters
time = 0
timeMax = int(60*12)            # 12 hours in minutes - 3pm to 3am 
iter = 0
maxIter = 1000


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
# for i in range(len(Pubs)):
#     distanceMatrix[i][i] = 10e15

# init the visibility matrix
visibilityMatrix = 1 / distanceMatrix

# travelTimeMatrix, is the distanceMatrix [m] divided by the velocity [m/s] between the nodes. Edges including Lindholmen, have a velocity of 12.65 m/s, edges including Chalmers have a velocity of 83.3 m/s
travelTimeMatrix = distanceMatrix

# loop over all nodes
for i in range(len(travelTimeMatrix)):
    for j in range(len(travelTimeMatrix)):
        # coloum 4 and 17 AND row 4 and 17 are divided by 12.65, except [4,17] and [17,4] which are divided by 83.3, the rest is divided by 83.3
        if (i == 4 or j == 4 or i == 17 or j == 17) and (i != j):
            travelTimeMatrix[i][j] = distanceMatrix[i][j] / 12.65
        elif (i != j):
            travelTimeMatrix[i][j] = distanceMatrix[i][j] / 83.3

travelTimeMatrix[4,17] = distanceMatrix[4,17] / 83.3
travelTimeMatrix[17,4] = distanceMatrix[17,4] / 83.3



        

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
    fig, axs = plt.subplots(1, 3, figsize=(15, 6))
    fig.suptitle('Pub Crawl')

    # create a scatter plot of the pubs
    x = [pub.posX for pub in Pubs]
    y = [pub.posY for pub in Pubs]
    pubs_scatter = axs[0].scatter(x, y,c='blue')    


    # place the names of the pubs
    # for i in range(len(Pubs)):
    #     axs[0].annotate(Pubs[i].pubName, (Pubs[i].posX, Pubs[i].posY))

    axs[0].annotate(Pubs[7].pubName, (Pubs[7].posX-60, Pubs[7].posY))


    axs[0].set_title('Map of pubs')
    axs[0].set_xlabel('x')
    axs[0].set_ylabel('y')
    axs[0].axis('equal')

    # plot the connections between the pubs
    connection_lines, = axs[0].plot([], [], 'k-')

    axs[1].grid(False)

    # create a second figure where the pheromone matrix is shown with a legend for the cmap
    image = axs[1].imshow(pheromoneMatrix, cmap='hot', interpolation='nearest')
    axs[1].set_title('Pheromone Matrix')

    # Add a horizontal colorbar below the plot
    colorbar = plt.colorbar(image, ax=axs[1], orientation='horizontal', pad=0.1)  # Adjust the pad as needed
    colorbar.set_label('Pheromone value')  # You can customize the label as needed


    # create a third figure where the pathLength is y and the iteration is x
    # pathLengthPlot, = axs[2].plot([], [], '--x')
    pathLengthPlot, = axs[2].loglog([], [], '--x')
    axs[2].set_title('Path length found')
    axs[2].set_xlabel('Iteration')
    axs[2].set_ylabel('Path Length')
    LengthMax = 0



# clear the log file
Logger.clearLog()

bestIteration = 0
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
        ant = Ant.Ant(velocity=83.3)
        # set ant timer to 0
        ant.setTime(0)
        path = PCF.generatePath(pheromoneMatrix, visibilityMatrix, travelTimeMatrix, alpha, beta, Pubs, ant)
        pathLength = PCF.getPathLength(path, Pubs, travelTimeMatrix)
        #pathLength = PCF.getPathDuration(ant)
        pathDuration = PCF.getPathDuration(ant)

        # update the minimal path
        if pathLength < minimumPathLength:
            minimumPathLength = pathLength
            minimumPath = path
            minimumPathTimeTrajectory = ant.timedPath
            bestAnt = ant
            bestIteration = iter

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
                axs[2].set_xlim(10, iter*(popSize)+(i+1))
                if minimumPathLength > LengthMax:
                    LengthMax = minimumPathLength
                    axs[2].set_ylim(0, int(minimumPathLength*1.1))


                # update the figure title to the minimal path length and iteration
                # fig.suptitle(f'Nearest Neighbour, depending on traveltime \nPub Crawl, iteration: {iter * popSize + (i + 1)}, path length: {minimumPathLength:.3f}')
                fig.suptitle(f'Nearest Neighbour, depending on traveltime \nPub Crawl, iteration:  {iter * popSize + (i + 1)}, path length: {minimumPathLength:.3f}', y=0.98)
                
                plt.pause(0.01)

        pathCollection[i,:] = path
        pathLengthCollection[i] = pathLength
        pathDurationCollection[i] = pathDuration

    # reset the pheroomone matrix if no better path is found in 300 iterations
    if (0):
        if iter - bestIteration > 300:
            print("Resetting pheromone matrix")
            pheromoneMatrix = np.ones((len(Pubs), len(Pubs)))
            pheromoneMatrix = pheromoneMatrix * tau0
            bestIteration = iter

    # update the pheromone matrix
    deltaPheromoneMatrix = PCF.getDeltaPheromoneMatrix(pathCollection, pathLengthCollection)
    #deltaPheromoneMatrix = PCF.getDeltaPheromoneMatrix(pathCollection, pathDurationCollection)
    pheromoneMatrix = PCF.updatePheromoneMatrix(pheromoneMatrix, deltaPheromoneMatrix, rho)

# save the figure

#str(tau0) and limit 3 digits behind comma
#str(f'{tau0:.3f}')


# Plotting parameters as a text box with LaTeX formatting
axs[2].text(0.95, 0.25, r'$\textbf{Population size}$: ' + str(popSize) +
                             '\n$\\alpha$: ' + str(alpha) +
                             '\n$\\beta$: ' + str(beta) +
                             '\n$\\rho$: ' + str(rho) +
                             '\n$\\tau_0$: ' + str(f'{tau0:.3f}'),
            verticalalignment='top', horizontalalignment='right',
            transform=axs[2].transAxes, fontsize=10,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10},
            usetex=True)
if Plotting:
    plt.savefig('NearestNeighbour_PubCrawl.svg', format='svg')
    print("Figure saved")


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



