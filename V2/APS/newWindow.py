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

save_file_peaklist=()
save_directory=()
list_of_shifts=[]

class newTopLevel(object):
    def __init__(self, root):
        self.newWindow = Toplevel(root)
        self.newWindow.title("Assignment Generator")
        self.newWindow.geometry("800x800")
        tk.Label(self.newWindow, text="Amide Nitrogen Chemical Shift (if no value, leave blank)").grid(row=0)
        tk.Label(self.newWindow, text="Alpha Hydrogen Chemical Shift (if no value, leave blank)").grid(row=1)
        tk.Label(self.newWindow, text="Alpha Hydrogen2 Chemical Shift (if no value, leave blank) \nIf you suspect you have a glycine, but have no HA2, simply type in 1000.00").grid(row=2)
        tk.Label(self.newWindow, text="Carbonyl Carbon Chemical Shift (if no value, leave blank)").grid(row=3)
        tk.Label(self.newWindow, text="Alpha Carbon Chemical Shift (if no value, leave blank)").grid(row=4)
        tk.Label(self.newWindow, text="Beta Carbon Chemical Shift (if no value, leave blank)").grid(row=5)
        tk.Label(self.newWindow, text="Amide Hydrogen Chemical Shift (if no value, leave blank)").grid(row=6)
        tk.Label(self.newWindow, text="Save file name (use browse)").grid(row=7)
        self.nitrogen_input = tk.Entry(self.newWindow)
        self.alpha_hydrogen_input = tk.Entry(self.newWindow)
        self.alpha_hydrogen2_input = tk.Entry(self.newWindow)
        self.carbon_input = tk.Entry(self.newWindow)
        self.alpha_carbon_input = tk.Entry(self.newWindow)
        self.beta_carbon_input = tk.Entry(self.newWindow)
        self.hydrogen_input = tk.Entry(self.newWindow)
        self.save_file_input = tk.Entry(self.newWindow).grid(row=7, column=1)

        self.nitrogen_input.grid(row=0, column=1)
        self.alpha_hydrogen_input.grid(row=1, column=1)
        self.alpha_hydrogen2_input.grid(row=2, column=1)
        self.carbon_input.grid(row=3, column=1)
        self.alpha_carbon_input.grid(row=4, column=1)
        self.beta_carbon_input.grid(row=5, column=1)
        self.hydrogen_input.grid(row=6, column=1)

        self.newWindow.btn = tk.Button(self.newWindow,text='enter values',command=self.generate_files)
        self.newWindow.btn.grid(row=8,column=0)
        self.newWindow.btn = tk.Button(self.newWindow,text='save/write file',command=self.write_file)
        self.newWindow.btn.grid(row=8,column=1)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.save_file)
        self.newWindow.btn.grid(row=7,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='quit',command=self.newWindow.destroy)
        self.newWindow.btn.grid(row=8,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Start over',command=self.start_over)
        self.newWindow.btn.grid(row=9,column=1)

        ttk.Label(self.newWindow,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 15)

        self.text_area = ReadOnlyText(self.newWindow,width = 50,height = 20,font = ("Times New Roman",12))

        self.text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)

    def save_file(self):
        myFormats = [('Text File','*.txt'),]
        fullpath = tk.filedialog.asksaveasfilename(parent=self.newWindow,filetypes=myFormats ,title="Save the file as...")
        global save_file_peaklist
        global save_directory
        save_directory=os.path.dirname(fullpath)
        save_file_peaklist=os.path.basename(fullpath)
        label8=Label(self.newWindow,text=fullpath).grid(row=7,column=1)

    def start_over(self):
        global list_of_shifts
        self.text_area.delete(1.0,END)
        list_of_shifts=[]

    def generate_files(self):
         global list_of_shifts
         nitrogen=self.nitrogen_input.get()
         alpha_hydrogen=self.alpha_hydrogen_input.get()
         alpha_hydrogen2=self.alpha_hydrogen2_input.get()
         carbon=self.carbon_input.get()
         alpha_carbon=self.alpha_carbon_input.get()
         beta_carbon=self.beta_carbon_input.get()
         hydrogen=self.hydrogen_input.get()
         self.text_area.insert(tk.INSERT,f'added amide nitrogen: {nitrogen}\n')
         self.text_area.insert(tk.INSERT,f'added alpha hydrogen: {alpha_hydrogen}\n')
         self.text_area.insert(tk.INSERT,f'added alpha hydrogen2: {alpha_hydrogen2}\n')
         self.text_area.insert(tk.INSERT,f'added carbonyl carbon: {carbon}\n')
         self.text_area.insert(tk.INSERT,f'added alpha carbon: {alpha_carbon}\n')
         self.text_area.insert(tk.INSERT,f'added beta carbon: {beta_carbon}\n')
         self.text_area.insert(tk.INSERT,f'added amide hydrogen: {hydrogen}\n')
         if nitrogen != '':
             if float(nitrogen) > 150 or float(nitrogen) < 100:
                self.text_area.insert(tk.INSERT,f'Warning value of nitrogen: {nitrogen} is outside of expected range\n')
             list_of_shifts.append(nitrogen)
         else:
             list_of_shifts.append('1000.00')
         if alpha_hydrogen != '':
             if float(alpha_hydrogen) > 7 or float(alpha_hydrogen) < 3:
                 self.text_area.insert(tk.INSERT,f'Warning value of HA: {alpha_hydrogen} is outside of expected range\n')
             list_of_shifts.append(alpha_hydrogen)
         else:
             list_of_shifts.append('1000.00')
         if alpha_hydrogen2 != '' and beta_carbon == '':
             if float(alpha_hydrogen2) > 7 or float(alpha_hydrogen2) < 3:
                 self.text_area.insert(tk.INSERT,f'Warning value of HA2: {alpha_hydrogen2} is outside of expected range\n')
             list_of_shifts.append(alpha_hydrogen2)
         if carbon != '':
             if float(carbon) > 200 or float(carbon) < 150:
                self.text_area.insert(tk.INSERT,f'Warning value of carbon: {carbon} is outside of expected range\n')
             list_of_shifts.append(carbon)
         else:
           list_of_shifts.append('1000.00')
         if alpha_carbon != '':
            if float(alpha_carbon) > 80 or float(alpha_carbon) < 30:
                self.text_area.insert(tk.INSERT,f'Warning value of CA: {alpha_carbon} is outside of expected range\n')
            list_of_shifts.append(alpha_carbon)
         else:
           list_of_shifts.append('1000.00')
         if beta_carbon != '' and alpha_hydrogen2 == '':
             if float(beta_carbon) > 50 or float(beta_carbon) < 10:
                 self.text_area.insert(tk.INSERT,f'Warning value of CB: {beta_carbon} is outside of expected range\n')
             list_of_shifts.append(beta_carbon)
         if beta_carbon == '' and alpha_hydrogen2 == '':
             list_of_shifts.append('1000.00')
         if hydrogen != '':
             if float(hydrogen) > 11 or float(hydrogen) < 6:
                 self.text_area.insert(tk.INSERT,f'Warning value of hydrogen: {hydrogen} is outside of expected range\n')
             list_of_shifts.append(hydrogen)
         else:
           list_of_shifts.append('1000.00')
         self.nitrogen_input.delete(0,"end")
         self.alpha_hydrogen_input.delete(0,"end")
         self.alpha_hydrogen2_input.delete(0,"end")
         self.carbon_input.delete(0,"end")
         self.alpha_carbon_input.delete(0,"end")
         self.beta_carbon_input.delete(0,"end")
         self.hydrogen_input.delete(0,"end")

    def write_file(self):
        if save_file_peaklist == ():
            self.text_area.insert(tk.INSERT,'please indicate your save file (make sure to use browse)\n')
        else:
            os.chdir(save_directory)
            with open(save_file_peaklist,'w') as file:
                for values in list_of_shifts:
                    file.write(values+'\n')
            self.text_area.insert(tk.INSERT,'File written\n')
