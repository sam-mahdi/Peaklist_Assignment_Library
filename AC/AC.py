import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import tkinter.scrolledtext as st
from tkinter import ttk
import functools
import re
import webbrowser

root = tk.Tk()
root.title('SAC')

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

ttk.Label(root,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 7)

text_area = ReadOnlyText(root,width = 40,height = 10,font = ("Times New Roman",12))

text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)

tk.Label(root, text="Sequence File").grid(row=0)
tk.Label(root, text="NMR_STAR V3 SPARKY converted File").grid(row=1)
tk.Label(root, text="Please type in what residue number the first amino acid in the sequence file is\nI.E. if the first amino acid in the sequence file is 20, type in 20\n Click enter when done").grid(row=2)
tk.Label(root, text="Offset value (if protein contains tag, indicate how many amino acids in tag e.g. His-Tag pETDeut is 14)\n If no tag, leave blank. Click enter when done. ").grid(row=3)

e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e4 = tk.Entry(root)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

seq_file=()
seq_directory=()
seq_start=()
nmrstarfile=()
nmrstarfile_directory=()
offset_value=()

def input_seq():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global seq_file
    global seq_directory
    seq_directory=os.path.dirname(fullpath)
    seq_file= os.path.basename(fullpath)
    label3=Label(root,text=fullpath).grid(row=0,column=1)

def seq_number():
    seq_input=e3.get()
    global seq_start
    seq_start=int(seq_input)
    text_area.insert(tk.INSERT,f'number entered: {seq_input} \n')

def offset_fun():
    offset_input=e4.get()
    global offset_value
    offset_value=int(offset_input)
    text_area.insert(tk.INSERT,f'Offset Value set: {offset_value} \n')

def help():
    webbrowser.open('https://github.com/sam-mahdi/SPARKY-Assignment-Tools/blob/master/SAC/Manual/Manual.md')

def nmrstar():
    fullpath = filedialog.askopenfilename(parent=root, title='Choose a file')
    global nmrstarfile
    global nmrstarfile_directory
    nmrstarfile_directory=os.path.dirname(fullpath)
    nmrstarfile= os.path.basename(fullpath)
    label8=Label(root,text=fullpath).grid(row=1,column=1)


