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
#from PIL import ImageTk, Image





root = tk.Tk()
root.title('SAPUS')
root.geometry('800x600')

def on_resize(event):
    image = bgimg.resize((event.width, event.height), Image.ANTIALIAS)
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)

#bgimg = Image.open('thunderstorm.jpg')
#l = tk.Label(root)
#l.place(x=0, y=0, relwidth=1, relheight=1)
#l.bind('<Configure>', on_resize)

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

text_area = ReadOnlyText(root,width = 40,height = 10,font = ("Times New Roman",12))

text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)
sparta_file=()
sparta_directory=()
dat_file=()
dat_directory=()
set_threshold=()

tk.Label(root, text="Sparta File (use SAVUS to generate proper SPARTA format)").grid(row=0)
tk.Label(root, text="Chemical shift file\n Ensure in proper format (check manual or use SAG to generate)").grid(row=1)
tk.Label(root, text="Set RMSD Threshold (click enter when done)").grid(row=2)

e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

def input_file():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global sparta_directory
    global sparta_file
    sparta_directory=os.path.dirname(fullpath)
    sparta_file= os.path.basename(fullpath)
    label2=Label(root,text=fullpath).grid(row=0,column=1)

def threshold():
    threshold_input=e3.get()
    global set_threshold
    set_threshold=float(threshold_input)
    text_area.insert(tk.INSERT,f'RMSD Threshold set: {threshold_input} \n')

def help():
    webbrowser.open('https://github.com/sam-mahdi/SPARKY-Assignment-Tools/blob/master/SAPUS/Manual/SAPUS_Manual.md')

def clear_option():
    text_area.delete(1.0,END)

def data_file():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global dat_file
    global dat_directory
    dat_directory=os.path.dirname(fullpath)
    dat_file= os.path.basename(fullpath)
    label3=Label(root,text=fullpath).grid(row=1,column=1)

def diag_sum():
    os.chdir(sparta_directory)
    fig,ax=plt.subplots()
    experimental_values=[]
    predicted_values=[]
    dict={}
    amino_acid_number=-1
    counter=0
#Creates a dictionary for the amino acid type and number. Used for plotting and labeling
#Creates a matrix of zeros the size of the data set, to be filled
    with open(sparta_file) as predictions, open(dat_file) as experimental:
        rows=0
        columns=0
        for lines in predictions:
            dict_modifier=lines.strip()
            counter+=1
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+[A-Z]',dict_modifier)
                dict[amino_acid_number]=atom_type.group(0)
            rows+=1
            predicted_values.append(lines)
        for lines2 in experimental:
            columns+=1
            experimental_values.append(lines2)
        columns_divided=int(rows/6)
        rows_divided=int(columns/6)
        matrix=np.zeros((rows_divided,columns_divided))

#Stores an amino acids values (all 6), then calculates the rmsd of that amino acid with each amino acid in SPARTA
#Each row will be the rmsd of the SPARTA amino acid, with the columns the experimental amino acid
    predict_value=[]
    error_value=[]
    experiment_value=[]
    square_deviations=[]
    number=0
    count=0
    numpy_list=[]
    iterations=-1
    shit=0
    for experiments in experimental_values:
        modifier=experiments.strip()
        splitting=modifier.split()
        experiment_value.append(splitting[1])
        number+=1
        if number == 6:
            number=0
            iterations+=1
            for prediction in predicted_values:
                modifier2=prediction.strip()
                splitting2=modifier2.split()
                predict_value.append(splitting2[1])
                error_value.append(splitting2[2])
                count+=1
                if count ==6:
                    count=0
                    shit+=1
                    for predict,experiment,error in zip(predict_value,experiment_value,error_value):
                        square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                        if square_deviation>100:
                            pass
                        else:
                            square_deviations.append(square_deviation)
                    if len(square_deviations)==0:
                        rmsd_filler=0
                        numpy_list.append(rmsd_filler)
                    else:
                        rmsd=math.sqrt(((1/int(len(square_deviations)))*(sum(square_deviations))))
                        numpy_list.append(rmsd)
                    predict_value.clear()
                    square_deviations.clear()
                    error_value.clear()
            experiment_value.clear()
            arr=np.array(numpy_list)
            matrix[iterations,:]=arr
            numpy_list.clear()
