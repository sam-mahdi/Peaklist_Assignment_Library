import re
import os
import tkinter as tk

convert_dict={}

def make_dict(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL):
    global convert_dict
    trip_aa=['ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL']
    single_aa=['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V']
    for triple,single in zip(trip_aa,single_aa):
        convert_dict[triple]=single
    amino_acid_dict={}
    for (arguments,values),aa in zip(locals().items(),single_aa):
        if values == '':
            values = 0
        amino_acid_dict[aa]=int(values)
    return amino_acid_dict

def set_count(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,sequence_file,seq_directory):
    aa_dict=make_dict(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)
    count_from_seq=0
    with open(sequence_file) as sequence_file:
        for lines in sequence_file:
            for amino_acid in lines:
                if amino_acid == '>' or amino_acid == '\n':
                    continue
                count_from_seq+=aa_dict.get(amino_acid)
    return count_from_seq

def get_assigned_count(atom_list,save_file,save_directory):
    assigned_count=0
    os.chdir(save_directory)
    with open(save_file) as file:
        for line in file:
            if re.search('^\d+',line.strip()) is None:
                continue
            atom_type=line.strip().split()[4]
            if atom_type in set(atom_list.split()):
                assigned_count+=1
    return assigned_count

def get_assigned_count_special(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory):
    aa_dict=make_dict(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL)
    assigned_count=0
    os.chdir(save_directory)
    with open(save_file) as file:
        for line in file:
            if re.search('^\d+',line.strip()) is None:
                continue
            atom_type=line.strip().split()[4]
            amino_acid_type=line.strip().split()[3]
            if atom_type in set(atom_list.split()) and aa_dict[convert_dict[amino_acid_type]] != 0:
                assigned_count+=1
    return assigned_count



def custom_assignment(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory,text_area):
    assigned=get_assigned_count(atom_list,save_file,save_directory)
    theoretical=set_count(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,sequence_file,seq_directory)
    percent_assigned=int((assigned/theoretical)*100)
    text_area.insert(tk.INSERT,f'\nPercent Assigned: {percent_assigned}%\n')

def special_assignmnet(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory,text_area):
    assigned=get_assigned_count_special(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory)
    theoretical=set_count(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,sequence_file,seq_directory)
    percent_assigned=int((assigned/theoretical)*100)
    text_area.insert(tk.INSERT,f'\nPercent Assigned: {percent_assigned}%\n')
