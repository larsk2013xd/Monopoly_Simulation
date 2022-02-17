import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
browns = np.array([1, 3])
lblues = np.array([6, 8, 9])
purples = np.array([11, 13, 14])
oranges = np.array([16, 18, 19])
reds = np.array([21, 23, 24])
yellows = np.array([26, 27, 29])
greens = np.array([31, 32, 34])
blues = np.array([37, 39])
 
doubles = 0
def densityPlot(density, sname, printPilon, pilonSquare):
    
    
    
    plt.clf()
    boardImg = plt.imread("../article_raw/images/board.jpg")
    plt.imshow(boardImg, extent=[0,1,0,1])

    squares = range(40) # Indexing all squares
    xCenters = 0.189 + np.array(range(9)) * (0.62 / 8)

    yCenters = 0.189 + np.array(range(9)) * (0.62 / 8)
    squareCenters = np.array([[2]*2]*40, dtype= float)

    for i in range(1,10):
        squareCenters[i] = np.array([xCenters[9-i], 1/11])

    for i in range(11, 20):
       squareCenters[i] = [1/11, yCenters[i - 11]]
       
    for i in range(21, 30):
       squareCenters[i] = [xCenters[i - 30], 10/11]
       
    for i in range(31, 40):
        squareCenters[i] = [10/11, yCenters[39-i]]
        
    squareCenters[0] = np.array([10/11, 1/11])
    squareCenters[10] = np.array([1/11, 1/11])
    squareCenters[20] = np.array([1/11, 10/11])
    squareCenters[30] = np.array([10/11, 10/11])

    x = np.zeros(40)
    y = np.zeros(40)
    for i in range(40):
        x[i] = squareCenters[i][0]
        y[i] = squareCenters[i][1]
        
        
    colors = density
    plt.axis('off')
    #plt.scatter(x, y, marker = 's', s = 5000*density, c =density, cmap='RdYlGn')
    
    for i in range(40):
        green = 1/max(density) * density[i]
        red = 1 - green
        if printPilon and i == pilonSquare:
            plt.annotate(str(np.round(density[i]*100, decimals = 2)) + "%", (x[i], y[i]), fontsize = 2, horizontalalignment = 'center')
        else:
            plt.annotate(str(np.round(density[i]*100, decimals = 2)) + "%", (x[i], y[i]), fontsize = 4, backgroundcolor = (red, green, 0, 0.8), horizontalalignment = 'center')
    
    if printPilon:
       plt.scatter(x = squareCenters[pilonSquare][0], y = squareCenters[pilonSquare][1], s = 100, c = "red")
    plt.savefig("../article_raw/images/" + sname, dpi = 500, bbox_inches = 'tight') 
    