#The diagonal array rmsd is when the amino acid matches with the sparta+ values
    list1=[]
    for i in range(columns_divided):
        diagonal=np.diag(matrix,i)
        if len(diagonal)==rows_divided:
            summed_diagonal=(sum(diagonal))/(len(diagonal))
            if summed_diagonal<set_threshold:
                ax.scatter(i,summed_diagonal)
                tuples=(f'{dict[i]}-{dict[i+rows_divided-1]} rmsd=',summed_diagonal)
                list1.append(tuples)
        else:
            break
    text_area.insert(tk.INSERT,'Diagonal Sum (sorted by rmsd value)\n')
#This is sorting the rmsd from lowest to highest, then plotting them
    A=sorted(list1, key=lambda rmsd:rmsd[1])
    listed=list(A)
    for value in listed:
        two_decimal_points='%.2f' % value[1]
        text_area.insert(tk.INSERT,f'{value[0]}{two_decimal_points}\n')
    plt.title('Assigned-SPARTA RMSD values (Using Diagonal Sum)')
    plt.xlabel('Amino Acids')
    plt.ylabel('RMSD')
#This is a function designed to enable you highlight over the point in the plot and see its value
    crs = mplcursors.cursor(ax,hover=True)
    crs.connect("add", lambda sel: sel.annotation.set_text(
        'Point {},{}'.format(dict[sel.target[0]], '%.2f' % sel.target[1])))
    plt.show()

def rmsd_summed():
    os.chdir(sparta_directory)
    fig,ax=plt.subplots()
    experimental_values=[]
    predicted_values=[]
    dict={}
    amino_acid_number=-1
    counter=0
    with open(sparta_file) as predictions, open(dat_file) as experimental:
        rows=0
        columns=0
        for lines in predictions:
            dict_modifier=lines.strip()
            counter+=1
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+[A-Z]',dict_modifier)
                dict[amino_acid_number]=atom_type.group(0)
            rows+=1
            predicted_values.append(lines)
        for lines2 in experimental:
            columns+=1
            experimental_values.append(lines2)
        columns_divided=int(rows/6)
        rows_divided=int(columns/6)
        matrix=np.zeros((rows_divided,columns_divided))

        count=0
        iterations=0
        dmitry_list=[]
        dmitry_experiment_value=[]
        dmitry_predict_value=[]
        dmitry_error_value=[]
        dmitry_square_deviations=[]
        for experiments in experimental_values:
            modifier=experiments.strip()
            splitting=modifier.split()
            dmitry_experiment_value.append(splitting[1])
            iterations+=1
            if iterations == len(experimental_values):
                for prediction in predicted_values:
                    modifier2=prediction.strip()
                    splitting2=modifier2.split()
                    dmitry_predict_value.append(splitting2[1])
                    dmitry_error_value.append(splitting2[2])

#The experimental value is taken as a whole (instead of one by one) and the rmsd is calculated with SPARTA values
        below_rmsd_list=[]
        for i in range(len(dmitry_predict_value)):
            temp_predict_value=dmitry_predict_value[(i*6):(i*6)+len(dmitry_experiment_value)]
            temp_error_value=dmitry_error_value[(i*6):(i*6)+len(dmitry_experiment_value)]
            if ((i*6)+len(dmitry_experiment_value))>(len(dmitry_predict_value)):
                break
            else:
                for predict,experiment,error in zip(temp_predict_value,dmitry_experiment_value,temp_error_value):
                    square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                    if square_deviation>100:
                        pass
                    else:
                        dmitry_square_deviations.append(square_deviation)
                if len(dmitry_square_deviations)==0:
                    rmsd_filler=0
                    dmitry_list.append(rmsd_filler)
                else:
                    rmsd=math.sqrt(((1/int(len(dmitry_square_deviations)))*(sum(dmitry_square_deviations))))
                    dmitry_list.append(rmsd)
                    if rmsd<set_threshold:
                        ax.scatter(i,rmsd)
                        tuples2=(f'{dict[i]}-{dict[i+(len(dmitry_experiment_value)/6)-1]} rmsd=',rmsd)
                        below_rmsd_list.append(tuples2)
                dmitry_square_deviations.clear()
        text_area.insert(tk.INSERT,'Collective RMSD (sorted by rmsd value)\n')
