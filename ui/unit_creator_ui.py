# Zachary Neidig (zackneidig@gmail.com)
# 3/17/21
# This program is a UI used to more easily create and edit units

import sys
import tkinter as tk
from everglades_server.CreateJsonData import *
from everglades_server.ui_dependencies import *

thismodule = sys.modules[__name__]

unitList = [[],[]]
attrList = []

def loadFromFile():
    ### PURPOSE: When the "load from JSON" button is clicked, this function is called
    ### to load in the list of units and attributes from the server's files
    information = LoadAttributesBasedUnitFile(1)    ## The list of units
    dataList = LoadUnitAttributeFile()              ## The list of attributes
    ##LoadAttributesBasedUnitFile() defined in CreateJsonData
    ##The line below is the debug data I used to make sure the functions worked as intended
    #information = [["a", "b", "c"],[["name1", "name2", "name3"],["name1", "name3"],["name2"]]]
    #dataList = [["name1", "name2", "name3"],["eff1", "eff2", "eff3"],["desc1","desc2","desc3"],[1.1,2,3],[0,1,0],[1,2,3],[1,2,3]]

    if len(unitList) > 0:
        unitList.pop()
        unitList.pop()

    if len(attrList) > 0:
        for value in range(0,7):
                attrList.pop()

    for item in information:
        unitList.append(item)
    for item in dataList:
        attrList.append(item)

    createAttrList()
    refreshDropDown()
    checkIfCanDeleteUnit()

def generateFile():
    ### PURPOSE: When the "save to JSON" button is clicked, this function is called
    ### to save the list of units to the server's files
    GenerateAttributeBasedUnitsFile(unitList[0], unitList[1])
        
def refreshDropDown():
    ### PURPOSE: When the list of units changes, this function is called
    ### to update the options to reflect the changes

    ## Remove current dropdown options
    sel_attr_dd['menu'].delete(0, 'end')

    ## Add new options
    if len(unitList) > 0:
        if(len(unitList[0]) > 0):
            for choice in unitList[0]:
                sel_attr_dd['menu'].add_command(label=choice, command=tk._setit(ddtext, choice))
            ## Default to first choice and load its data
            ddtext.set(unitList[0][0])
        else:
            ddtext.set('')
    else:
        ddtext.set('')
    checkIfCanDeleteUnit()

def createAttrList():
    ### PURPOSE: When the load data button is pressed, this function is called
    ### to populate attribute list with all attributes

    ## Clear list of attributes and repopulate
    list_attr.delete(0, tk.END)
    for item in attrList[0]:
        list_attr.insert(tk.END, item)

def updateCost():
    ### PURPOSE: When a new unit's data is loaded, this function is called
    ### to update the cost of the unit as a UI element
    sum = 0
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    for usedAttr in unitList[1][attrNum]:
        attrIndex = attrList[0].index(usedAttr)
        sum += attrList[6][attrIndex]
    costVar.set(sum)

def saveToFile():
    ### PURPOSE: When the save to JSON button is pressed, this function is called
    ### to generate a JSON with the UIs data in it
    GenerateUnitAttributeFile(unitList[0], unitList[1], unitList[2], unitList[3], unitList[4], unitList[5], unitList[6])
    createPopUp("Saved to JSON!")

def loadUnit():
    ### PURPOSE: When a new unit name is selected in the dropdown, this function is called
    ### to load the unit's data into the UI
    ## Exception if text is blank
    if ddtext.get() == "":
        curr_attr.delete(0, tk.END)
        costVar.set(0)
        return
    ## Find index of current selection
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    
    ## Clear list of attributes and repopulate
    curr_attr.delete(0, tk.END)
    if len(unitList[1]) > 0:
        if len(unitList[1][attrNum]) > 0:
            for item in unitList[1][attrNum]:
                curr_attr.insert(tk.END, item)
    
    ## Update total cost
    updateCost()
    ## Check to update UI elements
    sanityCheck()

def addAttribute():
    ### PURPOSE: When the add attribute button is pressed, this function is called
    ### to add the currently selected attribute to the current unit
    if ddtext.get() == "":
        return
    ## If a selection is currently made
    if list_attr.curselection() != ():
        ## Get the name of the attribute
        toAdd = list_attr.get(list_attr.curselection())
        ## Get the index of the unit
        attrNum = sel_attr_dd['menu'].index(ddtext.get())
        ## Add the attribute to the unit
        unitList[1][attrNum].append(toAdd)
        ## Update list of unit's attributes
        curr_attr.insert(tk.END, toAdd)
        ## Update cost
        updateCost()

