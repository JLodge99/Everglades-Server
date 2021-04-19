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
outputFileUnitDefaults = "UnitDefaults.json"
outputFileUnitPresets = "UnitPresets.json"
outputFileUnitCustoms = "UnitCustoms.json"

outputFileUnitDefinitions = "UnitDefinitions.json"

defaultLoadoutFile = "LoadoutDefault.json"

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
        print("Default Loadout used for agent ", playerIdentifier)
        with open(os.path.abspath(os.path.join(outputLocation, defaultLoadoutFile))) as f:
            data = json.load(f)
    else:
        #print("Loading found")
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
            print("Invalid Loadout: Squad invalid")
            return False

        for j in range(len(loadout[i])):
                droneCount += loadout[i][j][1]

    if squadCount != 12: #TODO: Pull value from settings file
        print("Invalid Loadout: Squad Size Invalid")
        return False
    if droneCount != 100: #TODO: Pull value from settings file 
        print("Invalid Loadout: Drone Count Invalid")
        return False

    return True

def __getLoadoutTypeArrayViaJSON(loadedData):
    loadout = []
    
    for i in range(len(loadedData["Squads"])):
        row = []
        for j in range(len(loadedData["Squads"][i]["Squad"])):
            unit = (loadedData["Squads"][i]["Squad"][j]["Type"], loadedData["Squads"][i]["Squad"][j]["Count"])
            row.append(unit)
        loadout.append(row)

    return loadout

# Call this function to get the loadout to be used
def GetLoadout(playerIdentifier):
    loadedJSON = __loadJsonFileLoadout(playerIdentifier)
    if CheckIfValidLoadout(__getLoadoutTypeArrayViaJSON(loadedJSON)):
        return loadedJSON
    else:
        print("Loadout not accepted for agent ", playerIdentifier)
        return __loadJsonFileLoadout(-1) #Gets the default loadout

#Call this function for an array of arrays storing the unit types
def GetLoadoutTypeArray(playerIdentifier):
    loadedData = GetLoadout(playerIdentifier)

    return __getLoadoutTypeArrayViaJSON(loadedData)


# Converts JSON with array of strings into an object
def ConvertLoadoutToObject(playerIdentifier):
    unit_configs = {}
    loadout = GetLoadoutTypeArray(playerIdentifier)

    for i in range(len(loadout)):
        group_units = loadout[i]       ## Get each group
        unit_configs[i] = [(x) for x in set(group_units)]  ## Returns [('drone type', count),...]

    return unit_configs

def __getRandomUnit(preset):
    unitInfo = LoadAttributesBasedUnitFile(preset)


    return random.choice(unitInfo[0])

    
# Creates a random loadout
def GenerateRandomLoadout(preset):

    loadout = []
    numSquads = 12 #TODO: Read this in from file
    numDrones = 100 #TODO: Read this in from file

    dronePerSquad = numDrones / numSquads
    dronesOfLastSquad = (numDrones / numSquads) + (numDrones % numSquads)


    for squadNumber in range(0,int(numSquads - 1)):
        dronesToAdd = dronePerSquad
        loadout.append([])
        unitslength = dronePerSquad
        for unitInList in range(0,int(unitslength)):
            unit = __getRandomUnit(preset)
            loadout[squadNumber].append(unit)
                


    #Handle the last squad
    unitslength = dronesOfLastSquad
    loadout.append([])
    for unitInList in range(0,int(unitslength)):
        unit = __getRandomUnit(preset)
        loadout[numSquads-1].append(unit)

    return loadout



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

            for i in range(len(data["Attributes"])):
                names.append(data["Attributes"][i]["Name"])
                effects.append(data["Attributes"][i]["Effect"])
                descriptions.append(data["Attributes"][i]["Description"])
                modifiers.append(data["Attributes"][i]["Modifier"])
                isMults.append(data["Attributes"][i]["isMult"])
                modPriorities.append(data["Attributes"][i]["ModifierPriority"])
                costs.append(data["Attributes"][i]["Cost"])

            f.close()
    

    information.append(names)           #0
    information.append(effects)         #1
    information.append(descriptions)    #2
    information.append(modifiers)       #3
    information.append(isMults)         #4
    information.append(modPriorities)   #5
    information.append(costs)           #6

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

    #TODO: Ethan, come back to this
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
    if(preset == 0):
        fileName = outputFileUnitDefaults
    elif(preset == 1):
        fileName = outputFileUnitPresets
    else:
        fileName = outputFileUnitCustoms

    attributeFile = os.path.join(outputLocation, fileName)
    if (os.path.exists(os.path.abspath(attributeFile))):
        
        with open(os.path.abspath(attributeFile)) as f:
            data = json.load(f)

            for i in range(len(data["Units"])):
                names.append(data["Units"][i]["Name"])
                attributeSlugs = []
                for j in range(len(data["Units"][i]["Attributes"])):
                    attributeSlugs.append(data["Units"][i]["Attributes"][j])
                attributeLists.append(attributeSlugs)

            f.close()
    

    information.append(names)
    information.append(attributeLists)


    return information

