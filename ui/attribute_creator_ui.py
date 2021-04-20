# Zachary Neidig (zackneidig@gmail.com)
# 3/17/21
# This program is a UI used to more easily create and edit attributes

import sys
import tkinter as tk
from everglades_server.CreateJsonData import *
from everglades_server.ui_dependencies import *

thismodule = sys.modules[__name__]

unitList = [[], [], [], [], [], [], []]
newVarCounter = 1

def loadFromFile():
    ### PURPOSE: When the load data button is pressed, this function is called
    ### to grab the attributes from the server files
    global unitList
    unitList = LoadUnitAttributeFile() # Defined in CreateJsonData.py, loads data from server files

    if len(unitList[0]) > 0:
        enableUI()
    
    # Populate dropdown with loaded data
    refreshDropDown()

def generateFile():
    ### PURPOSE: When the generate JSON button is pressed, this function is called
    ### to call the function in CreateJSONData.py to export to JSON
    GenerateUnitAttributeFile(unitList[0],unitList[1],unitList[2],unitList[3],unitList[4],unitList[5],unitList[6])
    createPopUp("Saved to JSON!")

def refreshDropDown():
    ### PURPOSE: When the list of attribute names changes, this function is called
    ### to update the listbox to reflect the current list of attributes

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
            ddtext.set(' ')
    else:
        ddtext.set(' ')

def loadAttribute():
    ### PURPOSE: When an attribute is selected from the dropdown, this function is called
    ### to load its details into the appropriate UI elements
    attrName = ddtext.get()

    if attrName == "" or len(unitList[0]) == 0:
        disableUI()
        return
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    nameVar.set(unitList[0][attrNum])
    effVar.set(unitList[1][attrNum])
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.insert(tk.END, unitList[2][attrNum])
    modVar.set(str(unitList[3][attrNum]))
    if unitList[4][attrNum] == 0:
        multVar.set("Static Value")
    else:
        multVar.set("Multiplier")
    costVar.set(str(unitList[6][attrNum]))

def saveAttribute():
    ### PURPOSE: When the save changes button is pressed, this function is called
    ### to save the entry forms' contents to the array.
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    unitList[0][attrNum] = nameVar.get()
    unitList[1][attrNum] = effVar.get()
    unitList[2][attrNum] = ent_unitnum.get("1.0",tk.END)
    unitList[3][attrNum] = float(modVar.get())

    multType = multVar.get()
    if multType == "Static Value":
        unitList[4][attrNum] = 0
    else:
        unitList[4][attrNum] = 1
    
    unitList[5][attrNum] = 1
    unitList[6][attrNum] = int(costVar.get())

    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    refreshDropDown()
    ddtext.set(unitList[0][attrNum])

def deleteAttribute():
    ### PURPOSE: When the delete attribute button is pressed, this function is called
    ### to pop the attribute currently selected by the dropdown menu
    
    ## Get index of currently selected attribute
    attrNum = sel_attr_dd['menu'].index(ddtext.get())

    ## Pop it out of the array
    for val in range(0,len(unitList)):
        unitList[val].pop(attrNum)
    
    ## Update dropdown
    refreshDropDown()

def newAttribute():
    ### PURPOSE: When the new attribute button is pressed, this function is called
    ### to create an attribute with a unique name and append it to the list of attributes

    global newVarCounter
    global unitList

    ## Data that populates new attribute
    sampleData = ["Name"+str(newVarCounter),'Health','Description','0','0','0','0']
    newVarCounter+=1

    ## Add new data to array
    for val in range(0,len(unitList)):
        unitList[val].append(sampleData[val])

    ## Jump to new data in dropdown menu
    sel_attr_dd['menu'].add_command(label=sampleData[0], command=tk._setit(ddtext, sampleData[0]))

    ## If this is the first attribute
    if len(unitList[0]) == 1:
        ## There were no attributes before this one
        enableUI()          ## Re-enable UI
        refreshDropDown()   ## Update list of attributes
    else:
        ddtext.set(sampleData[0])   ## Set dropdown to name, which will load it into UI on traceback

