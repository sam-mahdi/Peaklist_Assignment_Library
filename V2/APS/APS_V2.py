import tkinter as tk
from tkinter import filedialog
import os
import tkinter.scrolledtext as st
from tkinter import ttk
import functools
from tkinter import *
import math
import re
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import webbrowser
from PIL import ImageTk, Image
from matplotlib import rcParams, cycler





root = tk.Tk()
root.title('APS')
root.geometry('1200x800')

def on_resize(event):
    image = bgimg.resize((event.width, event.height), Image.ANTIALIAS)
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)

bgimg = Image.open('beach.jpg')
l = tk.Label(root)
l.place(x=0, y=0, relwidth=1, relheight=1)
l.bind('<Configure>', on_resize)

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


ttk.Label(root,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 14)

text_area = ReadOnlyText(root,width = 80,height = 10,font = ("Times New Roman",12))

text_area.grid(column = 0,columnspan=4,sticky=W+E,pady = 10, padx = 10)
sparta_file=()
sparta_directory=()
data_file=()
data_directory=()
set_threshold=()

tk.Label(root, text="Sparta File (use AVS to generate proper SPARTA format)").grid(row=0)
tk.Label(root, text="Chemical shift file\n Ensure in proper format (check manual or use File Generator)").grid(row=1)
tk.Label(root, text="Set RMSD Threshold (click enter when done)").grid(row=2)
tk.Label(root, text="File Generator").grid(row=3)

sparta_input = tk.Entry(root)
exp_data_input = tk.Entry(root)
rmsd_threshold_input = tk.Entry(root)
sparta_input.grid(row=0, column=1)
exp_data_input.grid(row=1, column=1)
rmsd_threshold_input.grid(row=2, column=1)

def input_file():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global sparta_directory
    global sparta_file
    sparta_directory=os.path.dirname(fullpath)
    sparta_file= os.path.basename(fullpath)
    label2=Label(root,text=fullpath).grid(row=0,column=1)

def threshold():
    threshold_input=rmsd_threshold_input.get()
    global set_threshold
    set_threshold=float(threshold_input)
    text_area.insert(tk.INSERT,f'RMSD Threshold set: {threshold_input} \n')

def help():
    webbrowser.open('https://github.com/sam-mahdi/Peaklist_Assignment_Library-PAL-/tree/master/V2/APS/Manual')

def clear_option():
    text_area.delete(1.0,END)

def data_file():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global data_file
    global data_directory
    data_directory=os.path.dirname(fullpath)
    data_file= os.path.basename(fullpath)
    label3=Label(root,text=fullpath).grid(row=1,column=1)

