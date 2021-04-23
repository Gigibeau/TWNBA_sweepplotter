from TWNBA_sweepplotter import Data
from tkinter import *  # NOQA
from tkinter import ttk
from tkinter import filedialog

root = Tk()

button_open = Button(root, text="\U0001F4C2", command=lambda: open_files())
button_open.grid(row=0, column=0)

def open_files():
    file_name = filedialog.askopenfilename(
        initialdir="/Users/beau/Coding", title="Open File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    data = Data(file_name)

    text.delete('1.0', END)
    text.insert("end", "elec: " + str(data.elec) + "\n"
                "rho: " + str(data.rho) + "\n"
                "sweep: " + str(data.sweep) + "\n"
                "steps: " + str(data.steps) + "\n"
                "runs: " + str(data.runs) + "\n")
    text.see("end")

# Placement of the log
text = Text(root, width=20, height=10)
text.grid(row=2, column=0, columnspan=10)


root.mainloop()