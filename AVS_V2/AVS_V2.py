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




root = tk.Tk()
root.title('AVS_V2')
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

tk.Label(root, text="Sparta File").grid(row=0)
tk.Label(root, text="Sequence File").grid(row=1)
tk.Label(root, text="NHSQC Peaklist").grid(row=2)
tk.Label(root, text="HNCA  Peaklist").grid(row=3)
tk.Label(root, text="HNCACB  Peaklist").grid(row=4)
tk.Label(root, text="HNCO  Peaklist").grid(row=5)
tk.Label(root, text="Save Sparta Filename").grid(row=6)
tk.Label(root, text="Save Peaklist Filename").grid(row=7)
tk.Label(root, text="Mutations (enter what amino acid was mutated E.G.if mutation was R133A, type 133R)\n If multiple mutations, seperate with space.\n Hit enter when done").grid(row=8)
tk.Label(root, text="Mutations (enter what it was mutated to E.G. if mutation was R133A, type 133A)\n If multiple mutations, seperate with space.\n Hit enter when done").grid(row=9)
tk.Label(root, text="Please type in what residue number the first amino acid in the sequence file is\nI.E. if the first amino acid in the sequence file is 20, type in 20\n Click enter when done").grid(row=10)
tk.Label(root, text="Set RMSD Threshold (Recommended 2-3). Click enter when done").grid(row=11)
tk.Label(root, text="NMR_STAR V2 or V3").grid(row=12)


e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e4 = tk.Entry(root)
e5 = tk.Entry(root)
e6 = tk.Entry(root)
e7 = tk.Entry(root)
e8 = tk.Entry(root)
e9 = tk.Entry(root)
e10 = tk.Entry(root)
e11 = tk.Entry(root)
e12 = tk.Entry(root)
e13 = tk.Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)
e7.grid(row=6, column=1)
e8.grid(row=7, column=1)
e9.grid(row=8, column=1)
e10.grid(row=9, column=1)
e11.grid(row=10, column=1)
e12.grid(row=11, column=1)
e13.grid(row=12, column=1)

#These global values are what is entered by the user, and use within the script
sparta_file=()
sparta_directory=()
seq_file=()
seq_directory=()
save_file_sparta=()
save_file_peaklist=()
save_directory=()
NHSQC_file=()
NHSQC_directory=()
HNCA_file=()
HNCA_directory=()
HNCACB_file=()
HNCACB_directory=()
HNCO_file=()
HNCA_directory=()
mutation_list1=()
mutation_list2=()
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
    label2=Label(root,text=fullpath).grid(row=0,column=1)

def input_seq():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global seq_file
    global seq_directory
    seq_directory=os.path.dirname(fullpath)
    seq_file= os.path.basename(fullpath)
    label3=Label(root,text=fullpath).grid(row=1,column=1)

def NHSQC():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global NHSQC_file
    global NHSQC_directory
    NHSQC_directory=os.path.dirname(fullpath)
    NHSQC_file= os.path.basename(fullpath)
    label4=Label(root,text=fullpath).grid(row=2,column=1)

def HNCA():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global HNCA_file
    global HNCA_directory
    HNCA_directory=os.path.dirname(fullpath)
    HNCA_file= os.path.basename(fullpath)
    label5=Label(root,text=fullpath).grid(row=3,column=1)

def HNCACB():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global HNCACB_file
    global HNCACB_directory
    HNCACB_directory=os.path.dirname(fullpath)
    HNCACB_file= os.path.basename(fullpath)
    label6=Label(root,text=fullpath).grid(row=4,column=1)

def HNCO():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global HNCO_file
    global HNCO_directory
    HNCO_directory=os.path.dirname(fullpath)
    HNCO_file= os.path.basename(fullpath)
    label7=Label(root,text=fullpath).grid(row=5,column=1)


def save_file():
    myFormats = [('Text File','*.txt'),]
    fullpath = tk.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save file as...")
    global save_file_sparta
    global save_directory
    save_directory=os.path.dirname(fullpath)
    save_file_sparta=os.path.basename(fullpath)
    label2=Label(root,text=fullpath).grid(row=6,column=1)

def save_file2():
    myFormats = [('Text File','*.txt'),]
    fullpath = tk.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save the image as...")
    global save_file_peaklist
    global save_directory
    save_directory=os.path.dirname(fullpath)
    save_file_peaklist=os.path.basename(fullpath)
    label8=Label(root,text=fullpath).grid(row=7,column=1)