def enableUI():
    ### PURPOSE: When the amount of attributes goes from 0 to >0, this function is called
    ### to enable the UI elements
    ent_unitnum.config(bg="#FFF")
    for x in [btn_dlt, ent_unitname, ent_unitnum, uniteff_dd, ent_unitcost, ent_unitmod, multTypeDD]:
        x.config(state="normal")

def disableUI():
    ### PURPOSE: When the amount of attributes goes to 0, this function is called
    ### to disable the UI elements
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.config(bg="#F0F0F0")
    for x in [nameVar, effVar, costVar, modVar, multVar]:
        x.set("")
    for x in [btn_dlt, ent_unitname, ent_unitnum, uniteff_dd, ent_unitcost, ent_unitmod, multTypeDD]:
        x.config(state="disabled")

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Attribute Creator")
window.resizable(width=False, height=False)
section_bg = "#D8D8D8"
right_frame = tk.Frame(master=window)
right_frame.grid(row=0, column=1, padx=10, pady=10)
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Right column
header_frame = tk.Frame(master=right_frame)
header_frame.grid(row=0, column=0, sticky ="w")

nameVar = tk.StringVar()
unitname_lbl = tk.Label(master=header_frame, text="Name: ")
unitname_lbl.grid(row=0, column=0, sticky="w")
ent_unitname = tk.Entry(master=header_frame, width=25, textvariable = nameVar)
ent_unitname.grid(row=1, column=0, sticky="w")

btn_save = tk.Button(
    master=header_frame,
    text="Save Changes",
    command = saveAttribute
)
btn_save_ttp = CreateToolTip(btn_save, \
   'Saves changes to the currently selected attribute.\n\nIf you do not press this before changing attribute or exporting to JSON, changes will NOT be saved automatically!')
btn_save.grid(row=0, column=1, rowspan=2, padx=(5,0), pady=(10,0))

unitnum_lbl = tk.Label(master=right_frame, text="Description: ")
unitnum_lbl.grid(row=2, column=0, sticky="w")
ent_unitnum = tk.Text(master=right_frame, width=40, height=10, font = "TkTextFont", wrap="word")
ent_unitnum_ttp = CreateToolTip(ent_unitnum, \
   "The description of the attribute\s effect on the unit.\n\n"
   "Does not impact its effect, but does describe it in the unit creator UI.")
ent_unitnum.grid(row=3, column=0, sticky="w")

effCostFrame = tk.Frame(master=right_frame)
effCostFrame.grid(row=4, column=0, sticky='w')

effVar = tk.StringVar()
effVar.set("Health")
uniteff_lbl = tk.Label(master=effCostFrame, text="Effect: ")
uniteff_lbl.grid(row=0, column=1, sticky="w", padx=(10,0))
uniteff_dd = tk.OptionMenu(effCostFrame, effVar, "Health", "Damage", "Speed", "SpeedBonus_Controlled_Ally", "SpeedBonus_Controlled_Enemy", "Jamming", "Commander_Damage", "Commander_Speed", "Commander_Control", "Self_Repair", "Control", "Recon")
## uniteff_dd = tk.OptionMenu(effCostFrame, effVar, "Health", "Damage", "Speed")
uniteff_dd_ttp = CreateToolTip(uniteff_dd, \
   "The stat of the unit that is impacted by this attribute.")
uniteff_dd.grid(row=1, column=1, sticky="w", padx=(10,0))

costVar = tk.IntVar()
unitcost_lbl = tk.Label(master=effCostFrame, text="Cost: ")
unitcost_lbl.grid(row=0, column=0, sticky="sw")
ent_unitcost = tk.Entry(master=effCostFrame, width=5, textvariable = costVar)
ent_unitcost_ttp = CreateToolTip(ent_unitcost, \
   "The cost conferred on the unit for having this attribute.\n\n"
   "The maximum cost of a unit (and thus an attribute) is 6.")
