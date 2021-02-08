import sys
import tkinter as tk
from CreateJsonData import *

thismodule = sys.modules[__name__]

unitList = []
attrList = []

def loadFromFile():
    information = LoadAttributesBasedUnitFile(1)
    dataList = LoadUnitAttributeFile()
    ##LoadAttributesBasedUnitFile() defined in Ethan's code
    ##The line below is the debug data I used to make sure the functions worked as intended
    ##information = [["a", "b", "c"],[["name1", "name2", "name3"],["name1", "name3"],["name2"]]]
    ##dataList = [["name1", "name2", "name3"],["eff1", "eff2", "eff3"],["desc1","desc2","desc3"],[1.1,2,3],[0,1,0],[1,2,3],[1,2,3]]

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

def generateFile():
    GenerateAttributeBasedUnitsFile(unitList[0], unitList[1])
        
def refreshDropDown():
    ## Remove current dropdown options
    sel_attr_dd['menu'].delete(0, 'end')

    ## Add new options
    print(unitList)
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

def createAttrList():
    ## Clear list of attributes and repopulate
    list_attr.delete(0, tk.END)
    for item in attrList[0]:
        list_attr.insert(tk.END, item)

def updateCost():
    sum = 0
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    for usedAttr in unitList[1][attrNum]:
        attrIndex = attrList[0].index(usedAttr)
        sum += attrList[6][attrIndex]
    costVar.set(sum)

def saveToFile():
    GenerateUnitAttributeFile(unitList[0], unitList[1], unitList[2], unitList[3], unitList[4], unitList[5], unitList[6])

def loadUnit():
    ## Exception if text is blank
    if ddtext.get() == " ":
        curr_attr.delete(0, tk.END)
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

def addAttribute():
    if ddtext.get() == " ":
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
    if ddtext.get() == " ":
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
                print(str(index))
                unitList[1][attrNum][index] = unitList[1][attrNum][index+1]
        unitList[1][attrNum].pop()
        ## Update list of unit's attributes
        curr_attr.delete(toRemove)
        ## Update cost
        updateCost()

def newUnit():
    newName = nameVar.get()
    print(str(unitList))
    if len(unitList) == 0:
        temp = [[newName],[[]]]
        for item in temp:
            unitList.append(item)
    else:
        unitList[0].append(newName)
        unitList[1].append([])
    print(str(unitList))
    sel_attr_dd['menu'].add_command(label=newName, command=tk._setit(ddtext, newName))
    ddtext.set(newName)
    loadUnit()
    

def deleteAttribute():
    if ddtext.get() == " ":
        return
    ## Get current & end of data index
    attrNum = sel_attr_dd['menu'].index(ddtext.get())
    final = len(unitList[0])-1
    ## Move all data above deletion down an index
    for num in range(attrNum, final):
        for val in range(0,len(unitList)):
            unitList[val][num] = unitList[val][num+1]
    ## Pop duplicated final data
    unitList[0].pop()
    unitList[1].pop()
    if len(unitList[0]) == 0:
        unitList.pop()
        unitList.pop()
    ## Update dropdown
    refreshDropDown()

def updateDescription(*args):
    ## If a selection is currently made
    if list_attr.curselection() != ():
        ## Get the name of the attribute
        toDesc = list_attr.curselection()[0]
        ## Delete and repopulate description text
        ent_unitnum.delete(1.0, tk.END)
        ent_unitnum.insert(tk.END, attrList[2][toDesc])
    

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
unitname_lbl = tk.Label(master=left_frame, text="Name of New Unit: ")
unitname_lbl.grid(row=0, column=0, sticky="w")
ent_unitname = tk.Entry(master=left_frame, width=25, textvariable = nameVar)
ent_unitname.grid(row=1, column=0, sticky="w")

btn_new = tk.Button(
    master=left_frame,
    text="Add New Unit",
    command = newUnit
)
btn_new.grid(row=2, column=0, pady=(0,30))

dd_frame = tk.Frame(master=left_frame)
dd_frame.grid(row=3, column=0, sticky="w")
ddtext = tk.StringVar()
ddtext.set("")
def dd_callback(*args):
    loadUnit()
ddtext.trace("w", dd_callback)
sel_attr_lbl = tk.Label(master=dd_frame, text="Select Unit: ")
sel_attr_lbl.grid(row=0, column=0, sticky="e")
sel_attr_dd = tk.OptionMenu(dd_frame, ddtext, " ")
sel_attr_dd.grid(row=0, column=1, sticky="e")

btn_dlt = tk.Button(
    master=dd_frame,
    text="Delete Selected Unit",
    command = deleteAttribute
)
btn_dlt.grid(row=1, column=0, pady=(0,30))

btn_load = tk.Button(
    master=dd_frame,
    text="Load From File",
    command = loadFromFile
)
btn_load.grid(row=3, column=0)

btn_make = tk.Button(
    master=dd_frame,
    text="Save To File",
    command = generateFile
)
btn_make.grid(row=4, column=0)



# Middle column
top_frame = tk.Frame(master=mid_frame)
top_frame.grid(row=0, column=0, sticky="w")

curr_lbl = tk.Label(master=top_frame, text="Current Unit's Attributes: ")
curr_lbl.grid(row=0, column=0, sticky="w")
curr_attr = tk.Listbox(master=top_frame)
curr_attr.grid(row=1, column=0, sticky="w")

cost_frame = tk.Frame(master=top_frame)
cost_frame.grid(row=1, column=1, sticky="w")

list_lbl = tk.Label(master=top_frame, text="List of Attributes: ")
list_lbl.grid(row=0, column=2, sticky="w")
list_attr = tk.Listbox(master=top_frame)
list_attr.grid(row=1, column=2, sticky="w")
list_attr.bind('<<ListboxSelect>>', updateDescription)

btn_add = tk.Button(
    master=cost_frame,
    text="Add Selected Attribute",
    command = addAttribute
)
btn_add.grid(row=0, column=0)

costVar = tk.IntVar()
costVar.set("0")
cost_lbl = tk.Label(master=cost_frame, text="Current Cost of Attributes: ")
cost_lbl.grid(row=1, column=0)
cost_num_lbl = tk.Label(master=cost_frame, textvariable = costVar)
cost_num_lbl.grid(row=2, column=0)

btn_rmv = tk.Button(
    master=cost_frame,
    text="Remove Selected Attribute",
    command = removeAttribute
)
btn_rmv.grid(row=3, column=0)

bot_frame = tk.Frame(master=mid_frame)
bot_frame.grid(row=1, column=0, sticky="w", pady = 10)
unitnum_lbl = tk.Label(master=bot_frame, text="Attribute Information: ")
unitnum_lbl.grid(row=1, column=0, sticky="w")
ent_unitnum = tk.Text(master=bot_frame, width = 35, height = 5)
ent_unitnum.grid(row=1, column=1, sticky="w")


# Run the application
window.mainloop()
