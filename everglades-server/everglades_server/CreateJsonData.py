from queue import Queue
import random
import json
import os.path

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

#Global Variables
outputFileLoadout = "/Everglades/config/Loadout"
outputFileLoadoutEnd = ".json"

defaultLoadoutFile = "/Everglades/config/LoadoutDefault"
outputFileMap = "/Everglades/config/RandomMap.json"



#Generate Json File
def GenerateJsonFileMap(sizeX, sizeY, sizeZ, map):
    jsonData = {}
    nodes = []

    sizeW = sizeX #Size to be used for generating Base Node

    #Generate P0 Base Node
    first_node = {}
    first_node_connections = []
    
    if map[int(sizeW/2) - 1][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(sizeW/2) - 1) + 2)
        tmp_conn1["Distance"] = nodeDistance
        first_node_connections.append(tmp_conn1)
    if map[int(sizeW/2)][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(sizeW/2)) + 2)
        tmp_conn1["Distance"] = nodeDistance
        first_node_connections.append(tmp_conn1)
    if size%2 != 0 and map[int(sizeW/2) + 1][0] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((int(sizeW/2) + 1) + 2)
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
    
    if map[int(sizeW/2) - 1][sizeW-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((sizeW-1) * sizeW) + (int(sizeW/2) - 1) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)
    if map[int(sizeW/2)][sizeW-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((sizeW-1) * sizeW) + (int(sizeW/2)) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)
    if sizeW%2 != 0 and map[int(sizeW/2) + 1][sizeW-1] > 0:
        tmp_conn1 = {}
        tmp_conn1["ConnectedID"] = ((sizeW-1) * sizeW) + (int(sizeW/2) + 1) + 2
        tmp_conn1["Distance"] = nodeDistance
        last_node_connections.append(tmp_conn1)

    last_node["Connections"] = last_node_connections
    last_node["ID"] = sizeX*sizeY*sizeZ + 2
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
    jsonData["Xsize"] = sizeX
    jsonData["Ysize"] = sizeY
    jsonData["Zsize"] = sizeZ
    jsonData["nodes"] = nodes

    with open(outputFileMap, 'w', encoding='utf-8') as f:
              json.dump(jsonData, f, ensure_ascii=False, indent=4)

#Generate Json File for loadouts
# Takes in an array of array of strings
# loadout, array of squads. Each squad is an array that contains the name of the types of unit.
# player identifier, 0 or 1

def GenerateJsonFileLoadout(loadout, playerIdentifier):
    jsonData = {}
    squads = []

    for i in range(len(loadout)):
        tmp_squad = {}
        tmp_squadUnits = []
        for j in range(len(loadout[i])):
            tmp_unit = {}
            tmp_unit["Type"] = loadout[i][j]
            tmp_squadUnits.append(tmp_unit)
        tmp_squad["Squad"] = tmp_squadUnits
        squads.append(tmp_squad)


    jsonData["__type"] = "Loadout:#Everglades_LoadoutJSONDef"
    jsonData["Squads"] = squads

    with open(outputFileLoadout + playerIdentifier + outputFileLoadoutEnd, 'w', encoding='utf-8') as f:
              json.dump(jsonData, f, ensure_ascii=False, indent=4)


#Call this function for an array of arrays storing the unit types
def GetLoadoutTypeArray(playerIdentifier):
    loadout = []
    loadedData = GetLoadout(playerIdentifier)
    for i in range(len(loadedData["Squads"])):
        tmp_squad = {}
        tmp_squadUnits = []
        for j in range(len(loadedData["Squads"][i]["Squad"])):
            loadout[i][j] = tmp_unit["Type"]

    return loadout

# Call this function to get the loadout to be used
def GetLoadout(playerIdentifier):
    loadedJSON = __loadJsonFileLoadout(playerIdentifier)
    if CheckIfValidLoadout(loadedJSON):
        return loadedJSON
    else:
        return __loadJsonFileLoadout(-1) #Gets the default loadout

# Loadout -1 is reserved for default loadout
def __loadJsonFileLoadout(playerIdentifier):

    loadoutFile = outputFileLoadout + playerIdentifier + outputFileLoadoutEnd;
    if (playerIdentifier < 0 or not os.path.exists(loadoutFile)):
        with open(defaultLoadoutFile) as f:
            data = json.load(f)
    else:
        with open(loadoutFile) as f:
            data = json.load(f)

        
        
    
    return data

def CheckIfValidLoadout(loadout):

    droneCount = 0
    squadCount = 0
    for i in range(len(loadout)):
        squadCount = squadCount + 1

        if CheckIfValidSquad(loadout[i]) == false:
            return false

        for j in range(len(loadout[i])):
                droneCount = droneCount + 1

    if squadCount != 12: #TODO: Pull value from settings file
        return false
    if droneCount != 100: #TODO: Pull value from settings file
        return false

    return true

def CheckIfValidSquad(squad):

    return true