def mutation_input():
    mutation1_input=e9.get()
    split_mutation=mutation1_input.split()
    global mutation_list1
    mutation_list1=split_mutation
    text_area.insert(tk.INSERT,f'mutation entered: {mutation1_input} \n')


def mutation_input2():
    mutation2_input=e10.get()
    split_mutation2=mutation2_input.split()
    global mutation_list2
    mutation_list2=split_mutation2
    text_area.insert(tk.INSERT,f'mutation entered: {mutation2_input} \n')

def seq_number():
    seq_input=e11.get()
    global seq_start
    seq_start=int(seq_input)
    text_area.insert(tk.INSERT,f'number entered: {seq_input} \n')

def threshold():
    threshold_input=e12.get()
    global set_threshold
    set_threshold=float(threshold_input)
    text_area.insert(tk.INSERT,f'RMSD Threshold set: {threshold_input} \n')

def help():
    webbrowser.open('https://github.com/sam-mahdi/Peaklist_Assignment_Library/blob/master/AVS/HELP/AVS_Manual.md')

def nmrstar():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global nmrstarfile
    global nmrstarfile_directory
    nmrstarfile_directory=os.path.dirname(fullpath)
    nmrstarfile= os.path.basename(fullpath)
    label8=Label(root,text=fullpath).grid(row=12,column=1)

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
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
        text_area.insert(tk.INSERT,'Sparta file written\n')

def sparky_peaklist_files():
    text_area.delete(1.0,END)
    if sparta_file == ():
        text_area.insert(tk.INSERT,'please upload your sparta file (make sure to use browse)\n')
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if save_file_sparta == ():
        text_area.insert(tk.INSERT,'please indicate sparta save file (make sure to use browse)\n')
    if save_file_peaklist == ():
        text_area.insert(tk.INSERT,'please indicate peaklist save file (make sure to use browse)\n')
    if NHSQC_file == ():
        text_area.insert(tk.INSERT,'please upload NHSQC peaklist (make sure to use browse)\n')
    if HNCA_file == ():
        text_area.insert(tk.INSERT,'please upload HNCO file (make sure to use browse)\n')
    if HNCACB_file == ():
        text_area.insert(tk.INSERT,'please upload HNCACB file (make sure to use browse)\n')
    if HNCO_file == ():
        text_area.insert(tk.INSERT,'please upload HNCO file (make sure to use browse)\n')
    if set_threshold == ():
        text_area.insert(tk.INSERT,'please enter a threshold (make sure to hit enter)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    else:
        text_area.insert(tk.INSERT,'Starting Program\n')
#Determines the number of amino acids, used for filling in the missing data
#Extracts and combines the amino acid number, type, and its chemical shift and error from SPARTA+ pred.tab
#Since prolines lack the amide nitrogen and hydrogen, they are added in
        os.chdir(sparta_directory)
        text_area.insert(tk.INSERT,'Creating Sparta File\n')
        text_area.update_idletasks()
        from sparta_file_formatter import check_sparta_file_boundaries
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)

        text_area.insert(tk.INSERT,'Creating Peaklist File (takes a couple seconds)\n')
        text_area.update_idletasks()

        #This portion creates a list to be used later, the size of the list determines how many data points should be there
        from sparky_peaklists import compile_peaklist
        from sparky_peaklists import sequence_list
        sequence_list(seq_directory,seq_file,seq_start)
        compiled_list=compile_peaklist(NHSQC_file,NHSQC_directory,HNCA_file,HNCA_directory,HNCO_file,HNCACB_file)
#This part compares the peaklist to the SPARTA file, and only appens amino acids that are in both SPARTA and the Peaklist file
        text_area.insert(tk.INSERT,'Converting Peaklist to match Sparta\n')
        text_area.update_idletasks()
        peaklist_filtered_to_match_sparta=[]
        count=0
        for lines in compiled_list:
            modify=lines.strip()
            splitting=modify.split()
            number_search=re.search('\d+',splitting[0])
            amino_acid_search=re.search('^[A-Z]',splitting[0])
            string_to_be_searched=number_search.group(0)+amino_acid_search.group(0)+'N'
            r=re.compile(string_to_be_searched)
            comparison_to_sparta=list(filter(r.match,sparta_file_boundaries))
            if comparison_to_sparta != []:
                peaklist_filtered_to_match_sparta.append(modify)
            else:
                count+=1
                if count==6:
                    #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                    count=0
                    text_area.insert(tk.INSERT,f'{splitting[0]} was excluded\n')
