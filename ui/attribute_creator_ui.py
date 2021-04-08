# Zachary Neidig (zackneidig@gmail.com)
# 3/17/21
# This program is a UI used to more easily create and edit attributes

import sys
import tkinter as tk
from everglades_server.CreateJsonData import *

thismodule = sys.modules[__name__]

unitList = [[], [], [], [], [], [], []]
newVarCounter = 1

#Format:
    ### PURPOSE: When , this function is called
    ### to

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
    GenerateUnitAttributeFile(unitList[0],unitList[1],unitList[2],unitList[3],unitList[4],unitList[5],unitList[6])

def refreshDropDown():
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

def saveToFile():
    GenerateUnitAttributeFile(unitList[0], unitList[1], unitList[2], unitList[3], unitList[4], unitList[5], unitList[6])

def loadAttribute():
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
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    unitList[0][attrNum] = nameVar.get()
    unitList[1][attrNum] = effVar.get()
    unitList[2][attrNum] = ent_unitnum.get("1.0",tk.END)
    unitList[3][attrNum] = float(modVar.get())
    unitList[4][attrNum] = int(multVar.get())
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
    ## Get current & end of data index
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    final = len(unitList[0])-1
    ## Move all data above deletion down an index
    for num in range(attrNum, final):
        for val in range(0,len(unitList)):
            unitList[val][num] = unitList[val][num+1]
    ## Pop duplicated final data
    for val in range(0,len(unitList)):
        unitList[val].pop()
    ## Update dropdown
    refreshDropDown()

def newAttribute():
    global newVarCounter
    global unitList
    ## Data that populates new attribute
    sampleData = ["Name"+str(newVarCounter),'Effect','Description','0','0','0','0']
    newVarCounter+=1

    for val in range(0,len(unitList)):
        unitList[val].append(sampleData[val])

    sel_attr_dd['menu'].add_command(label=sampleData[0], command=tk._setit(ddtext, sampleData[0]))

    if len(unitList[0]) == 1:
        enableUI()
        refreshDropDown()
    else:
        ddtext.set(sampleData[0])

def enableUI():
    ent_unitnum.config(bg="#FFF")
    for x in [btn_dlt, ent_unitname, ent_unitnum, ent_uniteff, ent_unitcost, ent_unitmod, multTypeDD]:
        x.config(state="normal")

def disableUI():
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.config(bg="#F0F0F0")
    for x in [nameVar, effVar, costVar, modVar, multVar]:
        x.set("")
    for x in [btn_dlt, ent_unitname, ent_unitnum, ent_uniteff, ent_unitcost, ent_unitmod, multTypeDD]:
        x.config(state="disabled")

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Attribute Creator")
window.resizable(width=True, height=True)
section_bg = "#D8D8D8"
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=1, padx=10, pady=10)
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Right column
header_frame = tk.Frame(master=left_frame)
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
btn_save.grid(row=0, column=1, rowspan=2, padx=(5,0), pady=(10,0))

unitnum_lbl = tk.Label(master=left_frame, text="Description: ")
unitnum_lbl.grid(row=2, column=0, sticky="w")
ent_unitnum = tk.Text(master=left_frame, width=40, height=10, font = "TkTextFont", wrap="word")
ent_unitnum.grid(row=3, column=0, sticky="w")

effCostFrame = tk.Frame(master=left_frame)
effCostFrame.grid(row=4, column=0, sticky='w')

effVar = tk.StringVar()
uniteff_lbl = tk.Label(master=effCostFrame, text="Effect: ")
uniteff_lbl.grid(row=0, column=0, sticky="w")
ent_uniteff = tk.Entry(master=effCostFrame, width=30, textvariable = effVar)
ent_uniteff.grid(row=1, column=0, sticky="w")

costVar = tk.IntVar()
unitcost_lbl = tk.Label(master=effCostFrame, text="Cost: ")
unitcost_lbl.grid(row=0, column=1, sticky="sw", padx=(10,0))
ent_unitcost = tk.Entry(master=effCostFrame, width=5, textvariable = costVar)
ent_unitcost.grid(row=1, column=1, sticky="w", padx=(10,0))

mod_frame = tk.Frame(master=left_frame)
mod_frame.grid(row=5, column=0)

modVar = tk.StringVar()
modifier_lbl = tk.Label(master=mod_frame, text="Modifier Value:")
modifier_lbl.grid(row=0, column=0, sticky="w")
ent_unitmod = tk.Entry(master=mod_frame, width=12, textvariable = modVar)
ent_unitmod.grid(row=1, column=0, sticky="w")

multVar = tk.StringVar()
multVar.set("Static Value")
isMult_lbl = tk.Label(master=mod_frame, text="Modifier Type:")
isMult_lbl.grid(row=0, column=1, sticky="w", padx=(10,0))
multTypeDD = tk.OptionMenu(mod_frame, multVar, "Static Value", "Multiplier")
multTypeDD.config(width = 20)
multTypeDD.grid(row=1, column=1, sticky="w", padx=(10,0))



## Left column
# Top third
loadSaveTitle = tk.Label(master=mid_frame, text="Load from / Save to Server")
loadSaveTitle.grid(row=0, column=0, padx=(5,0),pady=(5,0), sticky="w")
file_frame = tk.Frame(master=mid_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
file_frame.grid(row=1, column=0)

btn_load = tk.Button(
    master=file_frame,
    text="Load From JSON",
    command = loadFromFile
)
btn_load.grid(row=0, column=0, padx=(0,10))
btn_make = tk.Button(
    master=file_frame,
    text="Generate JSON",
    command = generateFile
)
btn_make.grid(row=0, column=1)

# Middle third, including dropdown menu
dd_frame = tk.Frame(master=mid_frame)
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
createDeleteTitle = tk.Label(master=mid_frame, text="Create / Delete Attributes")
createDeleteTitle.grid(row=3, column=0, padx=(8,0),pady=(5,0), sticky="w")
newdel_frame = tk.Frame(master=mid_frame, bg = section_bg, bd=2, relief = "ridge", padx=15, pady=8)
newdel_frame.grid(row=4, column=0)

btn_new = tk.Button(
    master=newdel_frame,
    text="New Attribute",
    command = newAttribute
)
btn_new.grid(row=0, column=0)

btn_dlt = tk.Button(
    master=newdel_frame,
    text="Delete Selected",
    command = deleteAttribute,
)
btn_dlt.grid(row=0, column=1, padx=(15,0))

def startApplication():
    window.mainloop()

# Run the application
disableUI()
startApplication()
