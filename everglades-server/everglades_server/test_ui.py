import sys
import tkinter as tk
from CreateJsonData import *

thismodule = sys.modules[__name__]

squad1= []
squad2= []
squad3= []
squad4= []
squad5= []
squad6= []
squad7= []
squad8= []
squad9= []
squad10= []
squad11= []
squad12= []

def helloWorld():
    lbl_result["text"] = f"Hello World"

def clearSquad():
    sel_squad_list['text'] = ""

def loadSquad():
    line0 = "if len(squad" + sel_squad_dd["text"] + ") == 0:\n   sel_squad_list['text'] = ''\n"
    line1 = "for i, x in enumerate(squad" + sel_squad_dd["text"] + "):\n"
    line2 = "   if i == 0:\n"
    line3 = "      sel_squad_list['text'] = x\n"
    line4 = "   else:\n"
    line5 = "      sel_squad_list['text'] += ', ' + x"
    exec(line0 + line1 + line2 + line3 + line4 + line5)

def saveSquad():
    currentSquad = sel_squad_list['text'].split(", ")
    arrayName = "squad" + sel_squad_dd["text"]
    setattr(thismodule, arrayName, currentSquad[:])

def addUnit():
    unitName = ent_unitname.get()
    if unitName == "":
        return
    
    textofnum = ent_unitnum.get()
    if int(textofnum)>= 0 or int(textofnum) < 0:
        number = int(textofnum)
        for i in range(number):
            if len(sel_squad_list['text']) == 0:
                sel_squad_list['text'] = unitName
            else:
                sel_squad_list['text'] += ", " + unitName

def generateJSON():
    loadout = [squad1, squad2, squad3, squad4, squad5, squad6, squad7, squad8, squad9, squad10, squad11, squad12]
    playerIdentifier = int(ent_playnum.get())
    GenerateJsonFileLoadout(loadout, playerIdentifier)

# Set-up the window and frames
window = tk.Tk()
window.title("EVERGLADES Function Tester")
window.resizable(width=True, height=True)
top_frame = tk.Frame(master=window)
top_frame.grid(row=0, column=0, padx=10, pady=10)
mid_frame = tk.Frame(master=window)
mid_frame.grid(row=1, column=0, padx=10, pady=10)
bot_frame = tk.Frame(master=window)
bot_frame.grid(row=2, column=0, padx=10, pady=10)
foot_frame = tk.Frame(master=window)
foot_frame.grid(row=3, column=0, padx=10, pady=10)

# Create the test Button and result display Label
btn_test = tk.Button(
    master=top_frame,
    text="Test Button",
    command = helloWorld
)
lbl_result = tk.Label(master=top_frame, text="Placeholder ")

# Set-up the layout using the .grid() geometry manager
#btn_test.grid(row=0, column=0, padx=10, pady=10)
#lbl_result.grid(row=0, column=1, padx=10)

# Create dropdown menu
ddtext = tk.StringVar()
ddtext.set("1")
sel_squad_lbl = tk.Label(master=top_frame, text="Select Squad: ")
sel_squad_dd = tk.OptionMenu(top_frame, ddtext, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")

# Create the load/ save buttons
btn_load = tk.Button(
    master=top_frame,
    text="Load Squad",
    command = loadSquad
)

btn_save = tk.Button(
    master=top_frame,
    text="Save Squad",
    command = saveSquad
)

btn_clear = tk.Button(
    master=top_frame,
    text="Clear Current",
    command = clearSquad
)

# Layout the dropdown and label in frm_entry
sel_squad_lbl.grid(row=1, column=0, sticky="w")
sel_squad_dd.grid(row=1, column=1, sticky="e")
btn_load.grid(row=1, column=2, sticky = "e")
btn_save.grid(row=1, column=3, sticky = "w")
btn_clear.grid(row=1, column=4, sticky = "w")

## Text that says "Current Squad:"
sel_squad_text = tk.Label(master=mid_frame, text="Current Squad: ")
sel_squad_list = tk.Label(master=mid_frame, text="")

# Layout the dropdown and label
sel_squad_text.grid(row=0, column=0, sticky="w")
sel_squad_list.grid(row=0, column=1, sticky="e")

# Create the add button, unit name and number entry / labels
btn_add = tk.Button(
    master=bot_frame,
    text="Add Unit",
    command = addUnit
)
unitname_lbl = tk.Label(master=bot_frame, text="Unit Name: ")
ent_unitname = tk.Entry(master=bot_frame, width=20)
unitnum_lbl = tk.Label(master=bot_frame, text="Number: ")
ent_unitnum = tk.Entry(master=bot_frame, width=3)

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
    command = generateJSON
)
playnum_lbl = tk.Label(master=foot_frame, text="Player Number: ")
ent_playnum = tk.Entry(master=foot_frame, width=1)

# Layout
playnum_lbl.grid(row=0, column=0, sticky="w")
ent_playnum.grid(row=0, column=1, sticky="e")
btn_gen.grid(row=0, column=2, sticky="e")

# Run the application
window.mainloop()
