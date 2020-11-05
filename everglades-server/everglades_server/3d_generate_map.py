from queue import Queue
import random
import json
import numpy as np
import os

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

#Global Variable
directionX = [0, 0, 1, 1, 1, 0, -1, -1, -1]
directionY = [0, -1, -1, 0, 1, 1, 1, 0, -1]
nodeCount = 0
nodeDensityWeight = .5
nodeCreatedWeight = 1
nodeFailedWeight = .4
fortressWeight = 0.2
watchtowerWeight = 0.8
nodeDistance = 3
outputFile = "/Everglades/config/3DRandomMap.json"

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
    startingPoint = Point(int(xLen/2), int(yLen/2), 0)

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
                if i == 0 and k == 0:
                    None
                elif (currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0
                        or currentPoint.y + directionY[i] >= yLen or map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] != 0):
                    numPossibleConnections -= 1
                i += 1
            k += 1

        #If there are no possible connections skip to the next point in the queue
        if numPossibleConnections == 0:
            continue

        # print(numPossibleConnections)
        # weight = nodeDensityWeight/numPossibleConnections
        weight = .1
        
        #Iterate through the possible connections, creating a node from a random chance
        #k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 9:
                # print("i = {}".format(i))
                # print(map[0])
                # print("Checking point: {} {} {}".format(currentPoint.z + k, currentPoint.y + directionY[i], currentPoint.x + directionX[i]))
                if i == 0 and k == 0:
                    None
                elif (currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0 
                        or currentPoint.y + directionY[i] >= yLen):
                    a = 0
                elif map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] == 0:
                    randVal = random.random()
                    # print(randVal)
                    if randVal <= weight:
                        #print("Random: ", randVal, " Weight: ", weight, " numPossibleConnections: ", numPossibleConnections)
                        # print("Adding new point")
                        map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = 1
                        newPoint = Point(currentPoint.x + directionX[i], currentPoint.y + directionY[i], currentPoint.z + k)
                        queue.put(newPoint)
                        nodeCount += 1
                        weight = weight - (nodeCreatedWeight/numPossibleConnections)
                        if weight < 0:
                            weight = 0
                    else:
                        # print("Skipped point")
                        map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = -1
                        weight = weight + (nodeFailedWeight/numPossibleConnections) * 2
                        if weight > 1:
                            weight = 1
                i += 1
            k += 1

    #Fill in leftover 0s as -1s
    i = 0
    regenerate = False
    while i < int(zLen/2):
        j = 0
        sanityCheck = 0
        while j < yLen:
            k = 0
            while k < xLen:
                if map[i][j][k] == 0:
                    map[i][j][k] = -1
                if map[i][j][k] == 1:
                    sanityCheck += 1
                k += 1
            j += 1
        if sanityCheck == 0:
            print("WARNING LAYER ", i, " HAS NO NODES")
            regenerate = True
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
    # weight = (nodeDensityWeight / 17)
    weight = .1
    global nodeCount
    nodeCenterCount = 0
    i = 0
    while i < yLen:
        j = 0
        while j < xLen:
            currentPoint = Point(j, i, zCenter)
            hasConnection = False
            k = 0
            while k < 2:
                h = 0
                while h < 9:
                    if i == 0 and k == 0:
                        None
                    elif (currentPoint.x + directionX[h] >= 0 and currentPoint.x + directionX[h] < xLen and currentPoint.y + directionY[h] >= 0
                            and currentPoint.y + directionY[h] < yLen and map[currentPoint.z + k][currentPoint.y + directionY[h]][currentPoint.x + directionX[h]] > 0):
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
                weight = weight - (nodeCreatedWeight/17)
                if weight < 0:
                    weight = 0
            else:
                map[zCenter][currentPoint.y][currentPoint.x] = -1
                weight = weight + (nodeFailedWeight/17)
                if weight < 0:
                    weight = 0
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

