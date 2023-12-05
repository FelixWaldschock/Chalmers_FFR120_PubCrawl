import numpy as np
import os
import Ant
import json
import shutil

folder = "Logs/"
counter = folder + "counter.txt"
logFileName = folder + "BestPath_" + str(np.loadtxt(counter, dtype=int)) + ".csv"
logFileNameJSON = folder + "BestPath_" + str(np.loadtxt(counter, dtype=int)) + ".json"
# increment counter
np.savetxt(counter, [np.loadtxt(counter, dtype=int)+1], fmt='%i')

# log the best found path
# append it to the csv file 
# first column being the path, where all elements are seperated by ;, and the second column being the path length
def logBestPath(path, timedPath, pathLength):
    # open the file
    file = open(logFileName, "a")

    # # write the path
    # for i in range(len(path)):
    #     file.write(str(path[i]))
    #     if(i < len(path)-1):
    #         file.write(";")
    # file.write(",")

    # write the timed path
    for i in range(len(timedPath)):
        file.write(str(timedPath[i]))
        if(i < len(timedPath)-1):
            file.write(";")
    file.write(",")

    # # write the path length
    # file.write(str(pathLength))

    # write a new line
    file.write("\n")

    # close the file
    file.close()

    logBestPathJSON(path, timedPath, pathLength)
    
def logBestPathJSON(path, timedPath, pathLength):
    # open the file
    file = open(logFileNameJSON, "a")

    # write the path
    file.write("{ \"path\": [")
    for i in range(len(path)):
        file.write(str(path[i]+1))
        if(i < len(path)-1):
            file.write(",")
    file.write("],")

    # write the timed path, increment the index by 1

    file.write("\"timedPath\": [")
    for i in range(len(timedPath)):

        file.write(str(timedPath[i]))

        if(i < len(timedPath)-1):
            file.write(",")
    file.write("],")

    # write the path length
    file.write("\"pathLength\": " + str(pathLength))

    # write a new line
    file.write("}\n")

    # close the file
    file.close()

    # duplicate the created file and name it BestPath.json
    shutil.copy(logFileNameJSON, folder + "BestPath.json")


def clearLog():
    # delete the file if it exists
    if(os.path.exists(logFileName)):
        os.remove(logFileName)
        


def loadLog(filename, velAnt):
    Ants = []
    # data looks like this:
        # { "path": [4,2,1,3,11,0,14,16,5,8,7,6,15,12,13,10,18,9,17],"timedPath": [[4, 0],[2, 45.9859408862011],[1, 52.41728384522044],[3, 304.59735587403196],[11, 310.63755654737815],[0, 315.99062836418136],[14, 5036.218403465754],[16, 12241.687973867089],[5, 19447.04104568389],[8, 26652.29570598924],[7, 33857.81691351256],[6, 41062.96876358027],[15, 48268.27553266405],[12, 55474.05177099107],[13, 62680.73539898711],[10, 69886.41119576718],[18, 77091.74925405867],[9, 84297.14704617213],[17, 91542.94525025573]],"pathLength": 91542.94525025573}
    
    # Read the file line by line and process each line
    with open(filename, 'r') as file:
        for line in file:
            # Parse the JSON object from the line
            data = json.loads(line)

            # Access the values as needed
            path = data.get('path')
            timed_path = data.get('timedPath')
            path_length = data.get('pathLength')

            # Create an ant object
            ant = Ant.Ant(velAnt)
            ant.loadAnt(path, timed_path, path_length)
            Ants.append(ant)
    
    return Ants