# -------------------------------------
#   Unit Conversion
# -------------------------------------

def sortAttributeListbyPriority(attributeList):

    #TODO: Sort list. Sort by adjusted priority, lowest to highest integer value
    # Adjusted Priority Equation: Origional Priority * 2, if isMult then -1 from result
    return attributeList

def GenerateUnitDefinition(name, attributeList):
    jsonData = {}
    attributes = []

    jsonData["Name"] = name

    #Initialize Fields
    jsonData["Health"] = 1
    jsonData["Damage"] = 1
    jsonData["Speed"] = 1
    jsonData["SpeedBonus_Controlled_Ally"] = 0
    jsonData["SpeedBonus_Controlled_Enemy"] = 0
    jsonData["Jamming"] = 0
    jsonData["Commander_Damage"] = 0
    jsonData["Commander_Speed"] = 0
    jsonData["Commander_Control"] = 0
    jsonData["Self_Repair"] = 0
    jsonData["Control"] = 1
    jsonData["Recon"] = 0
    jsonData["Cost"] = 0





    sortedAttributeList = sortAttributeListbyPriority(attributeList)
    attributeFile = LoadUnitAttributeFile()
    
    costOfUnit = 0
    for i in range(len(sortedAttributeList)):
        attributeName = sortedAttributeList[i]
        foundSuccess = False
        index = -1

        # Determine which index in the attribute file corresponds for each attribute the unit has 
        for j in range(len(attributeFile[0])):
            if(attributeFile[0][j] == attributeName):
                foundSuccess = True
                index = j
                break
        if(foundSuccess == False):
            #TODO: Error handling
            placeholder = 1 #Delete this
        
        # Apply the modifier
        # TODO: Support same priority modifier addition. IE, multiplier of .2 and .3 on same priority would be combined to be .5
        if(attributeFile[4][index] == 1):
            jsonData[attributeFile[1][index]] = jsonData[attributeFile[1][index]] * attributeFile[3][index]
        else:
            jsonData[attributeFile[1][index]] = jsonData[attributeFile[1][index]] + attributeFile[3][index]

        costOfUnit += attributeFile[6][index]

    # Set cost in line with 1 being normal cost. Attribute selection is out of 6 for balance, therefore cost/6 gives actual cost
    jsonData["Cost"] = costOfUnit / 6

    return jsonData

# GameType determines the units used, 0 = only defaults, 1 = defaults and presets, 2 = all units including customs
def GenerateUnitDefinitions(gameType):
    jsonData = {}
    unitInformation = []

    unitNames = []
    unitAttributes = []
    for i in range(max(min(3,gameType + 1),1)):
        dataToConvert = LoadAttributesBasedUnitFile(i)
        unitNames = unitNames + dataToConvert[0]
        unitAttributes = unitAttributes + dataToConvert[1]

    for i in range(len(unitNames)):
        unitInformation.append(GenerateUnitDefinition(unitNames[i], unitAttributes[i]))
    

    jsonData["__type"] = "Units"
    jsonData["units"] = unitInformation

    fileName = outputFileUnitDefinitions
    savePath = os.path.join(outputLocation, fileName)
    FileO = open(os.path.abspath('{}'.format(savePath)), "w")
    FileO.write(json.dumps(jsonData, indent=4))
    FileO.close()




def TestingFunction():
    GenerateUnitDefinitions(0)
    GenerateJsonFileLoadout(GenerateRandomLoadout(0), 3)
TestingFunction()