def GenerateJsonFile(xLen, yLen, zLen, map):
    jsonData = {}
    nodes = []

    # #Generate P0 Base Node
    # first_node = {}
    firstPoint = Point(int(xLen/2), int(yLen/2), 0)
    # first_node_connections = discoverConnections(map, firstPoint, xLen, yLen, zLen)
    # first_node["Connections"] = first_node_connections
    # first_node["ID"] = (firstPoint.y * xLen) + (firstPoint.x) + (xLen * yLen * firstPoint.z) + 1
    # first_node["Radius"] = 1
    # resource1 = []
    # first_node["Resource"] = resource1
    # first_node["StructureDefense"] = 1
    # first_node["TeamStart"] = 0
    # first_node["ControlPoints"] = 500
    # nodes.append(first_node)
    
    # #Generate P1 Base Node
    # last_node = {}
    lastPoint = Point(int(xLen/2), int(yLen/2), zLen - 1)
    # last_node_connections = discoverConnections(map, lastPoint, xLen, yLen, zLen)
    # last_node["Connections"] = last_node_connections
    # last_node["ID"] = (lastPoint.y * xLen) + (lastPoint.x) + (xLen * yLen * lastPoint.z) + 1
    # last_node["Radius"] = 1
    # resource1 = []
    # last_node["Resource"] = resource1
    # last_node["StructureDefense"] = 1
    # last_node["TeamStart"] = 1
    # last_node["ControlPoints"] = 500

    # print("main json loop")
    #Generate Json for all other nodes
    i = 0
    while i < zLen:
        j = 0
        while j < yLen:
            k = 0
            while k < xLen:
                if map[i][j][k] > 0:
                    tmp_node = {}
                    nodeID = (j * xLen) + k + (xLen * yLen * i) + 1
                    connections = discoverConnections(map, Point(k, j, i), xLen, yLen, zLen)
                    tmp_node["Connections"] = connections
                    tmp_node["ID"] = nodeID
                    tmp_node["Radius"] = 1
                    tmp_node["Resource"] = []
                    tmp_node["StructureDefense"] = 1

                    if k == firstPoint.x and j == firstPoint.y and i == firstPoint.z:
                        tmp_node["TeamStart"] = 0
                    elif k == lastPoint.x and j == lastPoint.y and i == lastPoint.z:
                        tmp_node["TeamStart"] = 1
                    else:
                        tmp_node["TeamStart"] = -1
                    
                    tmp_node["ControlPoints"] = 100
                    nodes.append(tmp_node)
                #print("k: ", k, "j: ", j, "i: ", i)
                k += 1
            j += 1
        i += 1

    # nodes.append(last_node)

    jsonData["__type"] = "Map:#Everglades_MapJSONDef"
    jsonData["MapName"] = "3DRandom"
    jsonData["Xsize"] = xLen
    jsonData["Ysize"] = yLen
    jsonData["Zsize"] = zLen
    jsonData["nodes"] = nodes
    FileO = open(r"3dmapconnection.json", "w")
    FileO.write(json.dumps(jsonData, indent = 4))
    FileO.close()

def discoverConnections(map, point, xLen, yLen, zLen):
    # print("checking around the point z = ", point.z, " y = ", point.y, " x = ", point.x)
    connections = []
    k = -1
    while k < 2:
        i = 0
        while i < 9:
            if (point.z + k < 0 or point.z + k >= zLen or point.x + directionX[i] < 0 or point.x + directionX[i] >= xLen or point.y + directionY[i] < 0
            or point.y + directionY[i] >= yLen or (i == 0 and k == 0)):
                None
            elif map[point.z + k][point.y + directionY[i]][point.x + directionX[i]] == 1:
                # print("connection z = ", point.z + k, " y = ", point.y + directionY[i], " x = ", point.x + directionX[i])
                conNodeId = ((point.y + directionY[i]) * xLen) + (point.x + directionX[i]) + (xLen * yLen * (point.z + k)) + 1
                tmp_conn = {}
                tmp_conn["ConnectedID"] = conNodeId
                tmp_conn["Distance"] = 3
                connections.append(tmp_conn)
            i += 1
        k += 1
    return connections

x = 5
y = 3
z = 5
map = createCube(x, y, z)
generateMap(x, y, z, map)
generateCenterPlane(x, y, z, map)
print("Nodes: {}".format(nodeCount))
#printMap(map)

temp = {"x": x, "y": y, "z": z, "gameboard":map}
mapjson = json.dumps(temp, sort_keys=True, indent = 4)
#mapjson = json.dumps(map)

FileO = open(os.path.abspath('config/3dmap.json'), "w")
FileO.write(mapjson)
FileO.close()

GenerateJsonFile(x, y, z, map)
# print("done")

#print(arry)
#printMap(map)

#Add node types to json

#What if a layer has no nodes?

#Randomly generate watchtower, fortress, etc...