def checker():
    text_area.delete(1.0,END)
    if seq_file == ():
        text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
    if nmrstarfile == ():
        text_area.insert(tk.INSERT,'please upload your nmrstar file (make sure to use browse)\n')
    if seq_start == ():
        text_area.insert(tk.INSERT,'please enter a seq number (make sure to hit enter)\n')
    else:
        acid_map = {
              'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
              'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
              'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
              'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
              'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
            }
        os.chdir(nmrstarfile_directory)
        final_list=[]
        x=0
        with open(nmrstarfile) as file:
          for lines in file:
            modifier=lines.strip()
            A=re.search(r'\b\d+\s+[A-Z]{3}\s+[A-Z]',modifier)
            if A != None:
                atom_search=A.string
                C=atom_search.split()
                if offset_value == ():
                    amino_acid_number=C[2]
                else:
                    amino_acid_number=str(int(C[2])-offset_value)
                residue_type=C[3]
                atom_type=C[4]
                converted=acid_map[residue_type]
                chemical_shift=C[7]
                G=[amino_acid_number]+[converted]+[atom_type]+[chemical_shift]
                if atom_type == 'N' or atom_type == 'HA' or atom_type =='CA' or atom_type == 'CB' or atom_type=='H' or atom_type=='C':
                    joined=' '.join(G)
                    final_list.append(joined)
        final_list2=[]
        atom_number_list=[]
        temp_list=[]
        temp_list2=[]
        temp_list3=[]
        for amino_acids in final_list:
            splitter2=amino_acids.split()
            x+=1
            if x >= 2:
                if splitter2[0] != atom_number_list[0]:
                    list_compiler=temp_list2+temp_list3+temp_list
                    final_list2.append(list_compiler)
                    atom_number_list.clear()
                    temp_list.clear()
                    temp_list2.clear()
                    temp_list3.clear()
                    atom_number_list.append(splitter2[0])
                    if splitter2[2] == 'H':
                        temp_list.append(amino_acids)
                    elif splitter2[2] == 'N':
                        temp_list2.append(amino_acids)
                    else:
                        temp_list3.append(amino_acids)
                else:
                    if splitter2[2] == 'H':
                        temp_list.append(amino_acids)
                    elif splitter2[2] == 'N':
                        temp_list2.append(amino_acids)
                    else:
                        temp_list3.append(amino_acids)
            else:
                atom_number_list.append(splitter2[0])
                if splitter2[2] == 'H':
                    temp_list.append(amino_acids)
                elif splitter2[2] == 'N':
                    temp_list2.append(amino_acids)
                else:
                    temp_list3.append(amino_acids)

        final_list3=[]
        for lists in final_list2:
            for elements in lists:
                splitting=elements.split()
                joined=''.join(splitting[0:2])
                final_list3.append(joined+'-'+splitting[2]+ ' ' + splitting[3])

        list2=[]
        x=(0+seq_start)-1
        dict={}
        os.chdir(seq_directory)
        with open(seq_file) as sequence_file:
            for line in sequence_file:
                B=line.strip().upper()
                for word in B:
                    x+=1
                    dict[x]=word
                    list2.append(x)
        final_list4=[]
        temp_list=[]
        count=0
        i=0
        for values in final_list3:
            atom_find=re.search('^-*\d+[A-Z]',values)
            count+=1
            temp_list.append(atom_find.group(0))
            if count == 1:
                if re.findall('-N',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-N'+' 1000'+'\n')
                    count+=1
            if count == 2:
                if re.findall('-HA',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-HA'+' 1000'+'\n')
                    count+=1
            if count == 3:
                if re.findall('-C\s',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-C'+' 1000'+'\n')
                    count+=1
            if count == 4:
                if re.findall('-CA',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-CA'+' 1000'+'\n')
                    count+=1
            if count == 5:
                if re.findall('-CB',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-CB'+' 1000'+'\n')
                    count+=1
            if count == 6:
                if re.findall('-H\s',values) != []:
                    final_list4.append(values+'\n')
                    count=0
                    temp_list.clear()
                else:
                    final_list4.append(temp_list[0]+'-H'+' 1000'+'\n')
                    temp_list.clear()
                    if re.findall('-N',values) != []:
                        final_list4.append(values+'\n')
                        count=1
                    if re.findall('-HA',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=2
                    if re.findall('-C',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=3
                    if re.findall('-CA',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-C'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=4
                    if re.findall('-CB',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-C'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-CA'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=5


        glycine_search_list=[]
        for stuff in final_list4:
            if re.findall('\BG-HA',stuff) != []:
                splitting=stuff.split()
                glycine_search_list.append(stuff)
                glycine_search_list.append(splitting[0]+'2'+' 1000'+'\n')
            elif re.findall('\BG-CB',stuff) != []:
                pass
            else:
                glycine_search_list.append(stuff)

        outskirts_added=[]
        temp_outskirt_list=[]
        x=0
        y=0
        for atoms in glycine_search_list:
            A=re.search('^-*\d+',atoms)
            outskirts_added.append(atoms)
            x+=1
            y+=1
            if x == 6:
                if len(temp_outskirt_list)>0:
                    if int(A.group(0)) == (int(temp_outskirt_list[0])+1):
                        x=0
                        temp_outskirt_list.clear()
                        temp_outskirt_list.append(A.group(0))
                        pass
                    else:
                        z=int(temp_outskirt_list[0])+1
                        offset=0
                        try:
                            while z != int(A.group(0)):
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-H' + ' 1000' +'\n')
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-CB' + ' 1000' +'\n')
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-CA' + ' 1000' +'\n')
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-C' + ' 1000' +'\n')
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-HA' + ' 1000' +'\n')
                                outskirts_added.insert((y+offset-6),f'{z}{dict[z]}-N' + ' 1000' + '\n')
                                z+=1
                                offset+=6
                        except:
                            text_area.insert(tk.INSERT,f'Error in residue {atoms}\n Either residue number or atom type is assigned incorrectly. Check assignments and change accordingly\n')
                            break
                        x=0
                        y+=offset
                        temp_outskirt_list.clear()
                        temp_outskirt_list.append(A.group(0))
                else:
                    temp_outskirt_list.append(A.group(0))
                    x=0
        i=0
        atom_check_list=[]
        for residue_type_differences in outskirts_added:
            A=re.search('[A-Z]-',residue_type_differences)
            i+=1
            if i>=2:
                if (i-1)%6 == 0:
                    atom_check_list.append(A.group(0))
                else:
                    if A.group(0) != atom_check_list[(-2+i)]:
                        atom_check_list.append(A.group(0))
                        text_area.insert(tk.INSERT,f'Residue {residue_type_differences} is incorrect. Check residue number and change residue type accordingly\n')
                    else:
                        atom_check_list.append(A.group(0))
            else:
                atom_check_list.append(A.group(0))
        text_area.insert(tk.INSERT,f'Run complete, if errors were found, please correct and run again. No need to reload files, simply click "Run Checker"\n')

tk.Button(root,text='browse',command=input_seq).grid(row=0,column=2)
tk.Button(root,text='enter',command=seq_number).grid(row=2,column=2)
tk.Button(root,text='browse',command=nmrstar).grid(row=1,column=2)
tk.Button(root,text='enter',command=offset_fun).grid(row=3,column=2)
tk.Button(root,text='Quit',command=root.quit).grid(row=4,column=1)
tk.Button(root,text='Run Checker',command=checker).grid(row=4,column=0)
tk.Button(root,text='Help',command=help).grid(row=5,column=0)
root.mainloop()

