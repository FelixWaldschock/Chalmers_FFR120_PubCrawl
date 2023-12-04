# import csv
# import numpy as np
# import matplotlib.pyplot as plt

# ListPopularity = []
# ListPeakTime = []
# ListClosingTime = []
# ListOpeningTime = []
# ListBarnames = []
# ListSigmas = []

# with open('pubs.csv', 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         ListPopularity.append(int(row['Popularity']))
#         ListPeakTime.append(int(row['PeakTime']))
#         ListClosingTime.append(int(row['ClosingTime']))
#         ListOpeningTime.append(int(row['OpeningTime']))
#         ListBarnames.append(row['Name'])
#         ListSigmas.append(int(row['Sigma']))

# def getWAAATime(peakTime, popularity, currentTime, openingTime,sigma):
#     waitingTime = 0

#     if openingTime > currentTime:
#         waitingTime += openingTime - currentTime
#     mu = peakTime
#     term1 = popularity
#     term2 = np.exp(-0.5 * ((currentTime - mu) / sigma) ** 2)
#     queueLength = term1 * term2

#     waitingTime += queueLength

#     return waitingTime

# # Set the desired set ID
# set_id = 3

# # Get data for the selected set ID
# popularity = ListPopularity[set_id - 1]
# peakTime = ListPeakTime[set_id - 1]
# closingTime = ListClosingTime[set_id - 1]
# openingTime = ListOpeningTime[set_id - 1]
# bar_name = ListBarnames[set_id - 1]
# sigma = ListSigmas[set_id - 1]

# # Create a single set of time values from -10 to 730
# time = np.linspace(0, 720, 720)

# # Create a single plot for the selected set ID
# plt.figure(figsize=(16, 8))

# # Plot the queue for the selected set ID
# queue = [getWAAATime(peakTime, popularity, t, openingTime,sigma) for t in time]
# plt.plot(time, queue, label=f'Queue for {bar_name}')

# # Add vertical dashed lines at openingTime and closingTime
# plt.axvline(x=openingTime, color='g', linestyle='--', label='Opening Time')
# plt.axvline(x=closingTime, color='r', linestyle='--', label='Closing Time')

# # Set labels, title, and legend
# plt.xlabel('Time in minutes')
# plt.ylabel('Queue Length')
# plt.title(f'Queue Length Over Time for {bar_name}')
# plt.legend()
# plt.show()

import csv
import numpy as np
import matplotlib.pyplot as plt

ListPopularity = []
ListPeakTime = []
ListClosingTime = []
ListOpeningTime = []
ListBarnames = []
ListSigmas = []

with open('pubs.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        ListPopularity.append(int(row['Popularity']))
        ListPeakTime.append(int(row['PeakTime']))
        ListClosingTime.append(int(row['ClosingTime']))
        ListOpeningTime.append(int(row['OpeningTime']))
        ListBarnames.append(row['Name'])
        ListSigmas.append(int(row['Sigma']))

def getWAAATime(peakTime, popularity, currentTime, openingTime, sigma):
    waitingTime = 0

    if openingTime > currentTime:
        waitingTime += openingTime - currentTime
    mu = peakTime
    term1 = popularity
    term2 = np.exp(-0.5 * ((currentTime - mu) / sigma) ** 2)
    queueLength = term1 * term2

    waitingTime += queueLength

    return waitingTime

# Create a single figure for all plots
plt.figure(figsize=(16, 8))

# Iterate through each set ID and plot the queue
for set_id in range(1, len(ListPopularity) + 1):
    popularity = ListPopularity[set_id - 1]
    peakTime = ListPeakTime[set_id - 1]
    closingTime = ListClosingTime[set_id - 1]
    openingTime = ListOpeningTime[set_id - 1]
    bar_name = ListBarnames[set_id - 1]
    sigma = ListSigmas[set_id - 1]

    # Create a single set of time values from -10 to 730
    time = np.linspace(0, 720, 720)

    # Plot the queue for the selected set ID
    queue = [getWAAATime(peakTime, popularity, t, openingTime, sigma) for t in time]
    plt.plot(time, queue, label=f'Queue for {bar_name}')


# Set labels, title, and legend
plt.xlabel('Time in minutes')
plt.ylabel('Queue Length')
plt.title('Queue Length Over Time for Pubs')
plt.legend()
plt.show()
