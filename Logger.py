import numpy as np
import os

folder = "Logs/"
counter = folder + "counter.txt"
logFileName = folder + "BestPath_" + str(np.loadtxt(counter, dtype=int)) + ".csv" 
# increment counter
np.savetxt(counter, [np.loadtxt(counter, dtype=int)+1], fmt='%i')

# log the best found path
# append it to the csv file 
# first column being the path, where all elements are seperated by ;, and the second column being the path length
def logBestPath(path, pathLength):
    # open the file
    file = open(logFileName, "a")

    # write the path
    for i in range(len(path)):
        file.write(str(path[i]))
        if(i < len(path)-1):
            file.write(";")
    file.write(",")

    # write the path length
    file.write(str(pathLength))

    # write a new line
    file.write("\n")

    # close the file
    file.close()
    

def clearLog():
    # delete the file if it exists
    if(os.path.exists(logFileName)):
        os.remove(logFileName)