import numpy as np
import os

fileName = "randomPubs.csv"

# Populate the pubs.csv file with random values in the ranges
numberOfPubs = 10
xRange = [0, 1000]
yRange = [0, 1000]
openingTimeRange = [0, 12*60-100]
closingTimeRange = [100, 12*60]
populatity = [1, 20]
peakTime = [0, 12*60-100]


# delete the file if it exists
if(os.path.exists(fileName)):
    os.remove(fileName)

# open the file
file = open(fileName, "a")

# write the header
header = "ID,OpeningTime,ClosingTime,Popularity,PosX,PosY,PeakTime"
file.write(header)

# random pub names
pub_names = [
    "Velvet Tankard",
    "Eccentric Haven",
    "Whispering Willow",
    "Posh Pint",
    "Enchanted Emporium",
    "Majestic Boudoir",
    "Renaissance Sanctuary",
    "Celestial Tavern",
    "Opulent Den",
    "Velvet Lounge",
    "Moonlit Guild",
    "Regal Quarters",
    "Frosted Oasis",
    "Radiant Boutique",
    "Sable Hops",
    "Gilded Manor",
    "Nebula Nook",
    "Ethereal Bastion",
    "Frothy Phoenix",
    "Grandiose Gallery",
    "Enigmatic Enclave",
    "Luminous Lounge",
    "Silver Society",
    "Cosmic Soiree",
    "Imperial Pavilion",
    "Enchanting Hollow",
    "Sterling Salon",
    "Whimsical Wharf",
    "Ivory Atelier",
    "Resplendent Refuge",
    "Mystical Manor",
    "Grand Goblet",
    "Opalescent Oasis",
    "Amber Anvil",
    "Sovereign Salon",
    "Plush Pavilion",
    "Golden Grove",
    "Velvet Vault",
    "Noble Nest",
    "Celestial Castle",
    "Platinum Palace",
    "Whimsy Wonders",
    "Silken Sanctuary",
    "Brazen Barrel",
    "Mystic Mug",
    "Ethereal Elixir",
    "Whiskey Wonders",
    "Sapphire Sip",
    "Lush Lager",
    "Crimson Cask",
    "Enclave Ember",
    "Vivid Vessel",
    "Copper Cellar",
    "Echoing Stein",
    "Sylvan Suds",
    "Crested Cork",
    "Twilight Tap",
    "Ruby Refuge",
    "Dapper Draught",
    "Cask Cozy",
    "Royal Rum",
    "Golden Grove",
    "Whispering Wharf",
    "Cask Cascade",
    "Gentle Grail",
    "Baroque Brew",
    "Arcane Ale",
    "Goblet Grove",
    "Brew Bliss",
    "Sapphire Sip",
    "Mellow Mug",
    "Epicurean Elixir",
    "Nectar Nook",
    "Brewers' Boudoir",
    "Lively Lounge",
    "Pint Pavilion",
    "Bountiful Barrel",
    "Cask Commune",
    "Crimson Cork",
    "Silent Stein",
    "Aurora Ale",
    "Nectar Nook",
    "Tantalizing Tap",
    "Blissful Barrel",
    "Harmony Hop",
    "Cask Canvas",
    "Twilight Tavern",
    "Brazen Brew",
    "Regal Rum",
    "Sleek Suds",
    "Ivory Inn",
    "Velvet Venue",
    "Glistening Goblet",
    "Radiant Rendezvous",
    "Moonstone Mug",
    "Frosted Firkin",
    "Golden Grotto",
    "Sapphire Suds",
    "Cask Crystal",
    "Noble Nectar",
    "Brewers' Bounty",
    "Epicurean Elixir",
    "Gleaming Goblet",
    "Whimsy Whistle",
    "Sable Spirits",
    "Lustrous Lager",
    "Amber Ambiance",
    "Vivid Vessel",
    "Regal Refectory",
    "Brew Bliss",
    "Pristine Pint",
    "Epic Ale",
    "Aether Ale",
    "Celestial Cellar",
    "Crimson Chalice",
    "Enchanted Ember",
    "Jovial Jug",
    "Vibrant Vessel",
    "Majestic Malt",
    "Serene Spirits",
    "Enchanting Elixir",
    "Gilded Goblet",
    "Twilight Tavern",
    "Fireside Firkin",
    "Imperial Inn",
    "Whiskey Whistle",
    "Pristine Pint",
    "Noble Nectar",
]



for i in range(numberOfPubs):
    # write a new line
    file.write("\n")

    # write the ID
    file.write(str(i))
    file.write(",")

    # write the name
    file.write(pub_names[i])
    file.write(",")

    # write the opening time
    openingTime = np.random.randint(openingTimeRange[0], openingTimeRange[1])
    file.write(str(openingTime))
    file.write(",")

    # write the closing time
    closingTime = np.random.randint(closingTimeRange[0], closingTimeRange[1])

    # closing time must be larger than opening time
    while(closingTime < openingTime):
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
    file.write(",")

    # # write the peak time
    peakTimeT = np.random.randint(peakTime[0], peakTime[1])

    # peak time must be between opening and closing time
    while(peakTimeT < openingTime or peakTimeT > closingTime):
        peakTimeT = np.random.randint(peakTime[0], peakTime[1])


    file.write(str(peakTimeT))


# close the file
file.close()