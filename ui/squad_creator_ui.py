# Zachary Neidig (zackneidig@gmail.com)
# 3/16/21
# UI to more easily create and edit squads
# Not perfect, there are inefficiencies (ex: updating the whole listbox when only individual entries change, sorting random squads)
# Also once I got a weird bug involving changing squad and the numbers of units in them??? Can't reproduce, maybe it fixed itself
import sys
import tkinter as tk
from everglades_server.CreateJsonData import *

thismodule = sys.modules[__name__]

numSquads = 12      #The number of squads in the loadout
selectIndex = -1    #The index of the selected unit in its loadout, if -1 then none is selected. Used for loading/saving the amount of that unit

#Each of the below are in the form: squadUnits[Index of loadout (which equals loadout number - 1)][Index of unit in loadout (whic equals position in loadout - 1)]
squadUnits = []     #The names of each type of unit in a squad
squadNums = []      #The amount of each type of unit in a squad

#The below variables are the copied squad. They are in the same format as a squad from the loadout
tempSquadUnits = [] #The names of each type of unit in the copied squad
tempSquadNums = []  #The amount of each type of unit in the copied squad

#Initializing the squad-describing variables
for x in range(0, numSquads):
    squadUnits.append([])
    squadNums.append([])


def refreshDropDown():
    ### PURPOSE: When the number of loadouts changes, this function is called
    ### to update the squad selection dropdown menu to be correct

    ## Remove current dropdown options
    sel_squad_dd['menu'].delete(0, 'end')

    ## Add new options
    for x in range (1, numSquads+1):
        sel_squad_dd['menu'].add_command(label=str(x), command=tk._setit(selSquadDdText, str(x)))

    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def updateUnitList():
    ### PURPOSE: When the names or amounts of units in the selected squad changes, this function is called
    ### to update the listbox to be correct

    ## Get index of current squad
    squadIndex = int(selSquadDdText.get())-1

    ## Clear listbox of units
    curr_squad.delete(0, tk.END)

    ## Repopulate with up-to-date units and counts
    if len(squadUnits[squadIndex]) > 0: #If there are units to populate the list with
        for x in range(0,len(squadUnits[squadIndex])):  #For every unit in the current squad
            curr_squad.insert(tk.END, str(squadUnits[squadIndex][x]) + " ("+str(squadNums[squadIndex][x])+")") #Add their name and number to the listbox

def addSquad():
    ### PURPOSE: When a squad is added, this function is called
    ### to append empty arrays to the loadout-describing arrays and jump the UI to it

    global numSquads
    global squadUnits
    global squadNums

    ## Append empty squad
    numSquads+=1
    squadUnits.append([])
    squadNums.append([])

    ## Jump to new squad
    selSquadDdText.set(str(numSquads))

    ## Update dropdown & listbox
    refreshDropDown()
    updateUnitList()

def deleteSquad():
    ### PURPOSE: When a squad is deleted, this function is called
    ### to pop those indeces and jump to the nearest squad and load it

    global numSquads
    global squadUnits
    global squadNums

    # If there's only one squad left, end
    # Handling logic with no squads is weird and also there will always be a squad so this makes sense
    if numSquads == 1:
        return
    
    ## Get current index
    squadIndex = int(selSquadDdText.get())-1

    ## Pop index & update counter
    squadUnits.pop(squadIndex)
    squadNums.pop(squadIndex)
    numSquads-=1

    ## Jump down an index if necessary
    if int(selSquadDdText.get()) > numSquads:
       selSquadDdText.set(numSquads)
    
    ## Update dropdown and listbox
    refreshDropDown()
    updateUnitList()

def copySquad():
    ### PURPOSE: When a squad is copied, this function is called
    ### to store the current squad

    global squadUnits
    global squadNums
    global tempSquadUnits
    global tempSquadNums
    
    ## Get current squad index
    squadIndex = int(selSquadDdText.get())-1

    ## Store current state
    tempSquadUnits = squadUnits[squadIndex]
    tempSquadNums = squadNums[squadIndex]

def pasteSquad():
    ### PURPOSE: When a squad is pasted, this function is called
    ### to overwrite the current squad with the pasted squad

    global squadUnits
    global squadNums
    global tempSquadUnits
    global tempSquadNums
    
    ## Get current squad index
    squadIndex = int(selSquadDdText.get())-1

    ## Replace current squad with stored squad
    squadUnits[squadIndex] = tempSquadUnits
    squadNums[squadIndex] = tempSquadNums

    ## Update list of units in current squad
    updateUnitList()
    
    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def deleteUnit():
    ### PURPOSE: When a unit is deleted, this function is called
    ### to handle the UI and backend of popping that unit's index

    global squadUnits
    global squadNums
    global selectIndex
    
    if selectIndex > -1:    #If a unit is selected
        #Get the current squad
        squadIndex = int(selSquadDdText.get())-1 

        #Pop the units at the selected index
        squadUnits[squadIndex].pop(selectIndex)
        squadNums[squadIndex].pop(selectIndex)
    
    ## Update list of units in current squad
    updateUnitList()

    ## Remove unit selection
    selectIndex = -1

