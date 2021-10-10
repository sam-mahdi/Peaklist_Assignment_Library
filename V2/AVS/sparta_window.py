import re
#from pymol import cmd, stored, math
#import pymol
import os
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os
import functools
import tkinter.scrolledtext as st
from tkinter import ttk


pdb_file=()
pdb_directory=()
chain=()
start=()
end=()
use_entire_pdb_flag = IntVar()
Add_hydrogens_flag = IntVar()
Run_spart_flag = IntVar()
text_area=()

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



class SpartaGenerationWindow(object):
    def __init__(self, root):
        global text_area
        self.sparta_window = Toplevel(root)
        self.sparta_window.title("Sparta Generator")
        self.sparta_window.geometry("600x600")
        tk.Label(self.sparta_window, text="PDB File").grid(row=0)
        tk.Label(self.sparta_window, text="Start").grid(row=1)
        tk.Label(self.sparta_window, text="End").grid(row=2)
        tk.Label(self.sparta_window, text="Chain").grid(row=3)
        pdb_file_line = tk.Entry(self.sparta_window).grid(row=0, column=1)
        self.start_pdb = tk.Entry(self.sparta_window)
        self.start_pdb.grid(row=1, column=1)
        self.end_pdb = tk.Entry(self.sparta_window)
        self.end_pdb.grid(row=2, column=1)
        self.chain_pdb = tk.Entry(self.sparta_window)
        self.chain_pdb.grid(row=3, column=1)
        self.sparta_window.btn = tk.Button(self.sparta_window,text='browse',command=self.input_pdb_file)
        self.sparta_window.btn.grid(row=0,column=2)
        self.sparta_window.btn = tk.Button(self.sparta_window,text='Enter',command=self.start_of_pdb)
        self.sparta_window.btn.grid(row=1,column=2)
        self.sparta_window.btn = tk.Button(self.sparta_window,text='Enter',command=self.end_of_pdb)
        self.sparta_window.btn.grid(row=2,column=2)
        self.sparta_window.btn = tk.Button(self.sparta_window,text='Enter',command=self.chain_of_pdb)
        self.sparta_window.btn.grid(row=3,column=2)
        self.sparta_window.btn = tk.Button(self.sparta_window,text='Run',command=self.run)
        self.sparta_window.btn.grid(row=5,column=1)
        tk.Checkbutton(self.sparta_window, text="Use entire PDB Structure", variable=use_entire_pdb_flag).grid(row=4,column=0,stick=W)
        tk.Checkbutton(self.sparta_window, text="Add Hydrogens", variable=Add_hydrogens_flag).grid(row=4,column=1,stick=W)
        tk.Checkbutton(self.sparta_window, text="Run Sparta", variable=Run_spart_flag).grid(row=4,column=2,stick=W)

        ttk.Label(self.sparta_window,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 6)

        text_area = ReadOnlyText(self.sparta_window,height=10,width=50,font = ("Times New Roman",12))
        text_area.grid(column=0,columnspan=3,sticky=W)

    def input_pdb_file(self):
        fullpath = filedialog.askopenfilename(parent=self.sparta_window, title='Choose a file')
        global pdb_file
        global pdb_directory
        pdb_directory=os.path.dirname(fullpath)
        pdb_file= os.path.basename(fullpath)
        if pdb_file == '' or pdb_directory == '':
            pdb_file=()
            pdb_directory=()
        label4=Label(self.sparta_window,text=fullpath).grid(row=0,column=1)

    def start_of_pdb(self):
        start_input=self.start_pdb.get()
        global start
        start=float(start_input)
        text_area.insert(tk.INSERT,f'Start value set: {start_input} \n')

    def end_of_pdb(self):
        end_input=self.end_pdb.get()
        global end
        end=float(end_input)
        text_area.insert(tk.INSERT,f'End value set: {end_input} \n')

    def chain_of_pdb(self):
        chain_input=self.chain_pdb.get()
        global chain
        chain=chain_input
        text_area.insert(tk.INSERT,f'Chain value set: {chain_input} \n')

    def run(self):
        if pdb_file == ():
            text_area.insert(tk.INSERT,'Please Upload a PDB File\n')
            return
        import sparta_file_maker as sfm
        text_area.insert(tk.INSERT,'Program Start\n')
        os.chdir(pdb_directory)
        if use_entire_pdb_flag.get() == 0:
            if start == () or end == () or chain == ():
                text_area.insert(tk.INSERT,'Please enter a start and end value, and specify which chain\n')
                return
            text_area.insert(tk.INSERT,'Modifying PDB File\n')
            text_area.update_idletasks()
            sfm.write_new_pdb(pdb_file,start,end,chain)
        if Add_hydrogens_flag.get() != 0:
            text_area.insert(tk.INSERT,'Adding Hydrogens\n')
            text_area.update_idletasks()
            if use_entire_pdb_flag.get() == 0:
                sfm.add_hydrogen('modified_'+pdb_file)
            else:
                sfm.add_hydrogen(pdb_file)
        if Run_spart_flag.get() != 0:
            text_area.insert(tk.INSERT,'Running Sparta\n')
            text_area.update_idletasks()
            if use_entire_pdb_flag.get() == 0 and Add_hydrogens_flag.get() != 0:
                 sfm.run_sparta('modified_'+pdb_file[0:-4]+'_hydrogens_added.pdb')
            elif use_entire_pdb_flag.get() != 0 and Add_hydrogens_flag.get() != 0:
                sfm.run_sparta(pdb_file[0:-4]+'_hydrogens_added.pdb')
            elif use_entire_pdb_flag.get() != 0 and Add_hydrogens_flag.get() == 0:
                sfm.run_sparta(pdb_file)
            elif use_entire_pdb_flag.get() == 0 and Add_hydrogens_flag.get() == 0:
                sfm.run_sparta('modified_'+pdb_file)
            else:
                pass
        text_area.insert(tk.INSERT,'Program Complete\n')
