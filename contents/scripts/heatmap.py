import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

def densityPlot(density, sname, printPilon, pilonSquare):
    
    plt.clf()
    boardImg = plt.imread("../article_raw/images/board.jpg")
    plt.imshow(boardImg, extent=[0,1,0,1])

    squares = range(41) # Indexing all squares
    xCenters = 0.189 + np.array(range(9)) * (0.62 / 8)

    yCenters = 0.189 + np.array(range(9)) * (0.62 / 8)
    squareCenters = np.array([[2]*2]*41, dtype= float)

    for i in range(1,10):
        squareCenters[i] = np.array([xCenters[9-i], 1/11])

    for i in range(11, 20):
       squareCenters[i] = [1/11, yCenters[i - 11]]
       
    for i in range(21, 30):
       squareCenters[i] = [xCenters[i - 30], 10/11]
       
    for i in range(31, 40):
        squareCenters[i] = [10/11, yCenters[39-i]]
        
    squareCenters[0] = np.array([10/11, 1/11])
    squareCenters[10] = np.array([1/12, 1/12])
    squareCenters[20] = np.array([1/11, 10/11])
    squareCenters[30] = np.array([10/11, 10/11])
    squareCenters[40] = np.array([1/11, 1/11])

    x = np.zeros(41)
    y = np.zeros(41)
    for i in range(41):
        x[i] = squareCenters[i][0]
        y[i] = squareCenters[i][1]
        
        
    colors = density
    plt.axis('off')
    #plt.scatter(x, y, marker = 's', s = 5000*density, c =density, cmap='RdYlGn')
    
    for i in range(41):
        green = 1/max(density) * density[i]
        red = 1 - green
        if printPilon and i == pilonSquare:
            plt.annotate(str(np.round(density[i]*100, decimals = 2)) + "%", (x[i], y[i]), fontsize = 2, horizontalalignment = 'center')
        else:
            plt.annotate(str(np.round(density[i]*100, decimals = 2)) + "%", (x[i], y[i]), fontsize = 4, backgroundcolor = (red, green, 0, 0.8), horizontalalignment = 'center')
    
    if printPilon:
       plt.scatter(x = squareCenters[pilonSquare][0], y = squareCenters[pilonSquare][1], s = 100, c = "red")
    plt.savefig("../article_raw/images/" + sname, dpi = 500, bbox_inches = 'tight') 

def grabChanceCard(pos):
      
    pickedCard = np.random.randint(low = 1, high = 17)
    
    if pickedCard == 1 : return 39 # Go To Boardwalk
    elif pickedCard == 2 : return 0 # Go To Start
    elif pickedCard == 3 : return 24 # Go to illinois aveneu
    elif pickedCard == 4 : return 11 # Go To Saint Charle's place
    elif pickedCard == 5 or pickedCard == 6 : # Go to nearest station
        if pos > 35 : return 5 # Rearing Railroad
        elif pos > 25 : return 35 # Short Line
        elif pos > 15 : return 25 # B & 0 Railroad
        elif pos > 5 : return 15 # Pennsylvania Railroad
    elif pickedCard == 7 : # Go to nearest Utility
        if pos > 29 or pos < 12 : return 12 #water mains
        if pos < 29 and pos > 12 : return 29 #electricity
    elif pickedCard == 10 : return pos - 3 # Go back 3 spots
    elif pickedCard == 11 : return 40 # Go To Jail
    elif pickedCard == 14 : return 5 # Rearing Railroad
    else: return pos # Chance card does not move player (Money related)
    
def grabCommunityCard(pos):

    pickedCard = np.random.randint(low = 1, high = 17)
    if pickedCard == 1: return 0 # Go to start
    elif pickedCard == 2: return 40 # Go To jail
    else: return pos # Community card does not move player (Money related)
    
def simulateThrowOnPos(position, nDoubles):
    
    dies = np.random.randint(low = 1, high = 7, size =2)
    
    double = (dies[0] == dies[1])
    if double : nDoubles += 1
    else : nDoubles = 0
    if nDoubles == 3: return (40, nDoubles) # 3x Double go to jail
    
    if position == 40 : position = 10 #Assume (FOR NOW) immediate release from jail
    
    newPosition = position + dies.sum()
    newPosition = newPosition%40
    if newPosition == 30 : return (40, nDoubles) # Go To Jail
    if newPosition == 7 or newPosition == 22 or newPosition == 36: return (grabChanceCard(newPosition), nDoubles) # Chance card
    if newPosition == 2 or newPosition == 33 or newPosition == 17: return (grabCommunityCard(newPosition), nDoubles) #Community card
    else: return(newPosition, nDoubles)

def simulateGame(nTurns):
    
    positions = np.zeros(nTurns, dtype = int)
    doubles = 0
    
    for i in range(nTurns):
        if i == 0 : (positions[i], doubles) = simulateThrowOnPos(0, doubles)
        else : (positions[i], doubles) = simulateThrowOnPos(positions[i-1], doubles)

    return positions

def simulateGames(nSims, nTurns):
    
    freqArray = np.zeros(41, dtype = int)
    
    for i in range(nSims):
        positions = simulateGame(nTurns)
        freqArray[positions] += 1
    
    return freqArray




    