def removeAttribute():
    ### PURPOSE: When the remove attribute button is pressed, this function is called
    ### to remove the currently selected attribute from the current unit
    if ddtext.get() == "":
        return
    ## If a selection is currently made
    if curr_attr.curselection() != ():
        ## Get the name of the attribute
        toRemove = curr_attr.curselection()[0]
        ## Get the index of the unit
        attrNum = sel_attr_dd['menu'].index(ddtext.get())
        ## Remove the attribute to the unit
        endList = len(unitList[1][attrNum])-1
        for index, item in enumerate(unitList[1][attrNum]):
            if (index >= toRemove) & (index < endList):
                unitList[1][attrNum][index] = unitList[1][attrNum][index+1]
        unitList[1][attrNum].pop()
        ## Update list of unit's attributes
        curr_attr.delete(toRemove)
        ## Update cost
        updateCost()

def newUnit():
    if checkIfCanAddUnit() == False:
        return

    newName = nameVar.get()
    unitList[0].append(newName)
    unitList[1].append([])

    if ddtext.get() == "":
        refreshDropDown()
    else:
        sel_attr_dd['menu'].add_command(label=newName, command=tk._setit(ddtext, newName))
        ddtext.set(newName)

    loadUnit()

def deleteAttribute():
    if ddtext.get() == " ":
        return
    ## Get current & end of data index
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    
    ## Pop duplicated final data
    unitList[0].pop(attrNum)
    unitList[1].pop(attrNum)

    ## Update dropdown
    refreshDropDown()

def updateDescription(*args):
    sanityCheck()
    ## If a selection is currently made in the list of all attributes
    if list_attr.curselection() != ():
        ## Get the name of the attribute
        toDesc = list_attr.curselection()[0]
    elif curr_attr.curselection() != ():
        global attrList
        print(attrList)
        attributeName = curr_attr.get(curr_attr.curselection()[0])
        toDesc = attrList[0].index(attributeName)
    ## Delete and repopulate description text
    ent_unitnum.config(state="normal")
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.insert(tk.END, attrList[2][toDesc])
    ent_unitnum.config(state="disabled")
    ## Update cost above listbox
    costVar2.set(attrList[6][toDesc])
    sanityCheck()

def sanityCheck():
    checkIfCanAddAttr()
    checkIfCanRemoveAttr()

def checkIfCanAddAttr():
    selection = list_attr.curselection()
    if len(selection) == 0:
        ## No selection
        btn_add.config(state="disabled")
    else:
        selIndex = selection[0]
        if attrList[6][selIndex] > 6 - costVar.get():
            btn_add.config(state="disabled")
        else:
            btn_add.config(state="normal")

def checkIfCanRemoveAttr():
    selection = curr_attr.curselection()
    if len(selection) == 0:
        ## No selection
        btn_rmv.config(state="disabled")
    else:
        btn_rmv.config(state="normal")

def checkIfCanDeleteUnit():
    global unitList
    if len(unitList[0]) > 0:
        btn_dlt.config(state="normal")
    else:
        btn_dlt.config(state="disabled")

def checkIfCanAddUnit():
    newName = nameVar.get()

    if len(newName) == 0:
        createPopUp("Unit name cannot be empty!")
        return False   
    else:
        global unitList
        if newName in unitList[0]:
            createPopUp("Unit with that name already defined!")
            return False
    return True
            

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Unit Creator")
window.resizable(width=False, height=False)
section_bg = "#D8D8D8"
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10)
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=1, padx=10, pady=10)


