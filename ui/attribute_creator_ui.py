# Zachary Neidig (zackneidig@gmail.com)
# 3/17/21
# This program is a UI used to more easily create and edit attributes

import sys
import tkinter as tk
from everglades_server.CreateJsonData import *

thismodule = sys.modules[__name__]

unitList = []
newVarCounter = 1

#Format:
    ### PURPOSE: When , this function is called
    ### to

def loadFromFile():
    ### PURPOSE: When the load data button is pressed, this function is called
    ### to grab the attributes from the server files
    global unitList
    unitList = LoadUnitAttributeFile() # Defined in CreateJsonData.py, loads data from server files

    # Populate dropdown with loaded data
    refreshDropDown()

def generateFile():
    GenerateUnitAttributeFile(unitList[0],unitList[1],unitList[2],unitList[3],unitList[4],unitList[5],unitList[6])

def refreshDropDown():
    ## Remove current dropdown options
    #ddtext.set('1')
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
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    nameVar.set(unitList[0][attrNum])
    effVar.set(unitList[1][attrNum])
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.insert(tk.END, unitList[2][attrNum])
    modVar.set(str(unitList[3][attrNum]))
    multVar.set(str(unitList[4][attrNum]))
    priorityVar.set(str(unitList[5][attrNum]))
    costVar.set(str(unitList[6][attrNum]))

def saveAttribute():
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    unitList[0][attrNum] = nameVar.get()
    unitList[1][attrNum] = effVar.get()
    unitList[2][attrNum] = ent_unitnum.get("1.0",tk.END)
    unitList[3][attrNum] = float(modVar.get())
    unitList[4][attrNum] = int(multVar.get())
    unitList[5][attrNum] = int(priorityVar.get())
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

    ## If no data exists
    if sel_attr_dd['text'] == '':
        for val in range(0,7):
            unitList.append(sampleData[val])
    else:
        ## Else (data exists)
        for val in range(0,len(unitList)):
            unitList[val].append(sampleData[val])
            #print(unitList[val][len(unitList[0])-1])

    sel_attr_dd['menu'].add_command(label=sampleData[0], command=tk._setit(ddtext, sampleData[0]))
    ddtext.set(sampleData[0])

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Attribute Creator")
window.resizable(width=True, height=True)
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=1, padx=10, pady=10)
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=0, padx=10, pady=10)
right_frame = tk.Frame(master=window)
right_frame.grid(row=0, column=2, padx=10, pady=10)
foot_frame = tk.Frame(master=window)
foot_frame.grid(row=0, column=3, padx=10, pady=10)

# Right column
nameVar = tk.StringVar()
unitname_lbl = tk.Label(master=left_frame, text="Name: ")
unitname_lbl.grid(row=0, column=0, sticky="w")
ent_unitname = tk.Entry(master=left_frame, width=25, textvariable = nameVar)
ent_unitname.grid(row=1, column=0, sticky="w")

unitnum_lbl = tk.Label(master=left_frame, text="Description: ")
unitnum_lbl.grid(row=2, column=0, sticky="w")
ent_unitnum = tk.Text(master=left_frame, width=30, height=10)
ent_unitnum.grid(row=3, column=0, sticky="w")

effVar = tk.StringVar()
uniteff_lbl = tk.Label(master=left_frame, text="Effect: ")
uniteff_lbl.grid(row=4, column=0, sticky="w")
ent_uniteff = tk.Entry(master=left_frame, width=30, textvariable = effVar)
ent_uniteff.grid(row=5, column=0, sticky="w")

mod_frame = tk.Frame(master=left_frame)
mod_frame.grid(row=6, column=0)

modVar = tk.StringVar()
modifier_lbl = tk.Label(master=mod_frame, text="Modifier: ")
modifier_lbl.grid(row=0, column=0, sticky="w")
ent_unitmod = tk.Entry(master=mod_frame, width=30, textvariable = modVar)
ent_unitmod.grid(row=1, column=0, sticky="w")

multVar = tk.StringVar()
isMult_lbl = tk.Label(master=mod_frame, text="isMult: ")
isMult_lbl.grid(row=0, column=1, sticky="w", padx=(10,0))
ent_unitmult = tk.Entry(master=mod_frame, width=2, textvariable = multVar)
ent_unitmult.grid(row=1, column=1, sticky="w", padx=(10,0))

priorityVar = tk.IntVar()
unitprio_lbl = tk.Label(master=mod_frame, text="Priority: ")
unitprio_lbl.grid(row=2, column=0, sticky="sw", pady = (0,0))
ent_unitprio = tk.Entry(master=mod_frame, width=5, textvariable = priorityVar)
ent_unitprio.grid(row=3, column=0, sticky="w")

costVar = tk.IntVar()
unitcost_lbl = tk.Label(master=mod_frame, text="Cost: ")
unitcost_lbl.grid(row=2, column=1, sticky="sw", padx=(10,0))
ent_unitcost = tk.Entry(master=mod_frame, width=5, textvariable = costVar)
ent_unitcost.grid(row=3, column=1, sticky="w", padx=(10,0))


## Left column
# Top third
file_frame = tk.Frame(master=mid_frame)
file_frame.grid(row=0, column=0, pady=(0,30))

btn_load = tk.Button(
    master=file_frame,
    text="Load From File",
    command = loadFromFile
)
btn_load.grid(row=0, column=0, padx=(0,10))
btn_make = tk.Button(
    master=file_frame,
    text="Generate File",
    command = generateFile
)
btn_make.grid(row=0, column=1)

# Middle third, including dropdown menu
dd_frame = tk.Frame(master=mid_frame)
dd_frame.grid(row=1, column=0)

ddtext = tk.StringVar()
ddtext.set("")
def dd_callback(*args):
    loadAttribute()
ddtext.trace("w", dd_callback)
sel_attr_lbl = tk.Label(master=dd_frame, text="Select Attribute: ")
sel_attr_lbl.grid(row=0, column=0, sticky="w")
sel_attr_dd = tk.OptionMenu(dd_frame, ddtext, "")
sel_attr_dd.config(width=20)
sel_attr_dd.grid(row=0, column=1)

btn_save = tk.Button(
    master=mid_frame,
    text="Save To Selected Attribute",
    command = saveAttribute
)
btn_save.grid(row=2, column=0, pady=(0,30))

# Bottom third
newdel_frame = tk.Frame(master=mid_frame)
newdel_frame.grid(row=3, column=0)

btn_new = tk.Button(
    master=newdel_frame,
    text="New Attribute",
    command = newAttribute
)
btn_new.grid(row=0, column=0)

btn_dlt = tk.Button(
    master=newdel_frame,
    text="Delete Selected",
    command = deleteAttribute
)
btn_dlt.grid(row=0, column=1, padx=(15,0))

def startApplication():
    window.mainloop()

# Run the application
startApplication()
