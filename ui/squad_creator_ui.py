# Zachary Neidig (zackneidig@gmail.com)
# 3/16/21
# This program is a UI used to more easily create and edit squads
# Not perfect, there are inefficiencies (ex: updating the whole listbox when only individual entries change, sorting random squads)

import sys
import tkinter as tk
from everglades_server.CreateJsonData import *
from everglades_server.ui_dependencies import *

thismodule = sys.modules[__name__]

numSquads = 12      #The number of squads in the loadout
selectIndex = -1    #The index of the selected unit in its loadout, if -1 then none is selected. Used for loading/saving the amount of that unit

#Each of the below are in the form: squadUnits[Index of loadout (which equals loadout number - 1)][Index of unit in loadout (whic equals position in loadout - 1)]
squadUnits = []     #The names of each type of unit in a squad
squadNums = []      #The amount of each type of unit in a squad

#The below variables are the copied squad. They are in the same format as a squad from the loadout
copiedSquadUnits = [] #The names of each type of unit in the copied squad
copiedSquadNums = []  #The amount of each type of unit in the copied squad

printStatementsThatEthanNeedsApparently = False

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
    unselectUnit()

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
    global copiedSquadUnits
    global copiedSquadNums
    
    ## Get current squad index
    squadIndex = int(selSquadDdText.get())-1

    ## Store current state
    copiedSquadUnits = squadUnits[squadIndex]
    copiedSquadNums = squadNums[squadIndex]

def pasteSquad():
    ### PURPOSE: When a squad is pasted, this function is called
    ### to overwrite the current squad with the pasted squad

    global squadUnits
    global squadNums
    global copiedSquadUnits
    global copiedSquadNums
    
    ## Get current squad index
    squadIndex = int(selSquadDdText.get())-1

    ## Replace current squad with stored squad
    squadUnits[squadIndex] = copiedSquadUnits
    squadNums[squadIndex] = copiedSquadNums

    ## Update list of units in current squad
    updateUnitList()
    
    ## Remove unit selection
    unselectUnit()

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
    unselectUnit()

def addUnit():
    ### PURPOSE: When a unit is added, this function is called
    ### to handle the UI and backend of appending that unit

    global squadUnits
    global squadNums

    # Get index of squad to add to
    squadIndex = int(selSquadDdText.get())-1

    if rbChoice.get() == 1:
        # Add 1 of unit
        squadUnits[squadIndex].append(unitNameDDtext.get())
        squadNums[squadIndex].append(1)
    else:
        # Add 1 of unit
        squadUnits[squadIndex].append(nameVar.get())
        squadNums[squadIndex].append(1)

    # Update ListBox
    updateUnitList()

    ## Remove unit selection
    unselectUnit()

def updateSelNum(*args):
    ### PURPOSE: When an item in the listbox is selected, this function is called
    ### to set the number entry form to the number amount of that unit in that squad

    global selectIndex
    if curr_squad.curselection() != ():
        squadIndex = int(selSquadDdText.get())-1            # Current squad number
        selectIndex = curr_squad.curselection()[0]          # Index of selection in squad
        numVar.set(squadNums[squadIndex][selectIndex])      # Update amount entry
        sel_unit.set(squadUnits[squadIndex][selectIndex])   # Update unit name in UI
        ent_unitnum.config(state="normal")                  # Make amount entry editable
        btn_remove.config(state="normal")                   # Make remove unit button active
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
    if selectIndex < 0:
        return
    squadIndex = int(selSquadDdText.get())-1
    squadNums[squadIndex][selectIndex] = numVar.get()
    updateUnitList()

def enableButtons():
    global checkExperimental
    global btn_add
    global btn_delete
    ## If the box is checked
    if checkExperimental.get() == 1:
        # Warning message
        window.bell()
        popup = tk.Toplevel()

        label = tk.Label(popup,
        text="WARNING:\nChanging the number of squads is not currently supported by the server as of April 5th, 2021.\nGenerate a JSON at your own risk."
        )
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(popup, text="Close", command=popup.destroy)
        button_close.pack(pady=(0,5))
        ## Enable Buttons
        btn_add["state"] = "normal"
        btn_delete["state"] = "normal"
    ## If the box is not checked
    elif checkExperimental.get() == 0:
        ## Disable buttons
        btn_add.config(state="disabled")
        btn_delete.config(state="disabled")

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
    playerIdentifier = int(playerNumDdText.get())-1 # Translates DD options (1,2) to server-readable (0,1)

    # Call the function to write the current loadout to the appropriate JSON
    GenerateJsonFileLoadout(loadout, playerIdentifier)
    createPopUp("Saved to JSON!")

    if printStatementsThatEthanNeedsApparently == True:
        print("\nThis is the squad my UI displays")
        for squad in loadout:
            print(squad)
        print("Other than that it is sorted, they are identical\n")

    
        print("And for fun, the squad printed legibly (the way it is stored in the UI)")
        for indx1, squad in enumerate(squadNums):
            print("\nSquad "+str(indx1+1)+"\nLength: "+str(len(squadNums[indx1]))+"\n#######################")
            for indx2, unit in enumerate(squadUnits[indx1]):
                print(squadUnits[indx1][indx2]+": "+str(squadNums[indx1][indx2]))

