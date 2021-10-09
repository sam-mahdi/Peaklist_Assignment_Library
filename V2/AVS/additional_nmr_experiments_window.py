from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os


HNCOCA_file=()
HNCOCA_directory=()
CBCACONH_file=()
CBCACONH_directory=()
HNCACO_file=()
HNCACO_directory=()
HCCONH_file=()
HCCONH_directory=()

class nmr_experiment_window(object):
    def __init__(self, root):
        self.experimentswindow = Toplevel(root)
        self.experimentswindow.title("Additional NMR Experiments")
        self.experimentswindow.geometry("600x600")
        tk.Label(self.experimentswindow, text="HNCOCA  Peaklist").grid(row=0)
        tk.Label(self.experimentswindow, text="HNCACO  Peaklist").grid(row=1)
        tk.Label(self.experimentswindow, text="CBCACONH  Peaklist").grid(row=2)
        tk.Label(self.experimentswindow, text="HCCONH  Peaklist").grid(row=3)
        hncoca_line = tk.Entry(self.experimentswindow).grid(row=0, column=1)
        hncaco_line = tk.Entry(self.experimentswindow).grid(row=1, column=1)
        cbcaconh_line = tk.Entry(self.experimentswindow).grid(row=2, column=1)
        hcconh_line = tk.Entry(self.experimentswindow).grid(row=3, column=1)
        self.experimentswindow.btn = tk.Button(self.experimentswindow,text='browse',command=self.HNCOCA)
        self.experimentswindow.btn.grid(row=0,column=2)
        self.experimentswindow.btn = tk.Button(self.experimentswindow,text='browse',command=self.HNCACO)
        self.experimentswindow.btn.grid(row=1,column=2)
        self.experimentswindow.btn = tk.Button(self.experimentswindow,text='browse',command=self.CBCACONH)
        self.experimentswindow.btn.grid(row=2,column=2)
        self.experimentswindow.btn = tk.Button(self.experimentswindow,text='browse',command=self.HCCONH)
        self.experimentswindow.btn.grid(row=3,column=2)

    def HNCOCA(self):
        fullpath = filedialog.askopenfilename(parent=self.experimentswindow, title='Choose a file')
        global HNCOCA_file
        global HNCOCA_directory
        HNCOCA_directory=os.path.dirname(fullpath)
        HNCOCA_file= os.path.basename(fullpath)
        if HNCOCA_directory == '' or HNCOCA_file == '':
            HNCOCA_file=()
            HNCOCA_directory=()
        label7=Label(self.experimentswindow,text=fullpath).grid(row=0,column=1)

    def HNCACO(self):
        fullpath = filedialog.askopenfilename(parent=self.experimentswindow, title='Choose a file')
        global HNCACO_file
        global HNCACO_directory
        HNCACO_directory=os.path.dirname(fullpath)
        HNCACO_file= os.path.basename(fullpath)
        if HNCACO_file == '' or HNCACO_directory == '':
            HNCACO_file=()
            HNCACO_directory=()
        label7=Label(self.experimentswindow,text=fullpath).grid(row=1,column=1)

    def CBCACONH(self):
        fullpath = filedialog.askopenfilename(parent=self.experimentswindow, title='Choose a file')
        global CBCACONH_file
        global CBCACONH_directory
        CBCACONH_directory=os.path.dirname(fullpath)
        CBCACONH_file= os.path.basename(fullpath)
        if CBCACONH_file=='' or CBCACONH_directory == '':
            CBCACONH_file=()
            CBCACONH_directory=()
        label7=Label(self.experimentswindow,text=fullpath).grid(row=2,column=1)

    def HCCONH(self):
        fullpath = filedialog.askopenfilename(parent=self.experimentswindow, title='Choose a file')
        global HCCONH_file
        global HCCONH_directory
        HCCONH_directory=os.path.dirname(fullpath)
        HCCONH_file= os.path.basename(fullpath)
        if HCCONH_file =='' or HCCONH_directory == '':
            HCCONH_file=()
            HCCONH_directory=()
        label7=Label(self.experimentswindow,text=fullpath).grid(row=3,column=1)

def get_variables():
    return HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory
