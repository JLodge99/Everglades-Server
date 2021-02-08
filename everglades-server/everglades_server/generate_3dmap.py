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

# Global Variable
directionX = [0, 0, 1, 1, 1, 0, -1, -1, -1]
directionY = [0, -1, -1, 0, 1, 1, 1, 0, -1]
nodeCount = 0
nodeDensityWeight = .1
nodeCreatedWeight = .5
nodeFailedWeight = .1
fortressWeight = 0.2
watchtowerWeight = 0.8
nodeDistance = 3
config_dir = os.path.abspath('config')

# Prints each 2D array in the 3D array
def printMap(map):
    length = len(map)
    count = 0
    for i in map:
        for k in i:
            print(k)
        print("Layer {}".format(count))
        count += 1

# Initializes a 3D array to represent the game board
def createCube(xLen, yLen, zLen):
    map = [[[0 for x in range(xLen)] for y in range(yLen)] for z in range(zLen)]
    return map

# Main function
# Recommended settings for weight
# Bellcurve Enable:   Weightinit should be .3 - .9
# Bellcurve Disable:  Weightinit should be .1 - .3
def generateMap(xLen, yLen, zLen, map, weightinit, bellcurve):
    global nodeCount
    queue = Queue()
    startingPoint = Point(int(xLen/2), int(yLen/2), 0)

    # Starting point is the middle of the plane of layer 0
    map[startingPoint.z][startingPoint.y][startingPoint.x] = 1
    queue.put(startingPoint)
    nodeCount = 1

    while not queue.empty():
        currentPoint = queue.get()
        numPossibleConnections = 17

        # Checks how many possible points a node can be made in by checking the surrounding nodes
        # k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 9:
                if i == 0 and k == 0:
                    # Ignore current point
                    None
                elif (currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0
                        or currentPoint.y + directionY[i] >= yLen or map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] != 0):
                    numPossibleConnections -= 1
                i += 1
            k += 1

        # If there are no possible connections skip to the next point in the queue
        if numPossibleConnections == 0:
            continue

        # weight = nodeDensityWeight/numPossibleConnections
        weight = weightinit
        
        # Iterate through the possible connections, creating a node from a random chance
        # k = 0 is the current layer and k = 1 is next layer
        k = 0
        while k < 2:
            i = 0
            while i < 9:
                if i == 0 and k == 0:
                    None
                elif (currentPoint.z + 1 >= int(zLen/2) or currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= xLen or currentPoint.y + directionY[i] < 0 
                        or currentPoint.y + directionY[i] >= yLen):
                    # Current point is out of bounds, do nothing
                    a = 0
                elif map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] == 0:
                    randVal = random.random()
                    totalBell = (bellCurveVal(currentPoint.z + 1, zLen) * bellCurveVal(currentPoint.y + 1, yLen) * bellCurveVal(currentPoint.x + 1, xLen))
                    tempweight = weightinit * totalBell

                    if randVal <= (tempweight if bellcurve else weight):
                        # Creating a new node
                        nodeTypeRandVal = random.random()

                        # Set node type
                        if nodeTypeRandVal < fortressWeight:
                            map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = 2
                        elif nodeTypeRandVal > watchtowerWeight:
                            map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = 3
                        else:
                            map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = 1

                        # Add newly created point to BFS queue and decrease weight to encourage sparse creation
                        newPoint = Point(currentPoint.x + directionX[i], currentPoint.y + directionY[i], currentPoint.z + k)
                        queue.put(newPoint)
                        nodeCount += 1

                        # weight = weight - (nodeCreatedWeight/numPossibleConnections)
                        weight -= nodeCreatedWeight

                        if weight < 0:
                            weight = 0
                    else:
                        # Node not created, increase weight to prevent dead ends
                        map[currentPoint.z + k][currentPoint.y + directionY[i]][currentPoint.x + directionX[i]] = -1

                        # weight = weight + (nodeFailedWeight/numPossibleConnections)
                        weight += nodeFailedWeight

                        if weight > 1:
                            weight = 1
                i += 1
            k += 1

    # Fill in leftover 0s as -1s
    # Check if a layer contains 0 nodes
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
                if map[i][j][k] > 0:
                    sanityCheck += 1
                k += 1
            j += 1
        if sanityCheck == 0:
            print("WARNING LAYER ", i, " HAS NO NODES")
            regenerate = True
            return True
        i += 1

    # Mirror map to opposite side to create fair board
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

    # Multiplied by 2 to account for the mirrored side
    nodeCount *= 2

    # Generate if the is a center plane. When zLen is odd
    if zLen % 2 != 0:
        generateCenterPlane(xLen, yLen, zLen, map, weightinit)
    return False