def generateRandom():
    ### PURPOSE: When the "generate random squad" button is pressed, this function is called
    ### to call the random squad function (automatically writes to json) and load loadout into UI

    presetNumber = preset_dd['menu'].index(presetSelDdText.get())
    loadout = GenerateRandomLoadout(presetNumber)   #Defined in CreateJsonData.py

    if printStatementsThatEthanNeedsApparently == True:
        print("This is the squad your function returns")
        for squad in loadout:
            print(squad)

    global squadUnits
    global squadNums
    global numSquads

    tempsquadUnits = []
    tempsquadNums = []

    numSquads = len(loadout)

    ## The code snippet below translates the loadout from the format used by the random loadout function
    ## to the format defined at the top of this program so it is usable in the UI
    ## ex:      loadout[0]: ["Striker", "Striker", "Tank", "Tank", "Striker"]
    ## becomes: squadNums[0]: [3, 2]  &  squadUnits[0]: ["Striker", "Tank"]

    # For each squad (squad = int index of current squad)
    for squad in range(0,numSquads):    

        # Create an array representing that squad
        tempsquadNums.append([])
        tempsquadUnits.append([])

        for unit in loadout[squad]:     # For each unit in the current squad

            # If the unit is in the squad, increment its counters
            if unit in tempsquadUnits[squad]:
                indexOfUnitInSquad = tempsquadUnits[squad].index(unit)  # Find its index in the squad
                tempsquadNums[squad][indexOfUnitInSquad]+=1            # Increment its count

            # If this is a new unit type, add the count of the previous unit, add new name to the list of unit types, and begin counting from 1
            else:
                tempsquadUnits[squad].append(unit)  # Add this unit's name to the list
                tempsquadNums[squad].append(1)      # Add this unit's count to the list

    squadUnits = tempsquadUnits
    squadNums = tempsquadNums

    # Update UI to accomodate
    updateUnitList()
    refreshDropDown()

def unselectUnit():
    global selectIndex

    selectIndex = -1
    numVar.set("")
    sel_unit.set("[none]")
    ent_unitnum.config(state="disabled")
    btn_remove.config(state="disabled")

def selectAddMethod():
    if rbChoice.get() == 1:
        ent_unitname.grid_remove()
        unitNameDD.grid(row=3, column=0)
    elif rbChoice.get() == 2:
        unitNameDD.grid_remove()
        ent_unitname.grid(row=3, column=0)

def updateAddUnitList():
    presetNumber = preset_dd['menu'].index(presetSelDdText.get())
    unitNames = LoadAttributesBasedUnitFile(presetNumber)[0]
    numNames = len(unitNames)
    ## Remove current dropdown options
    unitNameDD['menu'].delete(0, 'end')

    ## Add new options

    for x in range (0, numNames):
        unitNameDD['menu'].add_command(label=str(unitNames[x]), command=tk._setit(unitNameDDtext, str(unitNames[x])))

    unitNameDDtext.set(unitNames[0])
    ## Remove unit selection
    unselectUnit()

## Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Squad Creator UI")
window.resizable(width=False, height=False)
section_bg = "#D8D8D8"

## Left-most column
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Create dropdown menu
sel_squad_frame = tk.Frame(master=left_frame)
sel_squad_frame.grid(row=0, column=0, sticky = "w")

selSquadDdText = tk.StringVar()
selSquadDdText.set("1")

def dd_callback(*args):
    updateUnitList()
selSquadDdText.trace("w", dd_callback)

sel_squad_lbl = tk.Label(master=sel_squad_frame, text="Select Squad: ")
sel_squad_lbl.grid(row=0, column=0, sticky="w")
sel_squad_ttp = CreateToolTip(sel_squad_frame, \
   'Select which squad to view and edit')