def diag_sum():
    if sparta_file == ():
        text_area.insert(tk.INSERT,'\nPlease input a sparta file. Make sure to use the Browse button')
        return
    if isinstance(data_file,str) is False:
        text_area.insert(tk.INSERT,'\nPlease input a peaklist file. Make sure to use the Browse button ')
        return
    if set_threshold == ():
        text_area.insert(tk.INSERT,'\nPlease input an rmsd number. Make sure to click Enter.')
        return
    text_area.insert(tk.INSERT,'\nDiagonal Sum (sorted by rmsd value)\n')
    #This is sorting the rmsd from lowest to highest, then plotting them
    from check_file_format import check
    sparta,data=check(sparta_file,sparta_directory,data_file,data_directory)
    if sparta != []:
        for sparta_errors in sparta:
            text_area.insert(tk.INSERT, sparta_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return
    if data != []:
        for data_errors in data:
            text_area.insert(tk.INSERT, data_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return
    from diagonal_sum import find_diagonal
    residues,rmsd,list_of_matches,x_axis=find_diagonal(sparta_file,sparta_directory,data_file,data_directory,set_threshold)
    if len(list_of_matches) == 0:
        text_area.insert(tk.INSERT,'No Matches Found. Try increasing RMSD\n')
    else:
        fig,ax=plt.subplots()
        colors = np.random.rand(len(residues),3)
        ax.scatter(x_axis,rmsd,c=colors)
        sort_lowrmsd_highrmsd=sorted(list_of_matches, key=lambda rmsd:rmsd[1])
        listed=list(sort_lowrmsd_highrmsd)
        for value in listed:
            two_decimal_points='%.2f' % value[1]
            text_area.insert(tk.INSERT,f'{value[0]}{two_decimal_points}\n')
        plt.title('Assigned-SPARTA RMSD values (Using Diagonal Sum)')
        plt.xlabel('Amino Acids')
        plt.ylabel('RMSD')
        dict={}
        for number,values in zip(x_axis,residues):
            for amino_acids in listed:
                regex_search=re.search('(\d+\s+\w)(-\d+\s+\w+)',amino_acids[0])
                if regex_search.group(1) == values:
                    dict[number]=values+regex_search.group(2)
        #This is a function designed to enable you highlight over the point in the plot and see its value
        crs = mplcursors.cursor(ax,hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(
            'Point {},{}'.format(dict[sel.target[0]], '%.2f' % sel.target[1])))
        plt.show()

def rmsd_summed():
    if sparta_file == ():
        text_area.insert(tk.INSERT,'\nPlease input a sparta file. Make sure to use the Browse button')
        return
    if isinstance(data_file,str) is False:
        text_area.insert(tk.INSERT,'\nPlease input a peaklist file. Make sure to use the Browse button ')
        return
    if set_threshold == ():
        text_area.insert(tk.INSERT,'\nPlease input an rmsd number. Make sure to click Enter.')
        return
    from check_file_format import check
    sparta,data=check(sparta_file,sparta_directory,data_file,data_directory)
    if sparta != []:
        for sparta_errors in sparta:
            text_area.insert(tk.INSERT, sparta_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return
    if data != []:
        for data_errors in data:
            text_area.insert(tk.INSERT, data_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return

    from combined_rmsd import calculate_combined_rmsd
    text_area.insert(tk.INSERT,'Collective RMSD (sorted by rmsd value)\n')
#Sorting the rmsd values from lowest to highest
    residues,rmsd,list_of_matches,x_axis=calculate_combined_rmsd(sparta_file,sparta_directory,data_file,data_directory,set_threshold)
    if len(list_of_matches) == 0:
        text_area.insert(tk.INSERT,'No Matches Found. Try increasing RMSD\n')
    else:
        fig,ax=plt.subplots()
        colors = np.random.rand(len(residues),3)
        ax.scatter(x_axis,rmsd,c=colors)
        sort_lowrmsd_highrmsd=sorted(list_of_matches, key=lambda rmsd:rmsd[1])
        listed=list(sort_lowrmsd_highrmsd)
        for value in listed:
            two_decimal_points='%.2f' % value[1]
            text_area.insert(tk.INSERT,f'{value[0]}{two_decimal_points}\n')
        dict={}
        for number,values in zip(x_axis,residues):
            for amino_acids in listed:
                regex_search=re.search('(\d+\s+\w)(-\d+\s+\w+)',amino_acids[0])
                if regex_search.group(1) == values:
                    dict[number]=values+regex_search.group(2)
        plt.title('Assigned-SPARTA RMSD values (Using RMSD_Sum)')
        plt.xlabel('Amino Acids')
        plt.ylabel('RMSD')
        crs = mplcursors.cursor(ax,hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(
            'Point {},{}'.format(dict[sel.target[0]], '%.2f' % sel.target[1])))
        plt.show()

def combined_sum():
    if sparta_file == ():
        text_area.insert(tk.INSERT,'\nPlease input a sparta file. Make sure to use the Browse button')
        return
    if isinstance(data_file,str) is False:
        text_area.insert(tk.INSERT,'\nPlease input a peaklist file. Make sure to use the Browse button ')
        return
    if set_threshold == ():
        text_area.insert(tk.INSERT,'\nPlease input an rmsd number. Make sure to click Enter.')
        return
    from check_file_format import check
    sparta,data=check(sparta_file,sparta_directory,data_file,data_directory)
    if sparta != []:
        for sparta_errors in sparta:
            text_area.insert(tk.INSERT, sparta_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return
    if data != []:
        for data_errors in data:
            text_area.insert(tk.INSERT, data_errors)
        text_area.insert(tk.INSERT, '\nPlease correct above errors and try again')
        return
    from diagonal_sum import find_diagonal
    from combined_rmsd import calculate_combined_rmsd
    residues,rmsd,list_of_matches,x_axis=find_diagonal(sparta_file,sparta_directory,data_file,data_directory,set_threshold)
    sort_lowrmsd_highrmsd=sorted(list_of_matches, key=lambda rmsd:rmsd[1])
    listed=list(sort_lowrmsd_highrmsd)
    residues,rmsd,list_of_matches,x_axis=calculate_combined_rmsd(sparta_file,sparta_directory,data_file,data_directory,set_threshold)
    sort_lowrmsd_highrmsd=sorted(list_of_matches, key=lambda rmsd:rmsd[1])
    listed2=list(sort_lowrmsd_highrmsd)
#This combines the rmsd obtained from the diagonal sum, and the RMSD whole
    combined_list=[]
    if len(listed) == 0 or len(listed2) == 0:
        text_area.insert(tk.INSERT,'No Matches Found. Try increasing RMSD\n')
    else:
        fig,ax=plt.subplots()
        for values in listed:
            amino_acid_search=re.search('\d+\s+[A-Z]',values[0])
            r=re.compile(amino_acid_search.group(0))
            rmsd_find=list(filter(r.match,[i[0] for i in listed2]))
            if rmsd_find !=[]:
                rmsd_find_string=''.join(rmsd_find)
                for values2 in listed2:
                    if values2[0]==rmsd_find_string:
                        summed_values='%.2f' % ((values[1]+values2[1])/2)
                        combined_list.append(f'{values2[0]}{summed_values}')
        text_area.insert(tk.INSERT,'Combined sum (sorted by rmsd)\n')
        for_plotting=sorted(combined_list,key = lambda s: (s[s.find("=")+1:]))
    #The x value needs to be specified, thus in the first string that contains that value, it is extracted and plotted
        x=[]
        y=[]
        dict={}
        for values4 in for_plotting:
            x_axis=(re.search('^\d+',values4)).group(0)
            y_axis=(re.search('\d+\.\d+',values4)).group(0)
            dict_value=re.search('(\d+\s+\w)(-\d+\s+\w+)',values4)
            dict[int(x_axis)]=f'{dict_value.group(1)}{dict_value.group(2)}'
            x.append(float(x_axis))
            y.append(float(y_axis))
        for values3 in for_plotting:
            text_area.insert(tk.INSERT,f'{values3}\n')
        plt.title('Assigned-SPARTA RMSD values (Using Combined_Sum)')
        plt.xlabel('Amino Acids')
        plt.ylabel('RMSD')
        colors = np.random.rand(len(x),3)
        ax.scatter(x,y,c=colors)
        crs = mplcursors.cursor(ax,hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(
            'Point {},{}'.format(dict[sel.target[0]], '%.2f' % sel.target[1])))
        plt.show()

def file_generator():
    from newWindow import newTopLevel
    new_top = newTopLevel(root)
    newWindow = new_top.newWindow

def CH3_shift_window():
    from CH3_shift_window import CH3Shift
    new_window=CH3Shift(root)
    ch3shift_window=new_window.CH3_shift_window


tk.Button(root,text='browse',command=input_file).grid(row=0,column=2)
tk.Button(root,text='browse',command=data_file).grid(row=1,column=2)
tk.Button(root,text='enter',command=threshold).grid(row=2,column=2)
tk.Button(root,text='Click here to generate peaklist file',command=file_generator).grid(row=3,column=1)
tk.Button(root,text='run using diagonal sum',command=diag_sum).grid(row=4,column=0)
tk.Button(root,text='run using RMSD sum',command=rmsd_summed).grid(row=4,column=1)
tk.Button(root,text='run using combined sum',command=combined_sum).grid(row=4,column=2)
tk.Button(root,text='Clear',command=clear_option).grid(row=5,column=1)
tk.Button(root,text='quit',command=root.quit).grid(row=5,column=2)
tk.Button(root,text='help',command=help).grid(row=5,column=0)
tk.Button(root,text='CH3 Shift',command=CH3_shift_window).grid(row=5,column=3)



root.mainloop()