#Sorting the rmsd values from lowest to highest
        B=sorted(below_rmsd_list, key=lambda rmsd:rmsd[1])
        listed2=list(B)
        for value in listed2:
            two_decimal_points2='%.2f' % value[1]
            text_area.insert(tk.INSERT,f'{value[0]}{two_decimal_points2}\n')
        plt.title('Assigned-SPARTA RMSD values (Using RMSD_Sum)')
        plt.xlabel('Amino Acids')
        plt.ylabel('RMSD')
        crs = mplcursors.cursor(ax,hover=True)
        crs.connect("add", lambda sel: sel.annotation.set_text(
            'Point {},{}'.format(dict[sel.target[0]], '%.2f' % sel.target[1])))
        plt.show()

def combined_sum():
    os.chdir(sparta_directory)
    fig,ax=plt.subplots()
    experimental_values=[]
    predicted_values=[]
    dict={}
    amino_acid_number=-1
    counter=0
    with open(sparta_file) as predictions, open(dat_file) as experimental:
        rows=0
        columns=0
        for lines in predictions:
            dict_modifier=lines.strip()
            counter+=1
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+[A-Z]',dict_modifier)
                dict[amino_acid_number]=atom_type.group(0)
            rows+=1
            predicted_values.append(lines)
        for lines2 in experimental:
            columns+=1
            experimental_values.append(lines2)
        columns_divided=int(rows/6)
        rows_divided=int(columns/6)
        matrix=np.zeros((rows_divided,columns_divided))


    predict_value=[]
    error_value=[]
    experiment_value=[]
    square_deviations=[]
    number=0
    count=0
    numpy_list=[]
    iterations=-1
    shit=0
    for experiments in experimental_values:
        modifier=experiments.strip()
        splitting=modifier.split()
        experiment_value.append(splitting[1])
        number+=1
        if number == 6:
            number=0
            iterations+=1
            for prediction in predicted_values:
                modifier2=prediction.strip()
                splitting2=modifier2.split()
                predict_value.append(splitting2[1])
                error_value.append(splitting2[2])
                count+=1
                if count ==6:
                    count=0
                    shit+=1
                    for predict,experiment,error in zip(predict_value,experiment_value,error_value):
                        square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                        if square_deviation>100:
                            pass
                        else:
                            square_deviations.append(square_deviation)
                    if len(square_deviations)==0:
                        rmsd_filler=0
                        numpy_list.append(rmsd_filler)
                    else:
                        rmsd=math.sqrt(((1/int(len(square_deviations)))*(sum(square_deviations))))
                        numpy_list.append(rmsd)
                    predict_value.clear()
                    square_deviations.clear()
                    error_value.clear()
            experiment_value.clear()
            arr=np.array(numpy_list)
            matrix[iterations,:]=arr
            numpy_list.clear()
    list1=[]
    for i in range(columns_divided):
        diagonal=np.diag(matrix,i)
        if len(diagonal)==rows_divided:
            summed_diagonal=(sum(diagonal))/(len(diagonal))
            if summed_diagonal<set_threshold:
                tuples=(f'{dict[i]}-{dict[i+rows_divided-1]} rmsd=',summed_diagonal)
                list1.append(tuples)
        else:
            break
    A=sorted(list1, key=lambda rmsd:rmsd[1])
    listed=list(A)
    iterations=0
    dmitry_list=[]
    dmitry_experiment_value=[]
    dmitry_predict_value=[]
    dmitry_error_value=[]
    dmitry_square_deviations=[]
    for experiments in experimental_values:
        modifier=experiments.strip()
        splitting=modifier.split()
        dmitry_experiment_value.append(splitting[1])
        iterations+=1
        if iterations == len(experimental_values):
            for prediction in predicted_values:
                modifier2=prediction.strip()
                splitting2=modifier2.split()
                dmitry_predict_value.append(splitting2[1])
                dmitry_error_value.append(splitting2[2])


    below_rmsd_list=[]
    for i in range(len(dmitry_predict_value)):
        temp_predict_value=dmitry_predict_value[(i*6):(i*6)+len(dmitry_experiment_value)]
        temp_error_value=dmitry_error_value[(i*6):(i*6)+len(dmitry_experiment_value)]
        if ((i*6)+len(dmitry_experiment_value))>(len(dmitry_predict_value)):
            break
        else:
            for predict,experiment,error in zip(temp_predict_value,dmitry_experiment_value,temp_error_value):
                square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                if square_deviation>100:
                    pass
                else:
                    dmitry_square_deviations.append(square_deviation)
            if len(dmitry_square_deviations)==0:
                rmsd_filler=0
                dmitry_list.append(rmsd_filler)
            else:
                rmsd=math.sqrt(((1/int(len(dmitry_square_deviations)))*(sum(dmitry_square_deviations))))
                dmitry_list.append(rmsd)
                if rmsd<set_threshold:
                    tuples2=(f'{dict[i]}-{dict[i+(len(dmitry_experiment_value)/6)-1]} rmsd=',rmsd)
                    below_rmsd_list.append(tuples2)
            dmitry_square_deviations.clear()
    B=sorted(below_rmsd_list, key=lambda rmsd:rmsd[1])
    listed2=list(B)
