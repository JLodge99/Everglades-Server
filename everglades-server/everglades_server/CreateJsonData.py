from queue import Queue
import random
import json
import os.path

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

#Global Variables
outputLocation = "config"

outputFileLoadout = "Loadout"
outputFileLoadoutEnd = ".json"


outputFileAttributes = "Attributes.json"
outputFileUnitPresets = "UnitPresets.json"

defaultLoadoutFile = "LoadoutDefault"

outputFileMap = "RandomMap.json"





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
            foundDuplicate = False
            for k in range(len(tmp_squadUnits)):
                if(tmp_squadUnits[k]["Type"] == loadout[i][j]):
                    tmp_squadUnits[k]["Count"] = tmp_squadUnits[k]["Count"] + 1
                    foundDuplicate = True
                    break
            if not foundDuplicate:
                tmp_unit = {}
                tmp_unit["Type"] = loadout[i][j]
                tmp_unit["Count"] = 1
                tmp_squadUnits.append(tmp_unit)

        tmp_squad["Squad"] = tmp_squadUnits
        squads.append(tmp_squad)


    jsonData["__type"] = "Loadout:#Everglades_LoadoutJSONDef"
    jsonData["Squads"] = squads

    fileName = outputFileLoadout + str(playerIdentifier) + outputFileLoadoutEnd
    savePath = os.path.join(outputLocation, fileName)
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()

    #with open(outputFileLoadout + str(playerIdentifier) + outputFileLoadoutEnd, 'w', encoding='utf-8') as f:
    #          json.dump(jsonData, f, ensure_ascii=False, indent=4)


# Loadout -1 is reserved for default loadout


def __loadJsonFileLoadout(playerIdentifier):

    fileName = outputFileLoadout + str(playerIdentifier) + outputFileLoadoutEnd
    loadoutFile = os.path.join(outputLocation, fileName)
    dFile = os.path.join(outputLocation, loadoutFile)
    if (playerIdentifier < 0 or not os.path.exists(os.path.abspath(loadoutFile))):
        print("Loading failed")
        with open(os.path.abspath(defaultLoadoutFile)) as f:
            data = json.load(f)
    else:
        print("Loading found")
        with open(os.path.abspath(loadoutFile)) as f:
            data = json.load(f)

        
    f.close() #TODO check this line didnt break anything
    
    return data


def CheckIfValidSquad(squad):

    return True

# Takes in an array group
def CheckIfValidLoadout(loadout):

    droneCount = 0
    squadCount = 0
    for i in range(len(loadout)):
        squadCount = squadCount + 1

        if CheckIfValidSquad(loadout[i]) == False:
            return False

        for j in range(len(loadout[i])): # TODO: JEROLD: Make Duple thingy work here
                droneCount = droneCount + 1

    if squadCount != 12: #TODO: Pull value from settings file
        return False
    if droneCount != 100: #TODO: Pull value from settings file 
        return False

    return True

def __getLoadoutTypeArrayViaJSON(loadedData):
    loadout = []
    
    for i in range(len(loadedData["Squads"])):
        row = []
        for j in range(len(loadedData["Squads"][i]["Squad"])):
            row.append(loadedData["Squads"][i]["Squad"][j]["Type"])
        loadout.append(row) # TODO: JEROLD: Make Duple thingy

    return loadout

# Call this function to get the loadout to be used
def GetLoadout(playerIdentifier):
    loadedJSON = __loadJsonFileLoadout(playerIdentifier)
    if CheckIfValidLoadout(__getLoadoutTypeArrayViaJSON(loadedJSON)):
        return loadedJSON
    else:
        return __loadJsonFileLoadout(-1) #Gets the default loadout

#Call this function for an array of arrays storing the unit types
def GetLoadoutTypeArray(playerIdentifier): # TODO: JEROLD: Make Duple thingy work with whatever is calling this
    loadedData = GetLoadout(playerIdentifier)

    return __getLoadoutTypeArrayViaJSON(loadedData)







# -------------------------------------
#   Attribute Creation
# -------------------------------------
        
# Generates an Attribute for use with Unit Attributes
# Takes in name: Name to be displayed, effect: slug representing what needs modifying, modifier: value of change
#   isMult: Determines if the modifier, modPriority: integer representing ordering priority, cost: point cost for balancing
def GenerateUnitAttribute(name, effect, description, modifier, isMult, modPriority, cost):
    jsonData = {}


    jsonData["Name"] = name
    jsonData["Effect"] = effect
    jsonData["Description"] = description
    jsonData["Modifier"] = modifier    
    jsonData["isMult"] = isMult
    jsonData["ModifierPriority"] = modPriority    
    jsonData["Cost"] = cost

    return jsonData

def GenerateUnitAttributeFile(names, effects, descriptions, modifiers, isMults, modPriorities, costs):
    jsonData = {}
    abilities = []

    for i in range(len(names)):
        ability = GenerateUnitAttribute(names[i], effects[i], descriptions[i], modifiers[i], isMults[i], modPriorities[i], costs[i])

        abilities.append(ability)


    jsonData["__type"] = "Unit_Attributes"
    jsonData["Attributes"] = abilities

    fileName = outputFileAttributes
    savePath = os.path.join(outputLocation, fileName)
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()