def addUnit():
    ### PURPOSE: When a unit is added, this function is called
    ### to handle the UI and backend of appending that unit

    global squadUnits
    global squadNums

    # Get index of squad to add to
    squadIndex = int(selSquadDdText.get())-1

    # Add 1 of unit
    squadUnits[squadIndex].append(nameVar.get())
    squadNums[squadIndex].append(1)

    # Update ListBox
    updateUnitList()

    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def updateSelNum(*args):
    ### PURPOSE: When an item in the listbox is selected, this function is called
    ### to set the number entry form to the number amount of that unit in that squad

    global selectIndex
    if curr_squad.curselection() != ():
        squadIndex = int(selSquadDdText.get())-1
        selectIndex = curr_squad.curselection()[0]
        numVar.set(squadNums[squadIndex][selectIndex])
    else:
        if selectIndex < 0:
            numVar.set("")

def checkNumInput(S):
    ### PURPOSE: When the user types in the "number" text entry form, this function is called
    ### to make sure that they are typing a number

    if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '']:
        return True
    
    window.bell() # .bell() plays that ding sound telling you there was invalid input
    return False

def updateNum():
    ### PURPOSE: When the amount of a unit type changes, this function is called
    ### to update the unit listbox to the correct number

    global selectIndex
    squadIndex = int(selSquadDdText.get())-1
    squadNums[squadIndex][selectIndex] = numVar.get()
    updateUnitList()

def generateJSON():
    ### PURPOSE: When the "generate JSON" button is pressed, this function is called
    ### to write the loadout currently defined in this program to the appropriate JSON

    global squadUnits
    global squadNums
    global numSquads
    loadout = []
    
    ## The code snippet below translates the loadout from the format defined at the top of this program
    ## to the format used by the JSON-writing function it calls
    ## ex:      squadNums[0]: [3, 2]  &  squadUnits[0]: ["Striker", "Tank"]
    ## becomes: loadout[0]: ["Striker", "Striker", "Striker", "Tank", "Tank"]

    for squadNumber in range(0,numSquads):  # For each squad (squadNumber = int index of current squad)
        loadout.append([])                  # Create an array in the loadout
        unitslength = len(squadUnits[squadNumber])  # unitslength = int number of units in the current squad
        for unitInList in range(0,unitslength):     # for each unit in the current squad
            for unitNumber in range(0, int(squadNums[squadNumber][unitInList])):    # for the amount of this unit type
                loadout[squadNumber].append(squadUnits[squadNumber][unitInList])    # add that unit to the loadout
    
    # Grab player number from the dropdown
    playerIdentifier = int(playnumselSquadDdText.get())

    # Call the function to write the current loadout to the appropriate JSON
    GenerateJsonFileLoadout(loadout, playerIdentifier)

def generateRandom():
    ### PURPOSE: When the "generate random squad" button is pressed, this function is called
    ### to call the random squad function (automatically writes to json) and load loadout into UI

    presetNumber = int(presetselSquadDdText.get())
    loadout = GenerateRandomLoadout(presetNumber)

    # Sort the random squad
    # The current (3/16/21) squad generation function creates multiple groups of count 1 of each unit type
    # It is easiest to join these groups by sorting them first
    for squad in loadout:
        squad.sort()

    global squadUnits
    tempsquadUnits = []
    global squadNums
    tempsquadNums = []
    global numSquads

    numSquads = len(loadout)
    prevUnitName = ""       # Stores the previous name read from the random squad generation
    counter = 0             # Counts the number of each type of unit before a new name or the end of the squad appears

    ## After sorting the random loadout, it will be in the form used by the JSON-writing function
    ## The code snippet below translates the loadout from the format used by the JSON-writing function
    ## to the format defined at the top of this program so it is usable in the UI
    ## ex:      loadout[0]: ["Striker", "Striker", "Striker", "Tank", "Tank"]
    ## becomes: squadNums[0]: [3, 2]  &  squadUnits[0]: ["Striker", "Tank"]
    ## The code is a bit of a mess but it works as efficiently as possible

    # For each squad (squad = int index of current squad)
    for squad in range(0,numSquads):    

        # Create an array representing that squad
        tempsquadNums.append([])
        tempsquadUnits.append([])

        for unit in loadout[squad]:     # For each unit in the current squad

            # If this is a new unit, add the count of the previous unit, add new name to the list of unit types, and begin counting from 1
            if unit != prevUnitName:   
                # If this is NOT the first unit, append the count of the previous unit     
                if counter > 0:
                    tempsquadNums[squad].append(counter)

                # Add this unit's name to the list
                tempsquadUnits[squad].append(unit)

                # Begin counting new unit's amount
                counter = 1            

                # Set the previous unit name so we know what the last documented unit type is
                prevUnitName = unit

            # If this is the same unit type, increment its counters
            if unit == prevUnitName:
                counter+=1
        
        # Add the count of the last unit
        tempsquadNums[squad].append(counter)

    squadUnits = tempsquadUnits
    squadNums = tempsquadNums

    # Update UI to accomodate
    updateUnitList()
    refreshDropDown()

## Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Squad Creator UI")
window.resizable(width=True, height=True)

## Left-most column
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Create dropdown menu
sel_squad_frame = tk.Frame(master=left_frame)
sel_squad_frame.grid(row=0, column=0)

selSquadDdText = tk.StringVar()
selSquadDdText.set("1")

def dd_callback(*args):
    updateUnitList()
selSquadDdText.trace("w", dd_callback)

sel_squad_lbl = tk.Label(master=sel_squad_frame, text="Select Squad: ")
sel_squad_lbl.grid(row=0, column=0, sticky="w")
sel_squad_dd = tk.OptionMenu(sel_squad_frame, selSquadDdText, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
sel_squad_dd.grid(row=0, column=1, sticky="e")

# Add Squad Button
btn_add = tk.Button(
    master=left_frame,
    text="Add Empty Squad",
    command = addSquad
)
btn_add.grid(row=1, column=0, pady = 10)

# Delete Squad Button
btn_delete = tk.Button(
    master=left_frame,
    text="Delete Current Squad",
    command = deleteSquad
)
btn_delete.grid(row=2, column=0, pady = 10)

# Copy Squad Button
btn_copy = tk.Button(
    master=left_frame,
    text="Copy Current Squad",
    command = copySquad
)
btn_copy.grid(row=3, column=0, pady = 10)

# Paste Squad Button
btn_paste = tk.Button(
    master=left_frame,
    text="Paste Copied Squad",
    command = pasteSquad
)
btn_paste.grid(row=4, column=0, pady = 10)


## Middle column
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=1, padx=10, pady=10)

curr_lbl = tk.Label(master=mid_frame, text="Units in Selected Squad: ")
curr_lbl.grid(row=0, column=0, sticky="w")

curr_squad = tk.Listbox(master=mid_frame)
curr_squad.grid(row=1, column=0, sticky="w")
curr_squad.bind('<<ListboxSelect>>', updateSelNum)

# Delete Squad Button
btn_delete = tk.Button(
    master=mid_frame,
    text="Remove Selected Unit",
    command = deleteUnit
)
btn_delete.grid(row=2, column=0, pady = 10, sticky="w")


## Right column
right_frame = tk.Frame(master=window)
right_frame.grid(row=0, column=2, padx=10, pady=10)

topright_frame = tk.Frame(master=right_frame)
topright_frame.grid(row=0, column=0)

num_unit_lbl = tk.Label(master=topright_frame, text="Number of Selected Unit: ")
num_unit_lbl.grid(row=0, column=0, sticky="w")

numVar = tk.StringVar()
def num_callback(*args):
    updateNum()
numVar.trace("w", num_callback)
vcmd = (topright_frame.register(checkNumInput), '%S')

ent_unitnum = tk.Entry(master=topright_frame, width=5, textvariable = numVar, validate='key', vcmd=vcmd)
ent_unitnum.grid(row=0, column=1, sticky="e")

nameVar = tk.StringVar()
unitname_lbl = tk.Label(master=right_frame, text="Add Unit with Name: ")
unitname_lbl.grid(row=2, column=0, pady=(15,0))
ent_unitname = tk.Entry(master=right_frame, width=25, textvariable = nameVar)
ent_unitname.grid(row=3, column=0)

    

btn_new = tk.Button(
    master=right_frame,
    text="Add Unit to Squad",
    command = addUnit
)
btn_new.grid(row=4, column=0, pady=10)

## Frame and widgets for JSON generation
json_frame = tk.Frame(master=right_frame)
json_frame.grid(row=5, column=0, pady=(15,0))

playnum_lbl = tk.Label(master=json_frame, text="Player Number: ")
playnum_lbl.grid(row=0, column=0, sticky="w")

playnumselSquadDdText = tk.StringVar()
playnumselSquadDdText.set("0")
playnum_dd = tk.OptionMenu(json_frame, playnumselSquadDdText, "0", "1")
playnum_dd.grid(row=0, column=1, sticky="e")

btn_gen = tk.Button(
    master=json_frame,
    text="Generate JSON",
    command = generateJSON
)
btn_gen.grid(row=0, column=2, sticky="e")

## Frame and widgets for random squad generation
random_squad_frame = tk.Frame(master=right_frame)
random_squad_frame.grid(row=6, column=0, pady=(15,0))

playnum_lbl2 = tk.Label(master=random_squad_frame, text="Preset Number: ")
playnum_lbl2.grid(row=0, column=0, sticky="w")

presetselSquadDdText = tk.StringVar()
presetselSquadDdText.set("0")
preset_dd = tk.OptionMenu(random_squad_frame, presetselSquadDdText, "0", "1", "2")
preset_dd.grid(row=0, column=1, sticky="e")

btn_gen_random = tk.Button(
    master=random_squad_frame,
    text="Create Random Squad",
    command = generateRandom
)
btn_gen_random.grid(row=0, column=2, sticky="e")

# Run the application
window.mainloop()
