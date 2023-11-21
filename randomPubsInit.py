import numpy as np
import os

fileName = "randomPubs.csv"

# Populate the pubs.csv file with random values in the ranges
numberOfPubs = 50
xRange = [0, 1000]
yRange = [0, 1000]
openingTimeRange = [0, 12*60-100]
closingTimeRange = [100, 12*60]
populatity = [1, 20]


# delete the file if it exists
if(os.path.exists(fileName)):
    os.remove(fileName)

# open the file
file = open(fileName, "a")

# write the header
header = "ID,OpeningTime,ClosingTime,Popularity,PosX,PosY"
file.write(header)

for i in range(numberOfPubs):
    # write a new line
    file.write("\n")

    # write the ID
    file.write(str(i))
    file.write(",")

    # write the opening time
    openingTime = np.random.randint(openingTimeRange[0], openingTimeRange[1])
    file.write(str(openingTime))
    file.write(",")

    # write the closing time
    closingTime = np.random.randint(closingTimeRange[0], closingTimeRange[1])
    file.write(str(closingTime))
    file.write(",")

    # write the popularity
    popularity = np.random.randint(populatity[0], populatity[1])
    file.write(str(popularity))
    file.write(",")

    # write the x position
    posX = np.random.randint(xRange[0], xRange[1])
    file.write(str(posX))
    file.write(",")

    # write the y position
    posY = np.random.randint(yRange[0], yRange[1])
    file.write(str(posY))

# close the file
file.close()