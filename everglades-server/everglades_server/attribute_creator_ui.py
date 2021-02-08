import sys
import tkinter as tk
from CreateJsonData import *

thismodule = sys.modules[__name__]

unitList = []

def loadFromFile():
    information = LoadUnitAttributeFile()
    ##LoadUnitAttributeFile() defined in Ethan's code
    ##The line below is the debug data I used to make sure the functions worked as intended
    ##information = [["a", "b", "c"],["eff1", "eff2", "eff3"],["desc1","desc2","desc3"],[1.1,2,3],[0,1,0],[1,2,3],[1,2,3]]
    for item in information:
        unitList.append(item)
    refreshDropDown()


def generateFile():
    GenerateUnitAttributeFile(unitList[0],unitList[1],unitList[2],unitList[3],unitList[4],unitList[5],unitList[6])

def refreshDropDown():
    ## Remove current dropdown options
    ddtext.set('1')
    sel_attr_dd['menu'].delete(0, 'end')

    ## Add new options
    newchoices = [0]*len(unitList[0])
    for num in range(len(unitList[0])):
        newchoices[num] = str(num+1)
    for choice in newchoices:
        sel_attr_dd['menu'].add_command(label=choice, command=tk._setit(ddtext, choice))

def saveToFile():
    GenerateUnitAttributeFile(unitList[0], unitList[1], unitList[2], unitList[3], unitList[4], unitList[5], unitList[6])

def loadAttribute():
    attrNum = int(sel_attr_dd['text'])-1
    nameVar.set(unitList[0][attrNum])
    effVar.set(unitList[1][attrNum])
    ent_unitnum.delete(1.0, tk.END)
    ent_unitnum.insert(tk.END, unitList[2][attrNum])
    modVar.set(str(unitList[3][attrNum]))
    multVar.set(str(unitList[4][attrNum]))
    priorityVar.set(str(unitList[5][attrNum]))
    costVar.set(str(unitList[6][attrNum]))

def saveAttribute():
    attrNum = int(sel_attr_dd['text'])-1
    unitList[0][attrNum] = nameVar.get()
    unitList[1][attrNum] = effVar.get()
    unitList[2][attrNum] = ent_unitnum.get("1.0",tk.END)
    unitList[3][attrNum] = float(modVar.get())
    unitList[4][attrNum] = int(multVar.get())
    unitList[5][attrNum] = int(priorityVar.get())
    unitList[6][attrNum] = int(costVar.get())

def deleteAttribute():
    ## Get current & end of data index
    attrNum = int(sel_attr_dd['text'])-1
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
    ## Data that populates new attribute
    sampleData = ([['Name'],['Effect'],['Description'],['0'],['0'],['0'],['0']])

    ## If no data exists
    if sel_attr_dd['text'] == '':
        for val in range(0,7):
            unitList.append(sampleData[val])
        sel_attr_dd['menu'].add_command(label=str(1), command=tk._setit(ddtext, str(1)))
        ddtext.set('1')
        return

    ## Else (data exists)
    newFinal = len(unitList[0])+1
    for val in range(0,len(unitList)):
        unitList[val].append(sampleData[val])
    sel_attr_dd['menu'].add_command(label=str(newFinal), command=tk._setit(ddtext, str(newFinal)))

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Function Tester")
window.resizable(width=True, height=True)
left_frame = tk.Frame(master=window)
left_frame.grid(row=0, column=0, padx=10, pady=10)
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=0, column=1, padx=10, pady=10)
right_frame = tk.Frame(master=window)
right_frame.grid(row=0, column=2, padx=10, pady=10)
foot_frame = tk.Frame(master=window)
foot_frame.grid(row=0, column=3, padx=10, pady=10)

# Left column
nameVar = tk.StringVar()
unitname_lbl = tk.Label(master=left_frame, text="Name: ")
unitname_lbl.grid(row=0, column=0, sticky="w")
ent_unitname = tk.Entry(master=left_frame, width=25, textvariable = nameVar)
ent_unitname.grid(row=1, column=0, sticky="w")

unitnum_lbl = tk.Label(master=left_frame, text="Description: ")
unitnum_lbl.grid(row=2, column=0, sticky="w")
ent_unitnum = tk.Text(master=left_frame, width=30)
ent_unitnum.grid(row=3, column=0, sticky="w")

effVar = tk.StringVar()
uniteff_lbl = tk.Label(master=left_frame, text="Effect: ")
uniteff_lbl.grid(row=4, column=0, sticky="w")
ent_uniteff = tk.Entry(master=left_frame, width=30, textvariable = effVar)
ent_uniteff.grid(row=5, column=0, sticky="w")

