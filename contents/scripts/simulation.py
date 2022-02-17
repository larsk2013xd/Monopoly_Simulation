import numpy as np
import matplotlib.pyplot as plt
import imageio
import array
import os

boardColors = ["#AAAAAA"]*41
boardNamesEN_UK = ["Go", "Old Kent Road", "Community Chest #1", "Whitechapel Road", "Income Tax", "Kings Cross Station", "The Angel, Islington", "Chance #1", "Euston Road", "Pentonville Road", "Just visiting", "Pall Mall", "Electric Company", "Whitehall", "Norththumbn'd Avenue", "Marylebone Station", "Bow street", "Community Chest #2", "Marlborough Street", "Vine street", "Free Parking", "Strand", "Chance #2", "Fleet Street", "Trafalgar Square", "Fenchurch St. Station", "Leicester Square", "Coventry Street", "Water Works", "Piccadilly", "Go To Jail", "Regent Street", "Oxford Street", "Community Chest #3", "Bond Street", "Liverpool St. Station", "Chance #3", "Park Lane", "Super Tax", "Mayfair", "In Jail"]

colorBase = ["brown", "#AAAAFF", "purple", "orange", "red", "yellow", "green", "blue"]

#Grouping by squares
brownGroup = [1, 3]
lblueGroup = [6, 8, 9]
purpleGroup = [11, 13, 14]
orangeGroup = [16, 18, 19]
redGroup = [21, 23, 24]
yellowGroup = [26, 27, 29]
greenGroup = [31, 32, 34]
blueGroup = [39, 37]

chanceGroup = [7, 22, 36]
communityGroup = [2, 17, 33]
stationGroup = [5, 15, 25, 35]
utilsGroup = [12, 28]
taxGroup = [4, 38]
jailGroup = [40]
toJailGroup = [30]
freeParkingGroup = [20]
justVisitingGroup = [10]

i = 0
for group in [brownGroup, lblueGroup, purpleGroup, orangeGroup, redGroup, yellowGroup, greenGroup, blueGroup]:
    for index in group:
        boardColors[index] = colorBase[i]
    
    i += 1



def densityPlot(density, sname, printPilon = False, pilonSquare = 0, makeDensity = True, animate = False): #This function has to be re-done. It's quite messy
    
    origDensity = density
    
    if makeDensity:
        density = density/np.sum(density)
    
    plt.clf()
    fig, (boardPlot) = plt.subplots(1)
    boardImg = plt.imread("../article_raw/images/board.jpg")
    boardPlot.imshow(boardImg, extent=[0,1,0,1])

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
    squareCenters[40] = np.array([1.5/11, 1.5/11])

    x = np.zeros(41)
    y = np.zeros(41)
    for i in range(41):
        x[i] = squareCenters[i][0]
        y[i] = squareCenters[i][1]
        
        
    colors = density
    boardPlot.axis('off')
    #plt.scatter(x, y, marker = 's', s = 5000*density, c =density, cmap='RdYlGn')
    
    for i in range(41):
        green = 1/max(density) * density[i]
        white = 1
        if printPilon and i == pilonSquare:
            boardPlot.annotate(str(np.round(density[i]*100, decimals = 1)) + "%", (x[i], y[i]), fontsize = 2, horizontalalignment = 'center')
        else:
            boardPlot.annotate(str(np.round(density[i]*100, decimals = 1)) + "%", (x[i], y[i]), fontsize = 2, backgroundcolor = (1-green, 1, 1-green, 0.7 ), horizontalalignment = 'center')
    
    
   
    
    
    if printPilon:
       boardPlot.scatter(x = squareCenters[pilonSquare][0], y = squareCenters[pilonSquare][1], s = 100, c = "red")
    plt.savefig("../article_raw/images/" + sname, dpi = 500, bbox_inches = 'tight') 
    plt.close()

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
        if pos > 29 or pos < 12 : return 12 #electricit
        if pos < 29 and pos > 12 : return 28 #water mains
    elif pickedCard == 10 : return pos - 3 # Go back 3 spots
    elif pickedCard == 11 : return 40 # Go To Jail
    elif pickedCard == 14 : return 5 # Rearing Railroad
    else: return pos # Chance card does not move player (Money related)
    
def grabCommunityCard(pos):

    pickedCard = np.random.randint(low = 1, high = 17)
    if pickedCard == 1: return 0 # Go to start
    elif pickedCard == 2: return 40 # Go To jail
    else: return pos # Community card does not move player (Money related)
    
def doThrowOnPos(position, nDoubles = 0):
    
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

def simulateThrowOnPos(position, nSims):
    
    freqList = np.zeros(41)
    
    for i in range(nSims):
        freqList[doThrowOnPos(position)[0]] += 1
        
    return freqList

def simulateGame(nTurns):
    
    positions = np.zeros(nTurns, dtype = int)
    doubles = 0
    
    for i in range(nTurns):
        if i == 0 : (positions[i], doubles) = doThrowOnPos(0, doubles)
        else : (positions[i], doubles) = doThrowOnPos(positions[i-1], doubles)

    return positions

def simulateGames(nSims, nTurns):
    
    print("Simulating many games...")
    freqArray = np.zeros(41, dtype = int)
    
    for i in range(nSims):
        positions = simulateGame(nTurns)
        freqArray[positions] += 1
    
    return freqArray


