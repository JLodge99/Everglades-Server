from queue import Queue
import random
import json

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

#Global Variable
directionX = [0, 1, 1, 1, 0, -1, -1, -1]
directionY = [-1, -1, 0, 1, 1, 1, 0, -1]
nodeDensityWeight = 3

#Prints each 2D array in the 3D array
def printMap(map):
    length = len(map)
    count = 0
    for i in map:
        for k in i:
            print(k)
        print("Layer {}".format(count))
        count += 1

#Initializes a 3D array to represent the game board
def createCube(size):
    map = [[[0 for x in range(size)] for y in range(size)] for z in range(size)]
    return map

#Main function
def generateMap(size, map):
    queue = Queue()
    nodeCount = 1
    startingPoint = Point()
    startingPoint.x = int(size/2)
    startingPoint.y = int(size/2)

    #Starting point is the middle of the plane of layer 0
    map[startingPoint.z][startingPoint.y][startingPoint.x] = 1

    queue.put(startingPoint)

    while not queue.empty():
        currentPoint = queue.get()
        numPossibleConnections = 17
        # print("Current: {} {} {}".format(currentPoint.z, currentPoint.y, currentPoint.x))

        #Checks how many possible points a node can be made in
        #k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 8:
                if currentPoint.z + 1 >= int(size/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= size or currentPoint.y + directionY[i] < 0 or currentPoint.y + directionY[i] >= size or map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] != 0:
                    numPossibleConnections -= 1
                i += 1
            k += 1

        #If there are no possible connections skip to the next point in the queue
        if numPossibleConnections == 0:
            continue

        # print(numPossibleConnections)
        weight = nodeDensityWeight/numPossibleConnections
        
        #Iterate through the connections creating a node from a random chance
        #k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 8:
                # print("i = {}".format(i))
                # print(map[0])
                # print("Checking point: {} {} {}".format(currentPoint.z + k, currentPoint.y + directionY[i], currentPoint.x + directionX[i]))
                if currentPoint.z + 1 >= int(size/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= size or currentPoint.y + directionY[i] < 0 or currentPoint.y + directionY[i] >= size:
                    a = 0
                elif map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] == 0:
                    randVal = random.random()
                    # print(randVal)
                    if randVal <= weight:
                        # print("Adding new point")
                        map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = 1
                        newPoint = Point()
                        newPoint.x = currentPoint.x + directionX[i]
                        newPoint.y = currentPoint.y + directionY[i]
                        newPoint.z = currentPoint.z + k
                        queue.put(newPoint)
                        nodeCount += 1
                    else:
                        # print("Skipped point")
                        map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = -1
                i += 1
            k += 1

    #Fill in leftover 0s as -1s
    i = 0
    while i < int(size/2):
        j = 0
        while j < size:
            k = 0
            while k < size:
                if map[i][j][k] == 0:
                    map[i][j][k] = -1
                k += 1
            j += 1
        i += 1

    #Mirror map to opposite side
    i = 0
    while i < int(size/2):
        j = 0
        while j < size:
            k = 0
            while k < size:
                map[size - 1 - i][j][k] = map[i][j][k]
                k += 1
            j += 1
        i += 1

    #Multiplied by 2 to account for the mirrored side
    print("Nodes: {}".format(nodeCount * 2))

size = 5
map = createCube(size)
generateMap(size, map)
printMap(map)

#Center Plane Function

#Create json file function