ent_unitcost.grid(row=1, column=0, sticky="w")

mod_frame = tk.Frame(master=right_frame)
mod_frame.grid(row=5, column=0)

modVar = tk.StringVar()
modifier_lbl = tk.Label(master=mod_frame, text="Modifier Value:")
modifier_lbl.grid(row=0, column=0, sticky="w")
ent_unitmod = tk.Entry(master=mod_frame, width=12, textvariable = modVar)
ent_unitmod_ttp = CreateToolTip(ent_unitmod, \
   "The value of the modifier.\n\n"
   "If the modifier is multiplicative, the base stat is multiplied by this value.\n\n"
   "If the modifier is a static value, the base stat is overwritten by this value.")
ent_unitmod.grid(row=1, column=0, sticky="w")

multVar = tk.StringVar()
multVar.set("Static Value")
isMult_lbl = tk.Label(master=mod_frame, text="Modifier Type:")
isMult_lbl.grid(row=0, column=1, sticky="w", padx=(10,0))
multTypeDD = tk.OptionMenu(mod_frame, multVar, "Static Value", "Multiplier")
multTypeDD_ttp = CreateToolTip(multTypeDD, \
   "If the modifier is multiplicative, the base stat is multiplied by the modifier value.\n\n"
   "If the modifier is a static value, the base stat is overwritten by the modifier value.")
multTypeDD.config(width = 20)
multTypeDD.grid(row=1, column=1, sticky="w", padx=(10,0))



## Left column
# Top third
loadSaveTitle = tk.Label(master=left_frame, text="Load from / Save to Server")
loadSaveTitle.grid(row=0, column=0, padx=(5,0),pady=(5,0), sticky="w")
file_frame = tk.Frame(master=left_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
file_frame.grid(row=1, column=0)

btn_load = tk.Button(
    master=file_frame,
    text="Load From JSON",
    command = loadFromFile
)
btn_load_ttp = CreateToolTip(btn_load, \
   'Imports the list of attributes defined in the server\'s files to this UI')
btn_load.grid(row=0, column=0, padx=(0,10))
btn_make = tk.Button(
    master=file_frame,
    text="Generate JSON",
    command = generateFile
)
btn_make_ttp = CreateToolTip(btn_make, \
   'Exports the list of attributes defined in this UI to the server\'s files')
btn_make.grid(row=0, column=1)

# Middle third, including dropdown menu
dd_frame = tk.Frame(master=left_frame)
dd_frame.grid(row=2, column=0, pady=35)

ddtext = tk.StringVar()
ddtext.set("")
def dd_callback(*args):
    loadAttribute()
ddtext.trace("w", dd_callback)
sel_attr_lbl = tk.Label(master=dd_frame, text="Select Attribute: ")
sel_attr_lbl.grid(row=0, column=0, sticky="w")
sel_attr_dd = tk.OptionMenu(dd_frame, ddtext, unitList[0])
sel_attr_dd.config(width=18)
sel_attr_dd.grid(row=0, column=1)


# Bottom third
createDeleteTitle = tk.Label(master=left_frame, text="Create / Delete Attributes")
createDeleteTitle.grid(row=3, column=0, padx=(8,0),pady=(5,0), sticky="w")
newdel_frame = tk.Frame(master=left_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
newdel_frame.grid(row=4, column=0)

btn_new = tk.Button(
    master=newdel_frame,
    text="New Attribute",
    command = newAttribute
)
btn_new_ttp = CreateToolTip(btn_new, \
   "Adds a new attribute to the list of attributes.")
btn_new.grid(row=0, column=0)

btn_dlt = tk.Button(
    master=newdel_frame,
    text="Delete Selected",
    command = deleteAttribute,
)
btn_dlt_ttp = CreateToolTip(btn_dlt, \
   "Removes the currently selected attribute and jumps to the first in the list.")
btn_dlt.grid(row=0, column=1, padx=(15,0))

def startApplication():
    window.mainloop()

# Run the application
disableUI()
startApplication()
