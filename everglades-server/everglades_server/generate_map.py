from queue import Queue
import random
import json

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

#Global Variables
outputFile = "/Everglades/config/RandomMap.json"

nodeDensityWeight = 2
nodeCreatedWeight = 0.5
nodeFailedWeight = 0.5
fortressWeight = 0.2
watchtowerWeight = 0.8
nodeDistance = 3

directionX = [0, 1, 1, 1, 0, -1, -1, -1]
directionY = [1, 1, 0, -1, -1, -1, 0, 1]

#Generate Base Map
def GenerateBaseMap(size, map):
    queue = Queue()

    startingPoint = Point()
    startingPoint.x = int(size/2)

    map[startingPoint.x][startingPoint.y] = 1

    queue.put(startingPoint)

    while not queue.empty():
        currentPoint = queue.get()
        numPossibleConnections = 8

        i = 0
        while i < 8:
           if currentPoint.x + directionX[i] < 0 or currentPoint.x + directionX[i] >= size or currentPoint.y + directionY[i] < 0 or currentPoint.y + directionY[i] >= int(size/2) or map[currentPoint.x + directionX[i]][currentPoint.y + directionY[i]] != 0:
               numPossibleConnections = numPossibleConnections - 1
           i = i + 1

        if numPossibleConnections == 0:
            continue
        
        weight = nodeDensityWeight/numPossibleConnections

        offset = int(random.uniform(0, size - 1))

        i = 0
        while i < 8:
            if currentPoint.x + directionX[(i + offset)%8] < 0 or currentPoint.x + directionX[(i + offset)%8] >= size or currentPoint.y + directionY[(i + offset)%8] < 0 or currentPoint.y + directionY[(i + offset)%8] >= int(size/2):
                a = 0
                #Do Nothing
            elif map[currentPoint.x + directionX[(i + offset)%8]][currentPoint.y + directionY[(i + offset)%8]] == 0:
                testValue = random.random()

                if testValue <= weight:
                    testValue2 = random.random()

                    if testValue2 < fortressWeight:
                        map[currentPoint.x + directionX[(i + offset)%8]][currentPoint.y + directionY[(i + offset)%8]] = 2
                    elif testValue2 > watchtowerWeight:
                        map[currentPoint.x + directionX[(i + offset)%8]][currentPoint.y + directionY[(i + offset)%8]] = 3
                    else:
                        map[currentPoint.x + directionX[(i + offset)%8]][currentPoint.y + directionY[(i + offset)%8]] = 1
                    
                    newPoint = Point()
                    newPoint.x = currentPoint.x + directionX[(i + offset)%8]
                    newPoint.y = currentPoint.y + directionY[(i + offset)%8]
                    queue.put(newPoint)
                    weight = weight - (nodeCreatedWeight/numPossibleConnections)
                    if weight < 0:
                        weight = 0
                else:
                    map[currentPoint.x + directionX[(i + offset)%8]][currentPoint.y + directionY[(i + offset)%8]] = -1

                    weight = weight + (nodeCreatedWeight/numPossibleConnections) * 2
                    if weight > 1:
                        weight = 1
            i = i + 1

    #Fill in leftover 0s as -1s
    i = 0
    while i < int(size/2):
        j = 0
        while j < size:
            if map[j][i] == 0:
                map[j][i] = -1
            j = j + 1
        i = i + 1

    #Mirror map to opposite side
    i = 0
    while i < size:
        j = 0
        while j < int(size/2):
            map[i][size - 1 - j] = map[i][j]
            j = j + 1
        i = i + 1

    if size%2 != 0:
        GenerateCenterLine(size, map)
    return;

#Generate Center Line
def GenerateCenterLine(size, map):
    numNodes = 0
    weight = ((nodeDensityWeight + 2)/8)
    offset = int(random.uniform(0, size - 1))

    i = 0
    while i < size:
        currentPoint = Point()
        currentPoint.x = (i + offset)%size
        currentPoint.y = int(size/2)

        hasConnection = False
        j = 0
        while j < 8:
            if currentPoint.x + directionX[j] >= 0 and currentPoint.x + directionX[j] < size and currentPoint.y + directionY[j] >= 0 and currentPoint.y + directionY[j] < size and map[currentPoint.x + directionX[j]][currentPoint.y + directionY[j]] > 0:
                hasConnection = True
                break
            j = j + 1

        testValue = random.random()

        if hasConnection and testValue <= weight:
            map[(i + offset)%size][int(size/2)] = 1;
            weight = weight - nodeCreatedWeight/size
            if weight < 0:
                weight = 0
            numNodes = numNodes + 1
        else:
            map[(i + offset)%size][int(size/2)] = -1;
            weight = weight + nodeFailedWeight/size
            if weight > 1:
                weight = 1
        i = i + 1

    if numNodes < 2:
        GenerateBaseMap(size, map)
    return;