#This portion calculates the RMSD. First calculates the square deviations of each amino acid with its SPARTA counterpart
#Then it sums up these deviations (once you've done all 6 atoms), if the RMSD is above the set threshold, it prints it out
        amino_acid_square_deviation_values=[]
        number=0
        for experimental,predictions in zip(peaklist_filtered_to_match_sparta,sparta_file_boundaries):
            number+=1
            experimental_split=experimental.split()
            predictions_split=predictions.split()
            square_deviation=((float(predictions_split[1])-float(experimental_split[1]))**2)/((float(predictions_split[2]))**2)
            if square_deviation>100:
                square_deviation=0
            else:
                amino_acid_square_deviation_values.append(square_deviation)
            if number%6 ==0:
                if len(amino_acid_square_deviation_values)==0:
                    continue
                else:
                    rmsd=math.sqrt((1/int(len(amino_acid_square_deviation_values)))*sum(amino_acid_square_deviation_values))
                    amino_acid_square_deviation_values.clear()
                    if rmsd>float(set_threshold):
                        text_area.insert(tk.INSERT,f'{experimental_split[0]} had a rmsd of {rmsd}\n')
                    #text_area.insert(tk.INSERT,f'rmsd={rmsd}\n')
#The compiled files can be useful to use for other SPARTA comparisons (such as determing unknowns), so they are saved for later use
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as file2:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_write2 in peaklist_filtered_to_match_sparta:
                    file2.write(stuff_to_write2+'\n')

def nmrstarrun3():
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

        acid_map = {
                  'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
                  'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
                  'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
                  'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
                  'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
                }

        os.chdir(nmrstarfile_directory)
        from sparta_file_formatter import check_sparta_file_boundaries
        from nmrstar import dict_create
        from nmrstar import fill_missing_data
        #NMRSTAR files contain a variety of information, and side chain chemical shift values
        #We only want residues with backbone N,HA,C,CA,CB,H chemical shifts
        #Additionally, NMRSTAR file amino acids numbers are not always correct (they contain additional values). Thus the user defines what the starting value should be
        #NMRSTAR uses 3 letter amino acid abbreviations, we want single-letter, the acid map is used to convert
        exctracted_and_compiled_data=[]
        with open(nmrstarfile) as file:
            for lines in file:
                modifier=lines.strip()
                extract_data_only=re.search(r'\b\d+\s+[A-Z]{3}\s+\w+\s+\w+\s+\d+\s+\d+',modifier)
                if extract_data_only is not None:
                    atom_search=extract_data_only.string
                    split_data=atom_search.split()
                    amino_acid_number=str(int(split_data[5])+int(seq_start)-1)
                    residue_type=split_data[6]
                    atom_type=split_data[7]
                    converted=acid_map[residue_type]
                    chemical_shift=split_data[10]
                    compile_data=[amino_acid_number]+[converted]+[atom_type]+[chemical_shift]
                    if atom_type in {'N', 'HA', 'CA', 'CB', 'H', 'C'}:
                        joined=' '.join(compile_data)
                        exctracted_and_compiled_data.append(joined)
        dict_create(seq_file,seq_start,seq_directory)
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)
        data_files=fill_missing_data(exctracted_and_compiled_data,seq_start)
        #The peaklist may have additional chemical shifts not present in the crystal structure, and thus sparta file
        #We filter out and create a new list containing only the residues found in the sparta file
        peaklist_filtered_to_match_sparta=[]
        count=0
        for lines in data_files:
            modify=lines.strip()
            splitting=modify.split()
            number_search=re.search('^-*\d+[A-Z]',splitting[0])
            r=re.compile(number_search.group(0))
            comparison_to_sparta=list(filter(r.match,sparta_file_boundaries))
            if comparison_to_sparta != []:
                peaklist_filtered_to_match_sparta.append(modify)
            else:
                count+=1
                if count==6:
                    #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                    count=0
                    text_area.insert(tk.INSERT,f'{splitting[0]} was excluded\n')
        #RMSD values are calculated summing the deviations of the experimental with predicted values, and dividing it by the number of atoms used in the calculation
        amino_acid_square_deviation_values=[]
        number=0
        for experimental,predictions in zip(peaklist_filtered_to_match_sparta,sparta_file_boundaries):
            number+=1
            experimental_split=experimental.split()
            predictions_split=predictions.split()
            square_deviation=((float(predictions_split[1])-float(experimental_split[1]))**2)/((float(predictions_split[2]))**2)
            if square_deviation>100:
                square_deviation=0
            else:
                amino_acid_square_deviation_values.append(square_deviation)
            if number%6 ==0:
                if len(amino_acid_square_deviation_values)==0:
                    continue
                else:
                    rmsd=math.sqrt((1/int(len(amino_acid_square_deviation_values)))*sum(amino_acid_square_deviation_values))
                    amino_acid_square_deviation_values.clear()
                    if rmsd>float(set_threshold):
                        text_area.insert(tk.INSERT,f'{experimental_split[0]} had a rmsd of {rmsd}\n')
        #Both files are saved for use in other programs
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as file2:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_write2 in peaklist_filtered_to_match_sparta:
                    file2.write(stuff_to_write2+'\n')