# Loads in the attribute file as an array of arrays
def LoadUnitAttributeFile():

    information = []

    names = []
    effects = []
    descriptions = []
    modifiers = []
    isMults = []
    modPriorities = []
    costs = []

    fileName = outputFileAttributes
    attributeFile = os.path.join(outputLocation, fileName)
    if (os.path.exists(os.path.abspath(attributeFile))):
        
        with open(os.path.abspath(attributeFile)) as f:
            data = json.load(f)

            for info in range(len(data["Attributes"])):
                names.append(data["Attributes"]["Name"])
                effects.append(data["Attributes"]["Effect"])
                descriptions.append(data["Attributes"]["Description"])
                modifiers.append(data["Attributes"]["Modifier"])
                isMults.append(data["Attributes"]["isMult"])
                modPriorities.append(data["Attributes"]["ModifierPriority"])
                costs.append(data["Attributes"]["Cost"])

            f.close()
    

    information.append(names)
    information.append(effects)
    information.append(descriptions)
    information.append(modifiers)
    information.append(isMults)
    information.append(modPriorities)
    information.append(costs)

    return information


# -------------------------------------
#   Unit Creation
# -------------------------------------

def GenerateAttributeBasedUnit(name, attributeSlugs):
    jsonData = {}
    attributes = []

    jsonData["Name"] = name

    for i in range(len(attributeSlugs)):
        attributes.append(attributeSlugs[i])

    jsonData["Attributes"] = attributes


    return jsonData

def GenerateAttributeBasedUnitsFile(names, attributeSlugsList):
    jsonData = {}
    unitInformation = []

    for i in range(len(names)):
        unitInfo = GenerateAttributeBasedUnit(names[i], attributeSlugsList[i])

        unitInformation.append(unitInfo)


    jsonData["__type"] = "Units_in_Attribute_Format"
    jsonData["Units"] = unitInformation

    fileName = outputFileUnitPresets
    savePath = os.path.join(outputLocation, fileName)
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()

# Loads in the unit based attribute file as a structure of arrays. [name=0,attributeList=1][nameIndex or attributeListIndex][notUsedForName, attributeIndex]
def LoadAttributesBasedUnitFile(preset):

    information = []

    names = []
    attributeLists = []

    fileName = outputFileUnitPresets
    attributeFile = os.path.join(outputLocation, fileName)
    if (os.path.exists(os.path.abspath(attributeFile))):
        
        with open(os.path.abspath(attributeFile)) as f:
            data = json.load(f)

            for i in range(len(data["Units"])):
                names.append(data["Units"][i]["Name"])
                attributeSlugs = []
                for j in range(len(data["Units"][i]["Attributes"])):
                    attributeSlugs.append(data["Units"][i]["Attributes"])
                attributeLists.append(attributeSlugs)

            f.close()
    

    information.append(names)
    information.append(attributeLists)


    return information

'''
def GenerateSingleUnit(name, Attributes):
    jsonData = {}

    health = 1
    damage = 1
    speed = 1
    control = 1
    cost = 0

    maxPriority = 0

    Attributes.sort(key=lambda x: x., reverse=False)

    for attribute in range(len(Attributes)):
        

    jsonData["Name"] = name
    jsonData["Health"] = health
    jsonData["Damage"] = damage
    jsonData["Speed"] = speed    
    jsonData["Control"] = control   
    jsonData["Cost"] = cost

    return jsonData

def GenerateUnitAttributeFile(names, effects, descriptions, modifiers, isMults, modPriorities, costs):
    jsonData = {}
    abilities = []

    for i in range(len(names)):
        ability = GenerateUnitAttribute(names[i], effects[i], descriptions[i], modifiers[i], isMults[i], modPriorities[i], costs[i])

        abilities.append(ability)


    jsonData["__type"] = "Units"
    jsonData["Attributes"] = abilities

    fileName = outputFileAttributes
    savePath = os.path.join(outputLocation, fileName)
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()

# TODO, actually load
# Loads in the attribute file as an array of arrays
def LoadUnitAttributeFile():

    information = []

    names = []
    effects = []
    descriptions = []
    modifiers = []
    isMults = []
    modPriorities = []
    costs = []

    fileName = outputFileAttributes
    attributeFile = os.path.join(outputLocation, fileName)
    if (os.path.exists(os.path.abspath(attributeFile))):
        with open(os.path.abspath(attributeFile)) as f:
            data = json.load(f)

            for info in range(len(data["Attributes"])):
                names.append(data["Attributes"]["Name"])
                effects.append(data["Attributes"]["Effect"])
                descriptions.append(data["Attributes"]["Description"])
                modifiers.append(data["Attributes"]["Modifier"])
                isMults.append(data["Attributes"]["isMult"])
                modPriorities.append(data["Attributes"]["ModifierPriority"])
                costs.append(data["Attributes"]["Cost"])

            f.close()
    

    information.append(names)
    information.append(effects)
    information.append(descriptions)
    information.append(modifiers)
    information.append(isMults)
    information.append(modPriorities)
    information.append(costs)

    return information
'''