sel_squad_dd = tk.OptionMenu(sel_squad_frame, selSquadDdText, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
sel_squad_dd.config(width=2)
sel_squad_dd.grid(row=0, column=1, sticky="e",pady=(0,3))

curr_squad = tk.Listbox(master=left_frame)
curr_squad.config(width=25)
curr_squad.grid(row=1, column=0, sticky="ew")
curr_squad.bind('<<ListboxSelect>>', updateSelNum)

## Copy-Paste Frame
copy_paste_frame = tk.Frame(master=left_frame)
copy_paste_frame.grid(row=2, column=0, pady = (5,0))

# Copy Squad Button
btn_copy = tk.Button(
    master=copy_paste_frame,
    text="Copy Squad",
    command = copySquad
)
btn_copy_ttp = CreateToolTip(btn_copy, \
   'Stores the current squad to the program.\n\n'
   'Pasting a squad will overwrite the currently viewed squad with the stored squad.\n\n'
   'If a squad is already copied, it is overwritten by the current squad.')
btn_copy.grid(row=0, column=0, padx= (0,5))

# Paste Squad Button
btn_paste = tk.Button(
    master=copy_paste_frame,
    text="Paste Squad",
    command = pasteSquad
)
btn_paste_ttp = CreateToolTip(btn_paste, \
   'Overwrite the currently viewed squad with the stored squad.\n\n'
   'If nothing has been copied, the pasted squad will be empty.')
btn_paste.grid(row=0, column=1, padx= (5,0))


# Check Squad Number Change
checkExperimental = tk.IntVar()
change_num_cb = tk.Checkbutton(
    master = left_frame,
    text='Unimplemented Functions',
    variable=checkExperimental,
    onvalue=1, offvalue=0,
    command=enableButtons
)
change_num_cb.grid(row=3, column=0, pady=(20,0))

exper_frame = tk.Frame(master=left_frame, bg = section_bg, bd=2, relief = "ridge", padx=25, pady=3)
exper_frame.grid(row=4, column=0, sticky="ew")

# Add Squad Button
btn_add = tk.Button(
    master=exper_frame,
    text="Add Empty Squad",
    state = "disabled",
    command = addSquad
)
btn_add_ttp = CreateToolTip(btn_add, \
   'Appends an empty squad to the list of squads and jumps to it')
btn_add.grid(row=0, column=0, pady = 5)


# Delete Squad Button
btn_delete = tk.Button(
    master=exper_frame,
    text="Delete Current Squad",
    state = "disabled",
    command = deleteSquad
)
btn_delete_ttp = CreateToolTip(btn_delete, \
   'Deletes the currently viewed squad and jumps to the one before it numerically')
btn_delete.grid(row=1, column=0, pady = 5)


## Middle column
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')

## Frame and widgets for random squad generation
gametype_frame = tk.Frame(master=mid_frame)
gametype_ttp = CreateToolTip(gametype_frame, \
   "Select which gametype you will be using.\n\nThis changes which units are avilable in the existing name dropdown menu, as well as which JSON is written to.")
gametype_frame.grid(row=0, column=0)

presetnum_lbl = tk.Label(master=gametype_frame, text="Game Type: ")
presetnum_lbl.grid(row=0, column=0, sticky="w")

presetSelDdText = tk.StringVar()
presetSelDdText.set("Default Units")
def preset_callback(*args):
    updateAddUnitList()
presetSelDdText.trace("w", preset_callback)
preset_dd = tk.OptionMenu(gametype_frame, presetSelDdText, "Default Units", "Preset Units", "Custom Units")
preset_dd.grid(row=0, column=1, sticky="e")


## Selected unit area title
sel_unit_title_frame = tk.Frame(master=mid_frame)
sel_unit_title_frame.grid(row=1, column=0, sticky="w")

unit_sect_lbl = tk.Label(master=sel_unit_title_frame, text="Unit: ")
unit_sect_lbl.grid(row=0, column=0)

sel_unit = tk.StringVar()
sel_unit.set("[none]")
sel_unit_lbl = tk.Label(master=sel_unit_title_frame, textvariable=sel_unit)
sel_unit_lbl.grid(row=0, column=1, sticky="w")

### Selected unit area details
sel_unit_frame = tk.Frame(master=mid_frame, bg = section_bg, bd=2, relief = "ridge", padx=30, pady=3)
sel_unit_frame.grid(row=2, column=0)

## Number of
selectedNumber_frame = tk.Frame(master=sel_unit_frame, bg = section_bg)
selectedNumber_ttp = CreateToolTip(selectedNumber_frame, \
   "Change the amount of the selected unit in the squad.\n\nOnly allows numbers.")
selectedNumber_frame.grid(row=0, column=0, sticky="w")

num_unit_lbl = tk.Label(master=selectedNumber_frame, text="Amount: ", bg = section_bg)
num_unit_lbl.grid(row=0, column=0, sticky="w")

numVar = tk.StringVar()
def num_callback(*args):
    updateNum()
numVar.trace("w", num_callback)
vcmd = (selectedNumber_frame.register(checkNumInput), '%S')

ent_unitnum = tk.Entry(master=selectedNumber_frame, width=5, textvariable = numVar, validate='key', vcmd=vcmd, state="disabled")
ent_unitnum.grid(row=0, column=1, sticky="e")

# Remove Unit Button
btn_remove = tk.Button(
    master=sel_unit_frame,
    text="Remove Selected Unit",
    command = deleteUnit,
    state="disabled"
)
btn_remove_ttp = CreateToolTip(btn_remove, \
   'If a unit is selected,\n'
   'this button removes the selected unit from the squad.')
btn_remove.grid(row=1, column=0, pady = 10, sticky="w")



## Add unit area title
add_unit_lbl = tk.Label(master=mid_frame, text="Add a Unit to the Current Squad")
add_unit_lbl.grid(row=3, column=0, sticky="w", pady=(20,0))

### Add unit area details
add_unit_frame = tk.Frame(master=mid_frame, bg = section_bg, bd=2, relief = "ridge", padx=25, pady=3)
add_unit_frame.grid(row=4, column=0)

## Custom or existing radio buttons
rbChoice = tk.IntVar()
existingName = tk.Radiobutton(master= add_unit_frame, text="Existing Name", variable=rbChoice, value=1, bg = section_bg, command=selectAddMethod)
existingName_ttp = CreateToolTip(existingName, \
   "Set whether the added unit has the name of a unit already in the server's files or a new name.\n\nWarning!\nIf you enter a new unit name, define it in the unit creator!\nIf an undefined unit type is detected, the simulation will not run!")
existingName.grid(row=0, column=0)

customName = tk.Radiobutton(master = add_unit_frame, text="Custom Name", variable=rbChoice, value=2, bg = section_bg, command=selectAddMethod)
customName_ttp = CreateToolTip(customName, \
   "Set whether the added unit has the name of a unit already in the server's files or a new name.\n\nWarning!\nIf you enter a new unit name, define it in the unit creator!\nIf an undefined unit type is detected, the simulation will not run!")
customName.grid(row=1, column=0)
rbChoice.set(1)

unitNameDDtext = tk.StringVar()
unitNameDDtext.set("")
unitNameDD = tk.OptionMenu(add_unit_frame, unitNameDDtext, " ")
unitNameDD.config(width=20)
unitNameDD.grid(row=3, column=0)

## Custom name unit
nameVar = tk.StringVar()
ent_unitname = tk.Entry(master=add_unit_frame, width=25, textvariable = nameVar)

    

btn_new = tk.Button(
    master=add_unit_frame,
    text="Add Unit to Squad",
    command = addUnit
)
btn_new_ttp = CreateToolTip(btn_new, \
   "Adds a new unit to the squad.\n\n"
   "The unit's name is the text in the form above.\n\n"
   "The unit's amount defaults to 1.")
btn_new.grid(row=4, column=0, pady=10)


## Right column
right_frame = tk.Frame(master=window)
right_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")


## Frame and widgets for JSON generation
json_frame = tk.Frame(master=right_frame)
json_frame_ttp = CreateToolTip(json_frame, \
   "Set which player this squad will be set for.\n\n"
   "Although the shown values are 1 and 2,"
   "they are represented internally as 0 and 1")
json_frame.grid(row=0, column=0)

playnum_lbl = tk.Label(master=json_frame, text="Player Number: ")
playnum_lbl.grid(row=0, column=0, sticky="w")

playerNumDdText = tk.StringVar()
playerNumDdText.set("1")
playnum_dd = tk.OptionMenu(json_frame, playerNumDdText, "1", "2")
playnum_dd.grid(row=0, column=1, sticky="w")

btn_gen = tk.Button(
    master=right_frame,
    text="Generate JSON",
    command = generateJSON
)
btn_gen_ttp = CreateToolTip(btn_gen, \
   'Exports the squad defined in this UI to the server\'s files')
btn_gen.grid(row=1, column=0, pady=20)

btn_gen_random = tk.Button(
    master=right_frame,
    text="Create Random Squad",
    command = generateRandom
)
btn_random_ttp = CreateToolTip(btn_gen_random, \
   "Generates a random loadout of units in 12 squads.\n\n"
   "The units are pulled from the pool of units defined by the gametype.\n\n"
   "To learn more about the gametype, mouse over the \"Game Type:\" section.")
btn_gen_random.grid(row=2, column=0, pady=5)


# Run the application
updateAddUnitList()
window.mainloop()