def nmrstarrun2():
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

#NMRSTAR files are stored as 3 letter abbreviatons, SPARTA+ files use single letter, thus this dict will conver the 3 letter, into 1 letter
        acid_map = {
              'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
              'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
              'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
              'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
              'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
            }

        os.chdir(nmrstarfile_directory)
        exctracted_and_compiled_data=[]
        x=0
#NMRSTAR files contain a lot of into, and may have multiple formats. However all formats contain atom number, followed by amino acid type, and atom type
#If protein contains tag, it will be missing in the SPARTA+ file. However, NMRSTAR includes tags into its atom_number ocunt. Thus, the offset will take this into account.
        with open(nmrstarfile) as file:
          for lines in file:
            modifier=lines.strip()
            A=re.search(r'\d+\s+[A-Z]{3}\s+\w+\s+\w+\s+\d+',modifier)
            if A is not None:
                atom_search=A.string
                C=atom_search.split()
                amino_acid_number=str(int(C[2])+int(seq_start)-1)
                residue_type=C[3]
                atom_type=C[4]
                converted=acid_map[residue_type]
                chemical_shift=C[6]
#NMSTAR sorta atom number and atom types in different format. This converts it into the SPARTA+ format
                G=[amino_acid_number]+[converted]+[atom_type]+[chemical_shift]
#NMRSTAR files can contain carbon/hydrogen info from side chain assignment. This is used to remove them and focus exlclusively on backbone.
#As a result of this formatting tho, backbone atoms must use this nomenclature (i.e. H cannot be HN)
                if atom_type in {'N', 'HA', 'CA', 'CB', 'H', 'C'}:
                    joined=' '.join(G)
                    exctracted_and_compiled_data.append(joined)

        from sparta_file_formatter import check_sparta_file_boundaries
        from nmrstar import dict_create
        from nmrstar import fill_missing_data
        dict_create(seq_file,seq_start,seq_directory)
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)
        data_files=fill_missing_data(exctracted_and_compiled_data,seq_start)
        peaklist_filtered_to_match_sparta=[]
        count=0
        for lines in data_files:
            modify=lines.strip()
            splitting=modify.split()
            number_search=re.search('^-*\d+[A-Z]',splitting[0])
            r=re.compile(number_search.group(0))
            comparison_to_sparta=list(filter(r.match,sparta_file_boundaries))
            if comparison_to_sparta != []:
                peaklist_filtered_to_match_sparta.append(modify)
            else:
                count+=1
                if count==6:
                    #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                    count=0
                    text_area.insert(tk.INSERT,f'{splitting[0]} was excluded\n')

        amino_acid_square_deviation_values=[]
        number=0
        for experimental,predictions in zip(peaklist_filtered_to_match_sparta,sparta_file_boundaries):
            number+=1
            experimental_split=experimental.split()
            predictions_split=predictions.split()
            square_deviation=((float(predictions_split[1])-float(experimental_split[1]))**2)/((float(predictions_split[2]))**2)
            if square_deviation>100:
                square_deviation=0
            else:
                amino_acid_square_deviation_values.append(square_deviation)
            if number%6 ==0:
                if len(amino_acid_square_deviation_values)==0:
                    continue
                else:
                    rmsd=math.sqrt((1/int(len(amino_acid_square_deviation_values)))*sum(amino_acid_square_deviation_values))
                    amino_acid_square_deviation_values.clear()
                    if rmsd>float(set_threshold):
                        text_area.insert(tk.INSERT,f'{experimental_split[0]} had a rmsd of {rmsd}\n')
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as file2:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_write2 in peaklist_filtered_to_match_sparta:
                    file2.write(stuff_to_write2+'\n')

