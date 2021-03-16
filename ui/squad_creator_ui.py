import sys
import tkinter as tk
from everglades_server.CreateJsonData import *

thismodule = sys.modules[__name__]

numSquads = 12
squadUnits = []
squadNums = []
tempSquadUnits = []
tempSquadNums = []
selectIndex = -1

for x in range(0, numSquads):
    squadUnits.append([])
    squadNums.append([])

def refreshDropDown():
    ## Remove current dropdown options
    sel_squad_dd['menu'].delete(0, 'end')
    ## Add new options
    for x in range (1, numSquads+1):
        sel_squad_dd['menu'].add_command(label=str(x), command=tk._setit(ddtext, str(x)))
    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def updateUnitList():
    ## Get index of current squad
    squadIndex = int(ddtext.get())-1
    ## Clear listbox of units
    curr_squad.delete(0, tk.END)
    ## Repopulate with up-to-date units and counts
    if len(squadUnits[squadIndex]) > 0:
        for x in range(0,len(squadUnits[squadIndex])):
            curr_squad.insert(tk.END, str(squadUnits[squadIndex][x]) + " ("+str(squadNums[squadIndex][x])+")")

def addSquad():
    global numSquads
    global squadUnits
    global squadNums

    ## Append empty squad
    numSquads+=1
    squadUnits.append([])
    squadNums.append([])
    ## Jump to new squad
    ddtext.set(str(numSquads))
    ## Update dropdown & listbox
    refreshDropDown()
    updateUnitList()

def deleteSquad():
    global numSquads
    global squadUnits
    global squadNums

    if numSquads == 1:
        return
    
    ## Get current index
    squadIndex = int(ddtext.get())-1
    ## Pop index & update counter
    squadUnits.pop(squadIndex)
    squadNums.pop(squadIndex)
    numSquads-=1
    ## Jump down an index if necessary
    if int(ddtext.get()) > numSquads:
       ddtext.set(numSquads)
    ## Update dropdown and listbox
    refreshDropDown()
    updateUnitList()

def copySquad():
    global squadUnits
    global squadNums
    global tempSquadUnits
    global tempSquadNums
    
    ## Get current squad index
    squadIndex = int(ddtext.get())-1
    ## Store current state
    tempSquadUnits = squadUnits[squadIndex]
    tempSquadNums = squadNums[squadIndex]

def pasteSquad():
    global squadUnits
    global squadNums
    global tempSquadUnits
    global tempSquadNums
    
    ## Get current squad index
    squadIndex = int(ddtext.get())-1
    ## Replace current squad with stored squad
    squadUnits[squadIndex] = tempSquadUnits
    squadNums[squadIndex] = tempSquadNums
    ## Update list of units in current squad
    updateUnitList()
    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def deleteUnit():
    global squadUnits
    global squadNums
    global selectIndex
    
    if selectIndex > -1:
        squadIndex = int(ddtext.get())-1
        squadUnits[squadIndex].pop(selectIndex)
        squadNums[squadIndex].pop(selectIndex)
    ## Update list of units in current squad
    updateUnitList()
    ## Remove unit selection
    selectIndex = -1

def addUnit():
    global squadUnits
    global squadNums
    # Get index of squad to add to
    squadIndex = int(ddtext.get())-1
    # Add 1 of unit
    squadUnits[squadIndex].append(nameVar.get())
    squadNums[squadIndex].append(1)
    # Update ListBox
    updateUnitList()
    ## Remove unit selection
    global selectIndex
    selectIndex = -1

def updateSelNum(*args):
    global selectIndex
    if curr_squad.curselection() != ():
        squadIndex = int(ddtext.get())-1
        selectIndex = curr_squad.curselection()[0]
        numVar.set(squadNums[squadIndex][selectIndex])
    else:
        if selectIndex < 0:
            numVar.set("")

def checkNumInput(S):
    if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '']:
        return True
    print(S)
    window.bell() # .bell() plays that ding sound telling you there was invalid input
    return False

def updateNum():
    global selectIndex
    squadIndex = int(ddtext.get())-1
    squadNums[squadIndex][selectIndex] = numVar.get()
    updateUnitList()

def generateJSON():
    global squadUnits
    global squadNums
    global numSquads
    loadout = []
    
    for squadNumber in range(0,numSquads):
        loadout.append([])
        unitslength = len(squadUnits[squadNumber])
        for unitInList in range(0,unitslength):
            for unitNumber in range(0, int(squadNums[squadNumber][unitInList])):
                loadout[squadNumber].append(squadUnits[squadNumber][unitInList])
            
    playerIdentifier = int(ddtext2.get())
    #print(loadout)
    #print(playerIdentifier)
    GenerateJsonFileLoadout(loadout, playerIdentifier)

def generateRandom():
    loadout = GenerateRandomLoadout(int(ddtext22.get()))

    global squadUnits
    tempsquadUnits = []
    global squadNums
    tempsquadNums = []
    global numSquads

    numSquads = len(loadout)
    prevUnitName = ""
    counter = 0

    for squad in range(0,numSquads):
        tempsquadNums.append([])
        tempsquadUnits.append([])
        for unit in loadout[squad]:
            if unit != prevUnitName:
                if counter > 0:
                    tempsquadNums[squad].append(counter)
                tempsquadUnits[squad].append(unit)
                counter = 1
            if unit == prevUnitName:
                counter+=1
        tempsquadNums[squad].append(counter)

    squadUnits = tempsquadUnits
    squadNums = tempsquadNums

    updateUnitList()
    refreshDropDown()

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Squad Creator UI")
window.resizable(width=True, height=True)

# Left-most UI
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Create dropdown menu
topleft_frame = tk.Frame(master=left_frame)
topleft_frame.grid(row=0, column=0)
ddtext = tk.StringVar()
ddtext.set("1")
def dd_callback(*args):
    updateUnitList()
ddtext.trace("w", dd_callback)
sel_squad_lbl = tk.Label(master=topleft_frame, text="Select Squad: ")
sel_squad_dd = tk.OptionMenu(topleft_frame, ddtext, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
sel_squad_lbl.grid(row=0, column=0, sticky="w")
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


## Second column
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

# Create bottom row of features
foot_frame = tk.Frame(master=right_frame)
foot_frame.grid(row=5, column=0, pady=(15,0))

playnum_lbl = tk.Label(master=foot_frame, text="Player Number: ")
playnum_lbl.grid(row=0, column=0, sticky="w")

ddtext2 = tk.StringVar()
ddtext2.set("0")
playnum_dd = tk.OptionMenu(foot_frame, ddtext2, "0", "1", "2")
playnum_dd.grid(row=0, column=1, sticky="e")

btn_gen = tk.Button(
    master=foot_frame,
    text="Generate JSON",
    command = generateJSON
)
btn_gen.grid(row=0, column=2, sticky="e")

foot_frame2 = tk.Frame(master=right_frame)
foot_frame2.grid(row=6, column=0, pady=(15,0))

playnum_lbl2 = tk.Label(master=foot_frame2, text="Preset Number: ")
playnum_lbl2.grid(row=0, column=0, sticky="w")

ddtext22 = tk.StringVar()
ddtext22.set("0")
playnum_dd2 = tk.OptionMenu(foot_frame2, ddtext2, "0", "1")
playnum_dd2.grid(row=0, column=1, sticky="e")

btn_gen2 = tk.Button(
    master=foot_frame2,
    text="Create Random Squad",
    command = generateRandom
)
btn_gen2.grid(row=0, column=2, sticky="e")

# Run the application
window.mainloop()