#Generate Json File
def GenerateJsonFile(size, map):
    jsonData = {}
    nodes = []

    #Generate P0 Base Node
    first_node = {}
    first_node_connections = []
    
    if map[int(size/2) - 1][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(size/2) - 1) + 2)
        tmp_conn1["Distance"] = nodeDistance
        first_node_connections.append(tmp_conn1)
    if map[int(size/2)][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(size/2)) + 2)
        tmp_conn1["Distance"] = nodeDistance
        first_node_connections.append(tmp_conn1)
    if size%2 != 0 and map[int(size/2) + 1][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(size/2) + 1) + 2)
        tmp_conn1["Distance"] = nodeDistance
        first_node_connections.append(tmp_conn1)

    first_node["Connections"] = first_node_connections
    first_node["ID"] = 1
    first_node["Radius"] = 1

    resource1 = []
    first_node["Resource"] = resource1

    first_node["StructureDefense"] = 1
    first_node["TeamStart"] = 0
    first_node["ControlPoints"] = 500

    nodes.append(first_node)
    
    #Generate P1 Base Node
    last_node = {}
    last_node_connections = []
    
    if map[int(size/2) - 1][size-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((size-1) * size) + (int(size/2) - 1) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)
    if map[int(size/2)][size-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((size-1) * size) + (int(size/2)) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)
    if size%2 != 0 and map[int(size/2) + 1][size-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((size-1) * size) + (int(size/2) + 1) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)

    last_node["Connections"] = last_node_connections
    last_node["ID"] = size*size + 2
    last_node["Radius"] = 1

    resource1 = []
    last_node["Resource"] = resource1

    last_node["StructureDefense"] = 1
    last_node["TeamStart"] = 1
    last_node["ControlPoints"] = 500

    #Generate Json for all center nodes
    j = 0
    while j < size:
        i = 0
        while i < size:
            if map[i][j] > 0:
                tmp_node = {}
                connections = []
                connected_to_base = 0

                curNodeId = ((j) * size) + i + 2

                #Add Connection to P0 Base
                for firstNodeConnection in first_node_connections:
                    if firstNodeConnection["ConnectedID"] == curNodeId:
                        tmp_conn = {}
                        tmp_conn["ConnectedID"] = 1
                        tmp_conn["Distance"] = nodeDistance
                        connections.append(tmp_conn)
                        connected_to_base = 1

                #Add Connections
                k = 0
                while k < 8:
                    if j + directionX[k] >= 0 and j + directionX[k] < size and i + directionY[k] >= 0 and i + directionY[k] < size and map[i + directionY[k]][j + directionX[k]] > 0:
                        conNodeId = ((j + directionX[k]) * size) + i + directionY[k] + 2
                        
                        tmp_conn = {}
                        tmp_conn["ConnectedID"] = conNodeId
                        tmp_conn["Distance"] = nodeDistance
                        connections.append(tmp_conn)
                    k = k + 1

                #Add Connection to P1 Base
                for lastNodeConnection in last_node_connections:
                    if lastNodeConnection["ConnectedID"] == curNodeId:
                        tmp_conn = {}
                        tmp_conn["ConnectedID"] = size*size + 2
                        tmp_conn["Distance"] = nodeDistance
                        connections.append(tmp_conn)
                        connected_to_base = 1
                
                tmp_node["Connections"] = connections

                tmp_node["ID"] = curNodeId
                tmp_node["Radius"] = 1

                resource = []
                if map[i][j] == 2:
                    resource.append("DEFENSE")
                elif map[i][j] == 3:
                    resource.append("OBSERVE")
                
                tmp_node["Resource"] = resource

                if connected_to_base == 1:
                    tmp_node["StructureDefense"] = 1.5
                else:
                    tmp_node["StructureDefense"] = 1.25

                tmp_node["TeamStart"] = -1
                tmp_node["ControlPoints"] = 100
                    
                nodes.append(tmp_node)
            i = i + 1
        j = j + 1

    nodes.append(last_node)

    jsonData["__type"] = "Map:#Everglades_MapJSONDef"
    jsonData["MapName"] = "Random"
    jsonData["Xsize"] = size
    jsonData["Ysize"] = size
    jsonData["nodes"] = nodes

    with open(outputFile, 'w', encoding='utf-8') as f:
              json.dump(jsonData, f, ensure_ascii=False, indent=4)

#Main
def exec(size):
    map = [[0 for x in range(size)] for y in range(size)]
    
    GenerateBaseMap(size, map)
    GenerateJsonFile(size, map)
    
    print('--------------------Random Map---------------------')
        
    for x in map:
        print(*x, sep="\t")
    
    print('---------------------------------------------------')