def sparky_to_nmrstar():
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

        acid_map = {
              'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
              'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
              'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
              'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
              'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
            }
    os.chdir(nmrstarfile_directory)
    exctracted_and_compiled_data=[]
    x=0
    with open(nmrstarfile) as file:
      for lines in file:
        modifier=lines.strip()
        A=re.search(r'\d+\s+[A-Z]{3}\s+\w+\s+\w+\s+\d+',modifier)
        if A is not None:
            atom_search=A.string
            C=atom_search.split()
            amino_acid_number=C[2]
            amino_acid_number=str(int(C[2])+int(seq_start)-1)
            residue_type=C[3]
            atom_type=C[4]
            converted=acid_map[residue_type]
            chemical_shift=C[7]
            G=[amino_acid_number]+[converted]+[atom_type]+[chemical_shift]
            if atom_type in {'N', 'HA', 'CA', 'CB', 'H', 'C'}:
                joined=' '.join(G)
                exctracted_and_compiled_data.append(joined)
    from sparta_file_formatter import check_sparta_file_boundaries
    from nmrstar import dict_create
    from nmrstar import fill_missing_data
    dict_create(seq_file,seq_start,seq_directory)
    sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)
    data_files=fill_missing_data(exctracted_and_compiled_data,seq_start)
    peaklist_filtered_to_match_sparta=[]
    count=0
    for lines in data_files:
        modify=lines.strip()
        splitting=modify.split()
        number_search=re.search('^-*\d+[A-Z]',splitting[0])
        r=re.compile(number_search.group(0))
        comparison_to_sparta=list(filter(r.match,sparta_file_boundaries))
        if comparison_to_sparta != []:
            peaklist_filtered_to_match_sparta.append(modify)
        else:
            count+=1
            if count==6:
                #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                count=0
                text_area.insert(tk.INSERT,f'{splitting[0]} was excluded\n')

    amino_acid_square_deviation_values=[]
    number=0
    for experimental,predictions in zip(peaklist_filtered_to_match_sparta,sparta_file_boundaries):
        number+=1
        experimental_split=experimental.split()
        predictions_split=predictions.split()
        square_deviation=((float(predictions_split[1])-float(experimental_split[1]))**2)/((float(predictions_split[2]))**2)
        if square_deviation>100:
            square_deviation=0
        else:
            amino_acid_square_deviation_values.append(square_deviation)
        if number%6 ==0:
            if len(amino_acid_square_deviation_values)==0:
                continue
            else:
                rmsd=math.sqrt((1/int(len(amino_acid_square_deviation_values)))*sum(amino_acid_square_deviation_values))
                amino_acid_square_deviation_values.clear()
                if rmsd>float(set_threshold):
                    text_area.insert(tk.INSERT,f'{experimental_split[0]} had a rmsd of {rmsd}\n')
    os.chdir(save_directory)
    with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as file2:
        for stuff_to_write in sparta_file_boundaries:
            file.write(stuff_to_write+'\n')
        for stuff_to_write2 in peaklist_filtered_to_match_sparta:
                file2.write(stuff_to_write2+'\n')




tk.Button(root,text='browse',command=input_file).grid(row=0,column=2)
tk.Button(root,text='browse',command=input_seq).grid(row=1,column=2)
tk.Button(root,text='browse',command=NHSQC).grid(row=2,column=2)
tk.Button(root,text='browse',command=HNCA).grid(row=3,column=2)
tk.Button(root,text='browse',command=HNCACB).grid(row=4,column=2)
tk.Button(root,text='browse',command=HNCO).grid(row=5,column=2)
tk.Button(root,text='browse',command=save_file).grid(row=6,column=2)
tk.Button(root,text='browse',command=save_file2).grid(row=7,column=2)
tk.Button(root,text='enter',command=mutation_input).grid(row=8,column=2)
tk.Button(root,text='enter',command=mutation_input2).grid(row=9,column=2)
tk.Button(root,text='enter',command=seq_number).grid(row=10,column=2)
tk.Button(root,text='enter',command=threshold).grid(row=11,column=2)
tk.Button(root,text='browse',command=nmrstar).grid(row=12,column=2)
tk.Button(root,text='Quit',command=root.quit).grid(row=15,column=1)
tk.Button(root,text='Run using SPARKY files',command=sparky_peaklist_files).grid(row=13,column=0)
tk.Button(root,text='Run using NMRSTAR V3 file',command=nmrstarrun3).grid(row=13,column=1)
tk.Button(root,text='Run using NMRSTAR V2 file',command=nmrstarrun2).grid(row=13,column=2)
tk.Button(root,text='Run using SPARKY converted NMRSTAR V3 file',command=sparky_to_nmrstar).grid(row=14,column=2)
tk.Button(root,text='Help',command=help).grid(row=14,column=0)
tk.Button(root,text='Generate SPARTA file only (for APS)',command=sparta_gen_only).grid(row=14,column=1)

root.mainloop()
#tk.mainloop()