modVar = tk.StringVar()
modifier_lbl = tk.Label(master=left_frame, text="Modifier: ")
modifier_lbl.grid(row=6, column=0, sticky="w")
ent_unitmod = tk.Entry(master=left_frame, width=30, textvariable = modVar)
ent_unitmod.grid(row=7, column=0, sticky="w")

multVar = tk.StringVar()
isMult_lbl = tk.Label(master=left_frame, text="isMult: ")
isMult_lbl.grid(row=6, column=1, sticky="w")
ent_unitmult = tk.Entry(master=left_frame, width=2, textvariable = multVar)
ent_unitmult.grid(row=7, column=1, sticky="w")


# Middle column
btn_load = tk.Button(
    master=mid_frame,
    text="Load From File",
    command = loadFromFile
)
btn_load.grid(row=0, column=0)
btn_make = tk.Button(
    master=mid_frame,
    text="Generate File",
    command = generateFile
)
btn_make.grid(row=0, column=1)

priorityVar = tk.IntVar()
unitprio_lbl = tk.Label(master=mid_frame, text="Priority: ")
unitprio_lbl.grid(row=1, column=0, sticky="sw", pady = (20,0))
ent_unitprio = tk.Entry(master=mid_frame, width=30, textvariable = priorityVar)
ent_unitprio.grid(row=2, column=0, sticky="w")
costVar = tk.IntVar()
unitcost_lbl = tk.Label(master=mid_frame, text="Cost: ")
unitcost_lbl.grid(row=1, column=1, sticky="sw")
ent_unitcost = tk.Entry(master=mid_frame, width=30, textvariable = costVar)
ent_unitcost.grid(row=2, column=1, sticky="w")


# Right column
# Create dropdown menu
ddtext = tk.StringVar()
ddtext.set("")
sel_attr_lbl = tk.Label(master=right_frame, text="Select Attribute: ")
sel_attr_lbl.grid(row=0, column=0, sticky="w")
sel_attr_dd = tk.OptionMenu(right_frame, ddtext, "")
sel_attr_dd.grid(row=0, column=1)
btn_new = tk.Button(
    master=right_frame,
    text="Load Selected Attribute",
    command = loadAttribute
)
btn_new.grid(row=0, column=2)
btn_save = tk.Button(
    master=right_frame,
    text="Save To Selected Attribute",
    command = saveAttribute
)
btn_save.grid(row=1, column=2)

btn_dlt = tk.Button(
    master=right_frame,
    text="Delete Selected",
    command = deleteAttribute
)
btn_dlt.grid(row=1, column=0)
btn_new = tk.Button(
    master=right_frame,
    text="New Attribute",
    command = newAttribute
)
btn_new.grid(row=1, column=1)

"""
## Text that says "Current Attribute:"
sel_Attribute_text = tk.Label(master=mid_frame, text="Current Attribute: ")
sel_Attribute_list = tk.Label(master=mid_frame, text="")

# Layout the dropdown and label
sel_Attribute_text.grid(row=0, column=0, sticky="w")
sel_Attribute_list.grid(row=0, column=1, sticky="e")

# Create the add button, unit name and number entry / labels
btn_add = tk.Button(
    master=right_frame,
    text="Add Unit",
    command = addUnit
)
unitname_lbl = tk.Label(master=right_frame, text="Unit Name: ")
ent_unitname = tk.Entry(master=right_frame, width=20)
unitnum_lbl = tk.Label(master=right_frame, text="Number: ")
ent_unitnum = tk.Entry(master=right_frame, width=3)

# Layout
unitname_lbl.grid(row=0, column=0, sticky="w")
ent_unitname.grid(row=0, column=1, sticky="e")
unitnum_lbl.grid(row=0, column=2, sticky="e", padx=10)
ent_unitnum.grid(row=0, column=3, sticky="w")
btn_add.grid(row=0, column=4, sticky="e", padx=10)

# Create bottom row of features
btn_gen = tk.Button(
    master=foot_frame,
    text="Generate JSON",
    command = addUnit
)
playnum_lbl = tk.Label(master=foot_frame, text="Player Number: ")
ent_playnum = tk.Entry(master=foot_frame, width=1)

# Layout
playnum_lbl.grid(row=0, column=0, sticky="w")
ent_playnum.grid(row=0, column=1, sticky="e")
btn_gen.grid(row=0, column=2, sticky="e")
"""


def startApplication():
    window.mainloop()


# Run the application
startApplication()