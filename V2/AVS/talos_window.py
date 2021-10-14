import re
from pymol import cmd, stored, math
import pymol
import os
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os
import os.path
import functools
import tkinter.scrolledtext as st
from tkinter import ttk

pdb_file=()
pdb_directory=()
NMRSTAR_file=()
NMRSTAR_directory=()
startaa=()
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



class TalosrunWindow(object):
    def __init__(self, root):
        global text_area
        self.talos_window = Toplevel(root)
        self.talos_window.title("TALOS")
        self.talos_window.geometry("600x600")
        tk.Label(self.talos_window, text="PDB File").grid(row=0)
        tk.Label(self.talos_window, text="NMRSTAR File").grid(row=1)
        tk.Label(self.talos_window, text="Start amino acid for PDB mapping").grid(row=2)
        pdb_file_line = tk.Entry(self.talos_window).grid(row=0, column=1)
        NMRSTAR_file_line=tk.Entry(self.talos_window).grid(row=1, column=1)
        self.start_aa = tk.Entry(self.talos_window)
        self.start_aa.grid(row=2, column=1)
        self.talos_window.btn = tk.Button(self.talos_window,text='browse',command=self.input_pdb_file)
        self.talos_window.btn.grid(row=0,column=2)
        self.talos_window.btn = tk.Button(self.talos_window,text='browse',command=self.input_NMRSTAR_file)
        self.talos_window.btn.grid(row=1,column=2)
        self.talos_window.btn = tk.Button(self.talos_window,text='Enter',command=self.start_aa)
        self.talos_window.btn.grid(row=2,column=2)
        self.talos_window.btn = tk.Button(self.talos_window,text='Run TALOS',command=self.runtalos)
        self.talos_window.btn.grid(row=4,column=1)
        self.talos_window.btn = tk.Button(self.talos_window,text='Display TALOS',command=self.displaytalos)
        self.talos_window.btn.grid(row=5,column=1)
        self.talos_window.btn = tk.Button(self.talos_window,text='Map Seconday Structure Prediction',command=self.mapSS)
        self.talos_window.btn.grid(row=4,column=2)
        self.talos_window.btn = tk.Button(self.talos_window,text='Map S2 Prediction',command=self.mapS2)
        self.talos_window.btn.grid(row=5,column=2)

        ttk.Label(self.talos_window,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 6)

        text_area = ReadOnlyText(self.talos_window,height=10,width=50,font = ("Times New Roman",12))
        text_area.grid(column=0,columnspan=3,sticky=W)

    def input_pdb_file(self):
        fullpath = filedialog.askopenfilename(parent=self.talos_window, title='Choose a file')
        global pdb_file
        global pdb_directory
        pdb_directory=os.path.dirname(fullpath)
        pdb_file= os.path.basename(fullpath)
        if pdb_file == '' or pdb_directory == '':
            pdb_file=()
            pdb_directory=()
        label4=Label(self.talos_window,text=fullpath).grid(row=0,column=1)

    def input_NMRSTAR_file(self):
        fullpath = filedialog.askopenfilename(parent=self.talos_window, title='Choose a file')
        global NMRSTAR_file
        global NMRSTAR_directory
        NMRSTAR_directory=os.path.dirname(fullpath)
        NMRSTAR_file= os.path.basename(fullpath)
        if NMRSTAR_file == '' or NMRSTAR_directory == '':
            NMRSTAR_file=()
            NMRSTAR_directory=()
        label4=Label(self.talos_window,text=fullpath).grid(row=0,column=1)

    def start_aa(self):
        start_aa=self.start_aa.get()
        global startaa
        startaa=float(start_aa)
        text_area.insert(tk.INSERT,f'Start value set: {startaa} \n')

    def runtalos(self):
        text_area.insert(tk.INSERT,'Starting Talos\n')
        if NMRSTAR_file == ():
            text_area.insert(tk.INSERT,'Please upload an NMRSTAR file\n')
        else:
            os.chdir(NMRSTAR_directory)
            os.system(f'talos+ -in {NMRSTAR_file}')
            text_area.insert(tk.INSERT,'Talos Completed\n')

    def displaytalos(self):
        if os.path.isfile('pred.tab') == False:
            text_area.insert(tk.INSERT,'No Pred.tab file found, please run Talos first\n')
        else:
            rama+ -in 'pred.tab'

    def mapSS(self):
        if pdb_file == ():
            text_area.insert(tk.INSERT,'Please Upload a PDB File\n')
        if os.path.isfile('predSS.tab') == False:
            text_area.insert(tk.INSERT,'No PredSS.tab file found, please run Talos first\n')
        else:
            ss_dict={'L':0,'H':2,'E':1,'X':0}
            ss_only=[]
            pymol.finish_launching()
            cmd.load(pdb_file)
            mol=pdb_file[0:-4]
        	with open('predSS.tab') as ss_file:
        		for lines in ss_file:
                    searcher=re.search('^\d+',lines.strip())
                    if searcher != None:
        				if int(lines.strip().split()[0]) < int(startaa):
        					continue
        				ss_only.append(ss_dict[lines.strip().split()[8]])
        	obj=cmd.get_object_list(mol)
        	cmd.alter(mol,"b=-1.0")
        	counter=int(startaa)
        	bfacts=[]
        	for line in ss_only:
        		bfact=float(line)
        		bfacts.append(bfact)
        		cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
        		counter=counter+1
        	if visual=="Y":
        		cmd.cartoon("automatic",mol)
        		cmd.spectrum("b","grey blue red", "%s and n. CA " %mol)
        		cmd.recolor()

    def mapS2(self):
        if pdb_file == ():
            text_area.insert(tk.INSERT,'Please Upload a PDB File\n')
        if os.path.isfile('predSS.tab') == False:
            text_area.insert(tk.INSERT,'No PredSS.tab file found, please run Talos first\n')
        else:
            s2_only=[]
            cmd.load(pdb_file)
            pymol.finish_launching()
            mol=pdb_file[0:-4]
        	with open('predS2.tab') as s2_file:
        		for lines in s2_file:
                    searcher=re.search('\d+\.\d{3}',lines)
                    if searcher != None:
        				if int(lines.strip().split()[0]) < int(startaa):
        					continue
        				s2_only.append(searcher.group(0))
        	obj=cmd.get_object_list(mol)
        	cmd.alter(mol,"b=-1.0")
        	counter=int(startaa)
        	bfacts=[]
        	for line in s2_only:
        		bfact=((1/(float(line)))-float(line))/1.5
        		bfacts.append(bfact)
        		cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
        		counter=counter+1
        	if visual=="Y":
        		cmd.show_as("cartoon",mol)
        		cmd.cartoon("putty", mol)
        		cmd.set("cartoon_putty_scale_min", min(bfacts),obj)
        		cmd.set("cartoon_putty_scale_max", max(bfacts),obj)
        		cmd.set("cartoon_putty_transform", 7,obj)
        		cmd.set("cartoon_putty_radius", max(bfacts),obj)
        		cmd.spectrum("b","white red", "%s and n. CA " %mol)
        		cmd.ramp_new("color_bar", obj, [min(bfacts), max(bfacts)],["white","red"])
        		cmd.recolor()