# First column
# Load and Save Button
loadSaveTitle = tk.Label(master=left_frame, text="Load from / Save to Server")
loadSaveTitle.grid(row=0, column=0, padx=(5,0),pady=(5,0), sticky="w")
data_frame = tk.Frame(master=left_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
data_frame.grid(row=1, column=0, sticky="w", pady = (0, 30))

btn_load = tk.Button(
    master=data_frame,
    text="Load From JSON",
    command = loadFromFile
)
btn_load_ttp = CreateToolTip(btn_load, \
   'Imports the custom units defined in the server\'s files to this UI')
btn_load.grid(row=0, column=0, padx = (0,10))

btn_make = tk.Button(
    master=data_frame,
    text="Generate JSON",
    command = generateFile
)
btn_make_ttp = CreateToolTip(btn_make, \
   'Exports the list of units defined in this UI to the server\'s files')
btn_make.grid(row=0, column=1)

# Select Unit Dropdown
dd_frame = tk.Frame(master=left_frame)
dd_frame.grid(row=2, column=0, sticky="w")
ddtext = tk.StringVar()
ddtext.set("")
def dd_callback(*args):
    loadUnit()
ddtext.trace("w", dd_callback)
sel_attr_lbl = tk.Label(master=dd_frame, text="Select Unit: ")
sel_attr_lbl.grid(row=0, column=0, sticky="e")
sel_attr_dd = tk.OptionMenu(dd_frame, ddtext, " ")
sel_attr_dd.config(width=20)
sel_attr_dd.grid(row=0, column=1, sticky="w")


addDltTitle = tk.Label(master=left_frame, text="Create / Delete Unit Types")
addDltTitle.grid(row=3, column=0, padx=(5,0),pady=(5,0), sticky="w")
addDlt_frame = tk.Frame(master=left_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
addDlt_frame.grid(row=4, column=0, sticky="w")

# Delete Unit Button
btn_dlt = tk.Button(
    master=addDlt_frame,
    text="Delete Selected Unit",
    command = deleteAttribute
)
btn_dlt_ttp = CreateToolTip(btn_dlt, \
   "Removes the currently selected unit and jumps to the first in the list.")
btn_dlt.grid(row=0, column=0, pady=(5,15))

# New Unit
nameVar = tk.StringVar()
unitname_lbl = tk.Label(master=addDlt_frame, text="Name of New Unit: ", bg = section_bg)
unitname_lbl.grid(row=1, column=0, sticky="w")

add_frame = tk.Frame(master=addDlt_frame, bg = section_bg)
add_frame_ttp = CreateToolTip(add_frame, \
   "Adds a new unit with the name in the entry form above.\n\n"
   "The unit must have an original name and be non-empty.")
add_frame.grid(row=2, column=0, sticky="w")
ent_unitname = tk.Entry(master=add_frame, width=20, textvariable = nameVar)
ent_unitname.grid(row=0, column=0, sticky="w")

btn_new = tk.Button(
    master=add_frame,
    text="Add",
    command = newUnit
)
btn_new.grid(row=0, column=1, padx = (5,0))



# Second column
# Cost of Unit
midcost_frame = tk.Frame(master=mid_frame)
midcost_frame_ttp = CreateToolTip(midcost_frame, \
   "The total cost of the unit.\n\n"
   "The cost of a unit is the sum of the cost of the attributes on it.\n\n"
   "A unit's cost cannot exceed 6.")
midcost_frame.grid(row=0, column=0, sticky="w")

costVar = tk.IntVar()
costVar.set("0")
cost_lbl = tk.Label(master=midcost_frame, text="Cost of Unit: ")
cost_lbl.grid(row=0, column=0)
cost_num_lbl = tk.Label(master=midcost_frame, textvariable = costVar)
cost_num_lbl.grid(row=0, column=1)
cost_max_lbl = tk.Label(master=midcost_frame, text="/ 6")
cost_max_lbl.grid(row=0, column=2)

# List of Unit's Attributes
curr_lbl = tk.Label(master=mid_frame, text="Current Unit's Attributes: ")
curr_lbl.grid(row=1, column=0, sticky="w")
curr_attr = tk.Listbox(master=mid_frame)
curr_attr.grid(row=2, column=0, sticky="w", padx=(0,20))
curr_attr.bind('<<ListboxSelect>>', updateDescription)

# Remove Attribute
btn_rmv = tk.Button(
    master=mid_frame,
    text="Remove Attribute",
    command = removeAttribute
)
btn_rmv_ttp = CreateToolTip(btn_rmv, \
   "Remove the currently selected attribute from the current unit.")
btn_rmv.grid(row=3, column=0, pady=(15,0), padx=(0,15))



# Third Column
rightcost_frame = tk.Frame(master=mid_frame)
rightcost_frame_ttp = CreateToolTip(rightcost_frame, \
   "The cost of the currently selected attribute.\n\n"
   "The cost of a unit is the sum of the cost of the attributes on it.")
rightcost_frame.grid(row=0, column=1, sticky="w", rowspan = True)

costVar2 = tk.IntVar()
costVar2.set("0")
cost_lbl = tk.Label(master=rightcost_frame, text="Cost of Attribute: ")
cost_lbl.grid(row=0, column=0)
cost_attr_lbl = tk.Label(master=rightcost_frame, textvariable = costVar2)
cost_attr_lbl.grid(row=0, column=1)


list_lbl = tk.Label(master=mid_frame, text="List of Attributes: ")
list_lbl.grid(row=1, column=1, sticky="w")
list_attr = tk.Listbox(master=mid_frame)
list_attr.grid(row=2, column=1, sticky="e", padx=(0,20))
list_attr.bind('<<ListboxSelect>>', updateDescription)

btn_add = tk.Button(
    master=mid_frame,
    text="Add Attribute",
    command = addAttribute
)
btn_add_ttp = CreateToolTip(btn_add, \
   "Adds the currently selected attribute to the current unit.")
btn_add.grid(row=3, column=1, pady=(15,0), padx=(0,15))

unitnum_lbl = tk.Label(master=mid_frame, text="Attribute Information: ")
unitnum_lbl.grid(row=1, column=2, sticky="w")
ent_unitnum = tk.Text(master=mid_frame, width = 25, height = 10, font = "TkTextFont", wrap="word", state="disabled")
ent_unitnum.grid(row=2, column=2, sticky="w")


# Run the application
sanityCheck()
checkIfCanDeleteUnit()
window.mainloop()