#This combines the rmsd obtained from the diagonal sum, and the RMSD whole
    combined_list=[]
    for values in listed:
        amino_acid_search=re.search('^\d+[A-Z]',values[0])
        r=re.compile(amino_acid_search.group(0))
        rmsd_find=list(filter(r.match,[i[0] for i in listed2]))
        if rmsd_find !=[]:
            rmsd_find_string=''.join(rmsd_find)
            for values2 in listed2:
                if values2[0]==rmsd_find_string:
                    summed_values='%.2f' % ((values[1]+values2[1])/2)
                    combined_list.append(f'{values2[0]}{summed_values}')
    text_area.insert(tk.INSERT,'Combined sum (sorted by rmsd)\n')
    for_plotting=sorted(combined_list,key = lambda s: int(s[:s.find("-")-1]))
#The x value needs to be specified, thus in the first string that contains that value, it is extracted and plotted
    for values4 in for_plotting:
        searcher=re.search('^\d+',values4)
        searcher2=re.search('\d+\.\d+',values4)
        ax.scatter(float(searcher.group(0)),float(searcher2.group(0)))
    for values3 in combined_list:
        text_area.insert(tk.INSERT,f'{values3}\n')
    plt.title('Assigned-SPARTA RMSD values (Using Combined_Sum)')
    plt.xlabel('Amino Acids')
    plt.ylabel('RMSD')
    crs = mplcursors.cursor(ax,hover=True)
    crs.connect("add", lambda sel: sel.annotation.set_text(
        'Point {},{}'.format(dict[sel.target[0]-4], '%.2f' % sel.target[1])))
    plt.show()


tk.Button(root,text='browse',command=input_file).grid(row=0,column=2)
tk.Button(root,text='browse',command=data_file).grid(row=1,column=2)
tk.Button(root,text='run using diagonal sum',command=diag_sum).grid(row=3,column=0)
tk.Button(root,text='run using RMSD sum',command=rmsd_summed).grid(row=3,column=1)
tk.Button(root,text='run using combined sum',command=combined_sum).grid(row=3,column=2)
tk.Button(root,text='Clear',command=clear_option).grid(row=4,column=1)
tk.Button(root,text='enter',command=threshold).grid(row=2,column=2)
tk.Button(root,text='quit',command=root.quit).grid(row=4,column=2)
tk.Button(root,text='help',command=help).grid(row=4,column=0)



root.mainloop()