# Center Plane Function
def generateCenterPlane(xLen, yLen, zLen, map, weightinit):
    zCenter = int(zLen / 2)
    # weight = (nodeDensityWeight / 17)
    weight = weightinit
    global nodeCount
    nodeCenterCount = 0

    # Check if there is a connection to both sides on the center plane, if not continue to next point
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

            # Create a node randomly
            randVal = random.random()
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

    # If 0 nodes have been generated in the center plane, rerun algorithm
    if nodeCenterCount == 0:
        print("Center plane has 0 nodes, regenerating")
        for i in range(yLen):
            for j in range(xLen):
                map[zCenter][i][j] = 0
        map[zCenter]
        generateCenterPlane(xLen, yLen, zLen, map)

# Generate json file to hold map data
def generateJsonFile(xLen, yLen, zLen, map):
    jsonData = {}
    nodes = []

    # Generate P0 Base Node
    p0basePoint = Point(int(xLen/2), int(yLen/2), 0)
    p0baseID = getNodeID(p0basePoint, xLen, yLen, zLen)
    
    # Generate P1 Base Node
    p1basePoint = Point(int(xLen/2), int(yLen/2), zLen - 1)
    p1baseID = getNodeID(p1basePoint, xLen, yLen, zLen)

    # Generate Json for all nodes
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
                    tmp_node["StructureDefense"] = 1

                    # Set different values for base and nonbase nodes
                    if k == p0basePoint.x and j == p0basePoint.y and i == p0basePoint.z:
                        tmp_node["TeamStart"] = 0
                        tmp_node["ControlPoints"] = 500
                        tmp_node["StructureDefense"] = 1
                    elif k == p1basePoint.x and j == p1basePoint.y and i == p1basePoint.z:
                        tmp_node["TeamStart"] = 1
                        tmp_node["ControlPoints"] = 500
                        tmp_node["StructureDefense"] = 1
                    else:
                        tmp_node["TeamStart"] = -1
                        tmp_node["ControlPoints"] = 100
                        firstNodeSearch = {'ConnectedID': p0baseID, 'Distance': nodeDistance}
                        lastNodeSearch = {'ConnectedID': p1baseID, 'Distance': nodeDistance}
                        if firstNodeSearch in connections or lastNodeSearch in connections:
                            tmp_node["StructureDefense"] = 1.5
                        else: 
                            tmp_node["StructureDefense"] = 1.25

                    # Set node type: fortress, watchtower
                    resource = []
                    if map[i][j][k] == 2:
                        resource.append("DEFENSE")
                    elif map[i][j][k] == 3:
                        resource.append("OBSERVE")
                    
                    tmp_node["Resource"] = resource
                    nodes.append(tmp_node)
                k += 1
            j += 1
        i += 1

    # Create json file
    jsonData["__type"] = "Map:#Everglades_MapJSONDef"
    jsonData["MapName"] = "3DRandom"
    jsonData["Xsize"] = xLen
    jsonData["Ysize"] = yLen
    jsonData["Zsize"] = zLen
    jsonData["Type"] = "3D"
    jsonData["nodes"] = nodes
    FileO = open(os.path.join(config_dir, "3dmap.json"), "w")
    FileO.write(json.dumps(jsonData, indent = 4))
    FileO.close()

# Json helper function, get surrounding nodes. Returns a dict of connection nodes
def discoverConnections(map, point, xLen, yLen, zLen):
    connections = []

    # Checks surrounding nodes. k = -1 as previous layer and k = 1 as next layer
    k = -1
    while k < 2:
        i = 0
        while i < 9:
            if (point.z + k < 0 or point.z + k >= zLen or point.x + directionX[i] < 0 or point.x + directionX[i] >= xLen or point.y + directionY[i] < 0
            or point.y + directionY[i] >= yLen or (i == 0 and k == 0)):
                # Out of bounds or ignore current point, do nothing
                None
            elif map[point.z + k][point.y + directionY[i]][point.x + directionX[i]] > 0:
                conNodeId = ((point.y + directionY[i]) * xLen) + (point.x + directionX[i]) + (xLen * yLen * (point.z + k)) + 1
                tmp_conn = {}
                tmp_conn["ConnectedID"] = conNodeId
                tmp_conn["Distance"] = nodeDistance
                connections.append(tmp_conn)
            i += 1
        k += 1
    return connections

# Convert (z, y, x) to node id.
def getNodeID(point, xLen, yLen, zLen):
    return (point.y * xLen) + point.x + (xLen * yLen * point.z) + 1

# Bellcurve functions returns a value (0,1]
def bellCurveVal(x, zLen):
    return - ( pow((x / ((zLen + 1) / 2)) - 1, 2)) + 1

# Main execute function
def exec(xLen, yLen, zLen, weight = .1, bellcurve = False):
    loop = True
    while loop:
        map = createCube(xLen, yLen, zLen)
        loop = generateMap(xLen, yLen, zLen, map, weight, bellcurve)
        print("Empty node, regenerating")
    generateJsonFile(xLen, yLen, zLen, map)

# Testing statements
# exec(5, 5, 7)
# print("Nodecount: ", nodeCount)