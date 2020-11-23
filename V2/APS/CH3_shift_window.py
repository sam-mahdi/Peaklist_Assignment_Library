from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os
import functools
import tkinter.scrolledtext as st
from tkinter import ttk

class ReadOnlyText(st.ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state=tk.DISABLED)

        self.insert = self._unlock(super().insert)
        self.delete = self._unlock(super().delete)

    def _unlock(self, f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            self.config(state=tk.NORMAL)
            r = f(*args, **kwargs)
            self.config(state=tk.DISABLED)
            return r
        return wrap

CH3shift_file=()
ch3_shift_directory=()
text_area=()

class CH3Shift(object):
    def __init__(self, root):
        global text_area
        self.CH3_shift_window = Toplevel(root)
        self.CH3_shift_window.title("CH3 Shift")
        self.CH3_shift_window.geometry("700x600")
        tk.Label(self.CH3_shift_window, text="CH3Shift File").grid(row=0)
        tk.Label(self.CH3_shift_window, text="Carbon").grid(row=1)
        tk.Label(self.CH3_shift_window, text="Hydrogen").grid(row=2)
        tk.Label(self.CH3_shift_window, text="Carbon Adjustment (leave blank if none needed)").grid(row=3)
        tk.Label(self.CH3_shift_window, text="Hydrogen Adjustment (leave blank if none needed)").grid(row=4)
        tk.Label(self.CH3_shift_window, text="Values to Display (RMSD ordered low to high)").grid(row=5)

        self.CH3_shift_file_input = tk.Entry(self.CH3_shift_window)
        self.carbon_input = tk.Entry(self.CH3_shift_window)
        self.hydrogen_input = tk.Entry(self.CH3_shift_window)
        self.carbon_adjustment_input = tk.Entry(self.CH3_shift_window)
        self.hydrogen_adjustment_input = tk.Entry(self.CH3_shift_window)
        self.display_values_input = tk.Entry(self.CH3_shift_window)
        self.CH3_shift_file_input.grid(row=0, column=1)
        self.carbon_input.grid(row=1, column=1)
        self.hydrogen_input.grid(row=2, column=1)
        self.carbon_adjustment_input.grid(row=3, column=1)
        self.hydrogen_adjustment_input.grid(row=4, column=1)
        self.display_values_input.grid(row=5, column=1)

        self.CH3_shift_window.btn = tk.Button(self.CH3_shift_window,text='browse',command=self.input_file)
        self.CH3_shift_window.btn.grid(row=0,column=2)
        self.CH3_shift_window.btn = tk.Button(self.CH3_shift_window,text='run',command=self.CH3_shift_RMSD)
        self.CH3_shift_window.btn.grid(row=6,column=1)
        self.CH3_shift_window.btn = tk.Button(self.CH3_shift_window,text='exit',command=self.CH3_shift_window.destroy)
        self.CH3_shift_window.btn.grid(row=7,column=1)
        self.CH3_shift_window.btn = tk.Button(self.CH3_shift_window,text='clear',command=self.clear)
        self.CH3_shift_window.btn.grid(row=6,column=2)

        ttk.Label(self.CH3_shift_window,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 15)

        text_area = ReadOnlyText(self.CH3_shift_window,width = 50,height = 10,font = ("Times New Roman",12))

        text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)

    def input_file(self):
        fullpath = filedialog.askopenfilename(parent=self.CH3_shift_window, title='Choose a file')
        global CH3shift_file
        global ch3_shift_directory
        ch3_shift_directory=os.path.dirname(fullpath)
        CH3shift_file= os.path.basename(fullpath)
        label3=Label(self.CH3_shift_window,text=fullpath).grid(row=0,column=1)
    def clear(self):
        text_area.delete(1.0,END)

    def CH3_shift_RMSD(self):
        if self.carbon_input.get() == '' or self.hydrogen_input.get() == '':
            self.text_area.insert(tk.INSERT,f'Carbon or Hydrogen value empty, please add value')
        if self.display_values_input.get() == '':
            self.text_area.insert(tk.INSERT,f'Please enter a value for displayed values')
        else:
            if self.carbon_adjustment_input.get() == '':
                carbon_adjustment=0
            else:
                carbon_adjustment=float(self.carbon_adjustment_input.get())
            if self.hydrogen_adjustment_input.get() == '':
                hydrogen_adjustment=0
            else:
                hydrogen_adjustment=float(self.hydrogen_adjustment_input.get())
            carbon=float(self.carbon_input.get())
            hydrogen=float(self.hydrogen_input.get())
            displayed_values=int(self.display_values_input.get())
            from ch3_shift import rmsd_calc
            rmsd_calc(carbon,hydrogen,CH3shift_file,ch3_shift_directory,carbon_adjustment,hydrogen_adjustment,displayed_values,text_area)