def simulateThrowOnPos(position, nSims):
    print("Simulating a throw from position ", position, "...")
    initPos = position
    freqList = np.zeros(40)
    global doubles
    
    for i in range(nSims):
        dies = np.random.randint(low = 1, high = 7, size =2)
        newPosition = position + dies.sum()
        newPosition = newPosition%40
        print("Die roll: ", dies)
        if dies[1]==dies[0]:
            doubles += 1
            print("Threw double!")
        
        else:
            doubles = 0
         
        if doubles == 3:
            print("Threw double three times. On to jail!")
            inJail = True
            jailTries = 0
            doubles = 0
            newPosition = 10
        else:  
            
            print("Thew a ", dies.sum(), ". Going to ", newPosition)
            
            if newPosition == 30 : 
                print("Landed on 30, Go to jail :(")
                newPosition = 10 # Go To Jail
            if newPosition == 7 or newPosition == 22 or newPosition == 36:   # Chance card
                print("Chance card!")
            
                pickedCard = np.random.randint(low = 1, high = 17)
                if pickedCard == 1 :
                    print("Go to boardwalk")
                    newPosition = 39 # Go To Boardwalk
                elif pickedCard == 2 : 
                    print("Go to start")
                    newPosition = 0 # Go To Start
                elif pickedCard == 3 :
                    print("Go to illinois aveneu")
                    newPosition = 23 
                elif pickedCard == 4 : 
                    print(" Go To Saint Charle's place")
                    newPosition = 11 # Go To Saint Charle's place
                elif pickedCard == 5 or pickedCard == 6 :
                    print("Go to nearest station")
                    stationarray = np.asarray([5, 15, 25, 35])
                    if newPosition > 35 : newPosition = 5
                    elif newPosition > 25 : newPosition = 35
                    elif newPosition > 15 : newPosition = 25
                    elif newPosition > 5 : newPosition = 15
                elif pickedCard == 7 :
                    if newPosition > 29 or newPosition < 12 : 
                        print("Head to water mains")
                        newPosition = 12
                    if newPosition < 29 and newPosition > 12 :
                        print("Head to electricity company")
                        newPosition = 29
                elif pickedCard == 10 : 
                    print("Go back 3 spots!")
                    newPosition -= 3
                elif pickedCard == 11 : 
                    print("Picked jail card :(")
                    newPosition = 10
                elif pickedCard == 14 :
                    print("Go to Station")
                    newPosition = 5
                else:
                    print("Money related chance card...")
            if newPosition == 2 or newPosition == 33:
                print("community card")
                pickedCard = np.random.randint(low = 1, high = 17)
                if pickedCard == 1:
                    print("Go to start")
                    newPosition = 0
                elif pickedCard == 2:
                    print("Go to jail")
                    newPosition = 10
                else:
                    print("Money related community card")
        
        freqList[newPosition] += 1
        
        if(nSims == 1):
            return(newPosition)
    
    freqList /= freqList.sum()
    return(freqList)

nSims = 2000
filelist = [None]*nSims
feqList = np.zeros(40)
posPlot = np.array([])
currentPos = 0
for i in range(nSims):
    print(i)
    plt.clf()
    plt.ylim(0,0.07)
    plt.annotate("Turn" + str(i) + "/" + str(nSims), (39, 0.07))
    currentPos = simulateThrowOnPos(currentPos, 1)
    feqList[currentPos] += 1
    posPlot = np.append(posPlot, currentPos)
    N, bins, patches = plt.hist(posPlot, density = True, rwidth = 0.9, bins = range(41), align='mid')
    for j in range(40):
        patches[j].set_facecolor('grey')
    for j in browns:
        patches[j].set_facecolor('brown')
    for j in lblues:
        patches[j].set_facecolor('#AAAAFF')
    for j in purples:
        patches[j].set_facecolor('purple')
    for j in oranges:
        patches[j].set_facecolor('orange')
    for j in reds:
        patches[j].set_facecolor('red')
    for j in yellows:
        patches[j].set_facecolor('yellow')
    for j in greens:
        patches[j].set_facecolor('green')
    for j in blues:
        patches[j].set_facecolor('blue')
    namelist = ["Go", "Old Kent Road", "Community Chest 1", "Whitechapel Road", "Income Tax", "Kings Cross Station", "The Angel, Islington", "Chance 1", "Euston Road", "Pentonville Road", "In jail / Just Visiting", "Pall Mall", "Electric Company", "Whitehall", "Norththumb'nd Avenue", "Marylebone Station", "Bow Street", "Community Chest 2", "Marlborough Street", "Vine Street", "Free Parking", "Strand", "Chance 2", "Fleet Street", "Trafalgar Square", "Fenchurch St. Station", "Leicester Square", "Coventry Street", "Water Works", "Piccadilly", "Go To Jail", "Regent Street", "Oxford Street", "Community Chest 3", "Bond Street", "Liverpool St. Station", "Chance 3", "Park Lane", "Super Tax", "Mayfair"]
    for j in range(40):
        plt.annotate(namelist[j], (j+0.2, 0.001), fontsize = 8, rotation = 90, horizontalalignment = 'left')
    
    filelist[i] = "hist" + str(i)+".png"
    plt.savefig(filelist[i])
    plt.close()

images = []  
for filename in filelist:
    images.append(imageio.imread(filename))
    os.remove(filename)

imageio.mimsave('histGif.gif', images)

feqList /= feqList.sum()    


#densityPlot(feqList, "overall.png", False, 0)

#for i in range(40):
#    densityPlot(simulateThrowOnPos(i, 5000), str(i)+".png", True, i)





    