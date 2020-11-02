from queue import Queue
import random
import json
import os.path

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

#Global Variables
outputFileLoadout = "config/Loadout"
outputFileLoadoutEnd = ".json"

defaultLoadoutFile = "config/LoadoutDefault"

outputFileMap = "config/RandomMap.json"

def GetFilePathToMain():
    print("Here is what I found: " + os.path.curdir)
    return os.path.dirname(os.path.dirname(os.path.curdir))



#Generate Json File for loadouts
# Takes in an array of array of strings
# loadout, array of squads. Each squad is an array that contains the name of the types of unit.
# player identifier, 0 or 1

def GenerateJsonFileLoadout(loadout, playerIdentifier):
    jsonData = {}
    squads = []

    print("Ran GenFile")
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

    savePath = outputFileLoadout + str(playerIdentifier) + outputFileLoadoutEnd
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()

    #with open(outputFileLoadout + str(playerIdentifier) + outputFileLoadoutEnd, 'w', encoding='utf-8') as f:
    #          json.dump(jsonData, f, ensure_ascii=False, indent=4)


#Call this function for an array of arrays storing the unit types
def GetLoadoutTypeArray(playerIdentifier):
    loadout = []
    loadedData = GetLoadout(playerIdentifier)
    for i in range(len(loadedData["Squads"])):
        tmp_squad = {}
        tmp_squadUnits = []
        for j in range(len(loadedData["Squads"][i]["Squad"])):
            loadout[i][j] = loadedData["Squads"][i]["Squad"]["Type"]

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

    loadoutFile = outputFileLoadout + playerIdentifier + outputFileLoadoutEnd
    if (playerIdentifier < 0 or not os.path.exists(os.path.abspath(loadoutFile))):
        with open(os.path.abspath(defaultLoadoutFile)) as f:
            data = json.load(f)
    else:
        with open(os.path.abspath(loadoutFile)) as f:
            data = json.load(f)

        
        
    
    return data

def CheckIfValidLoadout(loadout):

    droneCount = 0
    squadCount = 0
    for i in range(len(loadout)):
        squadCount = squadCount + 1

        if CheckIfValidSquad(loadout[i]) == False:
            return False

        for j in range(len(loadout[i])):
                droneCount = droneCount + 1

    if squadCount != 12: #TODO: Pull value from settings file
        return False
    if droneCount != 100: #TODO: Pull value from settings file
        return False

    return True

def CheckIfValidSquad(squad):

    return True
