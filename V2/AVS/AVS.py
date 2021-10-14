import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import math
import re
import tkinter.scrolledtext as st
from tkinter import ttk
import functools
from PIL import ImageTk, Image
import webbrowser
import sys


root = tk.Tk()
root.title('AVS_V3')
#This is for fitting the image to the size of the GUI
def on_resize(event):
    image = bgimg.resize((event.width, event.height), Image.ANTIALIAS)
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)

root.geometry('1200x800')

bgimg = Image.open('mountain.jpg')
l = tk.Label(root)
l.place(x=0, y=0, relwidth=1, relheight=1)
l.bind('<Configure>', on_resize)
#This enables the output box to update, but prevents the user from typing stuff into it (read only)
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


ttk.Label(root,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 15)

text_area = ReadOnlyText(root,width = 40,height = 10,font = ("Times New Roman",12))

text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)

tk.Label(root, text="If using SPARKY Peaklist Files").grid(row=0)
tk.Label(root, text="Sparta or BMRB File").grid(row=1)
tk.Label(root, text="Sequence File").grid(row=2)
tk.Label(root, text="Save Sparta or BMRB Filename").grid(row=3)
tk.Label(root, text="Save Peaklist Filename").grid(row=4)
tk.Label(root, text="Mutations (enter what amino acid was mutated E.G. R133A)\n If multiple mutations, seperate with space. (e.g. R133A Q223A)\n Hit enter when done").grid(row=5)
tk.Label(root, text="Please type in what residue number the first amino acid in the sequence file is\nI.E. if the first amino acid in the sequence file is 20, type in 20\n Click enter when done").grid(row=6)
tk.Label(root, text="Set RMSD Threshold (Recommended 2-3). Click enter when done").grid(row=7)
tk.Label(root, text="NMR_STAR File").grid(row=8)


sparta_bmrb_file_entry = tk.Entry(root)
sequence_file_entry = tk.Entry(root)
save_bmrb_sparta_entry = tk.Entry(root)
save_peaklist_entry = tk.Entry(root)
mutation_entry = tk.Entry(root)
sequence_start_entry = tk.Entry(root)
rmsd_entry = tk.Entry(root)
nmrstar_file_entry = tk.Entry(root)
sparta_bmrb_file_entry.grid(row=1, column=1)
sequence_file_entry.grid(row=2, column=1)
save_bmrb_sparta_entry.grid(row=3, column=1)
save_peaklist_entry.grid(row=4, column=1)
mutation_entry.grid(row=5, column=1)
sequence_start_entry.grid(row=6, column=1)
rmsd_entry.grid(row=7, column=1)
nmrstar_file_entry.grid(row=8, column=1)

#These global values are what is entered by the user, and use within the script
sparta_file=()
sparta_directory=()
seq_file=()
seq_directory=()
save_file_sparta=()
save_file_peaklist=()
save_directory=()
mutation_list=()
seq_start=()
set_threshold=()
nmrstarfile=()
nmrstarfile_directory=()

#These functions define the function of the buttons
def input_file():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global sparta_directory
    global sparta_file
    sparta_directory=os.path.dirname(fullpath)
    sparta_file= os.path.basename(fullpath)
    if sparta_directory == '' or sparta_file == '':
        sparta_file=()
        sparta_directory=()
    label2=Label(root,text=fullpath).grid(row=1,column=1)

def input_seq():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global seq_file
    global seq_directory
    seq_directory=os.path.dirname(fullpath)
    seq_file= os.path.basename(fullpath)
    if seq_directory == '' or seq_file == '':
        seq_directory=()
        seq_file=()
    label3=Label(root,text=fullpath).grid(row=2,column=1)


def save_file():
    myFormats = [('Text File','*.txt'),]
    fullpath = tk.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save file as...")
    global save_file_sparta
    global save_directory
    save_directory=os.path.dirname(fullpath)
    save_file_sparta=os.path.basename(fullpath)
    if save_directory == '' or save_file_sparta == '':
        save_directory=()
        save_file_sparta=()
    label2=Label(root,text=fullpath).grid(row=3,column=1)

