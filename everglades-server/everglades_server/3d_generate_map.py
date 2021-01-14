from queue import Queue
import random
import json
import numpy as np

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

#Global Variable
directionX = [0, 0, 1, 1, 1, 0, -1, -1, -1]
directionY = [0, -1, -1, 0, 1, 1, 1, 0, -1]
nodeDensityWeight = 5
nodeCount = 0

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
def createCube(xLen, yLen, zLen):
    map = [[[0 for x in range(xLen)] for y in range(yLen)] for z in range(zLen)]
    return map

#Main function
def generateMap(xLen, yLen, zLen, map):
    global nodeCount
    queue = Queue()
    startingPoint = Point()
    startingPoint.x = int(xLen/2)
    startingPoint.y = int(yLen/2)

    #Starting point is the middle of the plane of layer 0
    map[startingPoint.z][startingPoint.y][startingPoint.x] = 1

    queue.put(startingPoint)
    nodeCount = 1
    while not queue.empty():
        currentPoint = queue.get()
        numPossibleConnections = 17
        # print("Current: {} {} {}".format(currentPoint.z, currentPoint.y, currentPoint.x))

        #Checks how many possible points a node can be made in
        #k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 9:
                if currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0 or currentPoint.y + directionY[i] >= yLen or map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] != 0:
                    numPossibleConnections -= 1
                i += 1
            k += 1

        #If there are no possible connections skip to the next point in the queue
        if numPossibleConnections == 0:
            continue

        # print(numPossibleConnections)
        weight = nodeDensityWeight/numPossibleConnections
        
        #Iterate through the possible connections, creating a node from a random chance
        #k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 9:
                # print("i = {}".format(i))
                # print(map[0])
                # print("Checking point: {} {} {}".format(currentPoint.z + k, currentPoint.y + directionY[i], currentPoint.x + directionX[i]))
                if currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0 or currentPoint.y + directionY[i] >= yLen:
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
    while i < int(zLen/2):
        j = 0
        while j < yLen:
            k = 0
            while k < xLen:
                if map[i][j][k] == 0:
                    map[i][j][k] = -1
                k += 1
            j += 1
        i += 1

    #Mirror map to opposite side
    i = 0
    while i < int(zLen/2):
        j = 0
        while j < yLen:
            k = 0
            while k < xLen:
                map[zLen - 1 - i][j][k] = map[i][j][k]
                k += 1
            j += 1
        i += 1

    #Multiplied by 2 to account for the mirrored side
    nodeCount *= 2

#Center Plane Function
def generateCenterPlane(xLen, yLen, zLen, map):
    zCenter = int(zLen / 2)
    weight = (nodeDensityWeight / 10)
    global nodeCount
    nodeCenterCount = 0
    i = 0
    while i < yLen:
        j = 0
        while j < xLen:
            currentPoint = Point()
            currentPoint.x = j
            currentPoint.y = i
            currentPoint.z = zCenter
            hasConnection = False
            k = 0
            while k < 2:
                h = 0
                while h < 9:
                    if currentPoint.x + directionX[h] >= 0 and currentPoint.x + directionX[h] < xLen and currentPoint.y + directionY[h] >= 0 and currentPoint.y + directionY[h] < yLen and map[currentPoint.z + k][currentPoint.y + directionY[h]][currentPoint.x + directionX[h]] > 0:
                        hasConnection = True
                        break
                    h += 1
                k += 1

            randVal = random.random()
            # print(randVal)
            if hasConnection and randVal <= weight:
                map[zCenter][currentPoint.y][currentPoint.x] = 1
                nodeCount += 1
                nodeCenterCount += 1
            else:
                map[zCenter][currentPoint.y][currentPoint.x] = -1
            j += 1
        i += 1
    if nodeCenterCount == 0:
        print("Center plane has 0 nodes, regenerating")
        print(map[zCenter])
        for i in range(yLen):
            for j in range(xLen):
                map[zCenter][i][j] = 0
        map[zCenter]
        generateCenterPlane(xLen, yLen, zLen, map)

x = 5
y = 5
z = 5
map = createCube(x, y, z)
generateMap(x, y, z, map)
generateCenterPlane(x, y, z, map)
print("Nodes: {}".format(nodeCount))
#printMap(map)

mapjson = json.dumps(map)

# FileO = open(r"3dmap.json", "w")
# FileO.write(mapjson)
# FileO.close()

#print(arry)

#Create json file function

#What if a layer has no nodes?

#Adjust the weights, less chance of a full layer of nodes

#Randomly generate watchtower, fortress, etc...