def save_filsequence_file_entry():
    myFormats = [('Text File','*.txt'),]
    fullpath = tk.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save the image as...")
    global save_file_peaklist
    global save_directory
    save_directory=os.path.dirname(fullpath)
    save_file_peaklist=os.path.basename(fullpath)
    if save_directory == '' or save_file_peaklist == '':
        save_directory=()
        save_file_peaklist=()
    label8=Label(root,text=fullpath).grid(row=4,column=1)

def mutation_input():
    global mutation_list
    mutation_list=mutation_entry.get()
    text_area.insert(tk.INSERT,f'mutation entered: {mutation_list} \n')

def seq_number():
    seq_input=sequence_start_entry.get()
    global seq_start
    seq_start=int(seq_input)
    text_area.insert(tk.INSERT,f'sequence starts: {seq_input} \n')

def threshold():
    threshold_input=rmsd_entry.get()
    global set_threshold
    set_threshold=float(threshold_input)
    text_area.insert(tk.INSERT,f'RMSD Threshold set: {threshold_input} \n')

def help():
    webbrowser.open('https://github.com/sam-mahdi/Peaklist_Assignment_Library-PAL-/blob/master/V2/AVS/Manual/Manual.md')

def nmrstar():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global nmrstarfile
    global nmrstarfile_directory
    nmrstarfile_directory=os.path.dirname(fullpath)
    nmrstarfile= os.path.basename(fullpath)
    label8=Label(root,text=fullpath).grid(row=8,column=1)

def sparta_gen_only():
    text_area.delete(1.0,END)
    if sparta_file == ():
        text_area.insert(tk.INSERT,'please upload your sparta file (make sure to use browse)\n')
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if save_file_sparta == ():
        text_area.insert(tk.INSERT,'please indicate sparta save file (make sure to use browse)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    else:
        text_area.insert(tk.INSERT,'Starting Program\n')
        text_area.insert(tk.INSERT,'Creating Sparta File\n')
        text_area.update_idletasks()
        from sparta_file_formatter import check_sparta_file_boundaries
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
        text_area.insert(tk.INSERT,'Sparta file written\n')

def bmrb_gen_only():
    text_area.delete(1.0,END)
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if save_file_sparta == ():
        text_area.insert(tk.INSERT,'please indicate sparta save file (make sure to use browse)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    else:
        text_area.insert(tk.INSERT,'Starting Program\n')
        text_area.insert(tk.INSERT,'Creating BMRB File\n')
        text_area.update_idletasks()
        from bmrb_file_formatter import make_bmrb_list
        bmrb_file_boundaries=make_bmrb_list(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file:
            for stuff_to_write in bmrb_file_boundaries:
                file.write(stuff_to_write+'\n')
        text_area.insert(tk.INSERT,'BMRB file written\n')

def sparky_peaklist_files():
    from new_window import newTopLevel
    new_top = newTopLevel(root)
    newWindow = new_top.newWindow

def sparta_generator():
    from sparta_window import  SpartaGenerationWindow
    new_sparta_window= SpartaGenerationWindow(root)
    spartawidnow=new_sparta_window.sparta_window

def run_talos():
    from talos_window import TalosrunWindow
    new_talos_window=TalosrunWindow(root)
    taloswindow=new_talos_window.talos_window

def sparta_run():
    text_area.delete(1.0,END)
    if sparta_file == ():
        text_area.insert(tk.INSERT,'please upload your sparta file (make sure to use browse)\n')
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if save_file_sparta == ():
        text_area.insert(tk.INSERT,'please indicate sparta save file (make sure to use browse)\n')
    if save_file_peaklist == ():
        text_area.insert(tk.INSERT,'please indicate peaklist save file (make sure to use browse)\n')
    if set_threshold == ():
        text_area.insert(tk.INSERT,'please enter a threshold (make sure to hit enter)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    if nmrstarfile == ():
        text_area.insert(tk.INSERT,'please upload your nmrstar file (make sure to use browse)\n')
    else:
        text_area.insert(tk.INSERT,'Starting Program\n')
        text_area.insert(tk.INSERT,'Creating Sparta File\n')
        text_area.update_idletasks()

        os.chdir(nmrstarfile_directory)
        from sparta_file_formatter import check_sparta_file_boundaries
        from nmrstar import fill_in_missing_data
        from RMSD_Calculator import RMSD_calc
        from RMSD_Calculator import filter_peaklist_to_sparta

        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        data_files=fill_in_missing_data(seq_file,nmrstarfile,seq_start,text_area,seq_directory)
        RMSD_calc(set_threshold,sparta_file_boundaries,data_files,text_area)
        data_file_to_save=filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area)

        #Both files are saved for use in other programs
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as filsequence_file_entry:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_writsequence_file_entry in data_file_to_save:
                    filsequence_file_entry.write(stuff_to_writsequence_file_entry+'\n')

def bmrb_run():
    text_area.delete(1.0,END)
    if sparta_file == ():
        text_area.insert(tk.INSERT,'please upload your sparta file (make sure to use browse)\n')
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if save_file_sparta == ():
        text_area.insert(tk.INSERT,'please indicate sparta save file (make sure to use browse)\n')
    if save_file_peaklist == ():
        text_area.insert(tk.INSERT,'please indicate peaklist save file (make sure to use browse)\n')
    if set_threshold == ():
        text_area.insert(tk.INSERT,'please enter a threshold (make sure to hit enter)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    if nmrstarfile == ():
        text_area.insert(tk.INSERT,'please upload your nmrstar file (make sure to use browse)\n')
    else:
        text_area.insert(tk.INSERT,'Starting Program\n')
        text_area.insert(tk.INSERT,'Creating BMRB File\n')
        text_area.update_idletasks()

        os.chdir(nmrstarfile_directory)
        from bmrb_file_formatter import make_bmrb_list
        from nmrstar import fill_in_missing_data
        from RMSD_Calculator import RMSD_calc
        from RMSD_Calculator import filter_peaklist_to_sparta

        sparta_file_boundaries=make_bmrb_list(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        data_files=fill_in_missing_data(seq_file,nmrstarfile,seq_start,text_area,seq_directory)
        RMSD_calc(set_threshold,sparta_file_boundaries,data_files,text_area)
        data_file_to_save=filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area)

        #Both files are saved for use in other programs
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as filsequence_file_entry:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_writsequence_file_entry in data_file_to_save:
                    filsequence_file_entry.write(stuff_to_writsequence_file_entry+'\n')

tk.Button(root,text='Click here if using SPARKY peaklist files',command=sparky_peaklist_files).grid(row=0,column=1)
tk.Button(root,text='browse',command=input_file).grid(row=1,column=2)
tk.Button(root,text='Generate Sparta File',command=sparta_generator).grid(row=1,column=3)
tk.Button(root,text='Run TALOS',command=run_talos).grid(row=3,column=3)
tk.Button(root,text='browse',command=input_seq).grid(row=2,column=2)
tk.Button(root,text='browse',command=save_file).grid(row=3,column=2)
tk.Button(root,text='browse',command=save_filsequence_file_entry).grid(row=4,column=2)
tk.Button(root,text='enter',command=mutation_input).grid(row=5,column=2)
tk.Button(root,text='enter',command=seq_number).grid(row=6,column=2)
tk.Button(root,text='enter',command=threshold).grid(row=7,column=2)
tk.Button(root,text='browse',command=nmrstar).grid(row=8,column=2)
tk.Button(root,text='Help',command=help).grid(row=9,column=0)
tk.Button(root,text='Quit',command=root.quit).grid(row=10,column=0)
tk.Button(root,text='Run using SPARTA',command=sparta_run).grid(row=9,column=1)
tk.Button(root,text='Run using BMRB',command=bmrb_run).grid(row=9,column=2)
tk.Button(root,text='Generate SPARTA file only (for APS)',command=sparta_gen_only).grid(row=10,column=1)
tk.Button(root,text='Generate BMRB file only (for APS)',command=bmrb_gen_only).grid(row=10,column=2)

root.mainloop()
#tk.mainloop()
