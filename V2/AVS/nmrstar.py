import re
import os
import tkinter as tk

check_list=['H','N','C']
desired_format=['N','HA','C','CA','CB','H']
glycine_desired=['N','HA2','HA3','C','CA','H']

def format_order(items):
    number, residue, atom,shift = items.split()
    return (desired_format.index(atom), number, residue, shift)

def format_order_glycine(items):
    number, residue, atom,shift = items.split()
    return (glycine_desired.index(atom), number, residue, shift)

def check(nmrstarfile,text_area):
    regex_search=''
    residues=0
    amino_acids=0
    atoms=0
    shifts=0
    with open(nmrstarfile) as file:
        for lines in file:
            if re.search('^\d+\s+\.\s+\d+\s+\d+\s+\d+',lines.strip()) is not None:
                if lines.strip().split()[8] not in check_list:
                    break
                else:
                    text_area.insert(tk.INSERT,'NMRSTAR V3 Detected\n')
                    text_area.update_idletasks()
                    regex_search='^\d+\s+\.\s+\d+\s+\d+\s+\d+'
                    residues=19
                    amino_acids=6
                    atoms=7
                    shifts=10
                    break
    with open(nmrstarfile) as file:
        for lines in file:
            if re.search('^\d+\s+\d+\s+\d+\s+[A-Z]{3}\s+\w+\s+[A-Z]\s+\d+\.\d+',lines.strip()) is not None:
                if lines.strip().split()[5] not in check_list:
                    break
                else:
                    text_area.insert(tk.INSERT,'NMRSTAR V2 Detected\n')
                    text_area.update_idletasks()
                    regex_search='^\d+\s+\d+\s+\d+\s+[A-Z]{3}'
                    residues=1
                    amino_acids=3
                    atoms=4
                    shifts=6
                    break
    with open(nmrstarfile) as file:
        for lines in file:
            if re.search('^\d+\s+\d+\s+\d+\s+[A-Z]{3}\s+\w+\s+[A-Z]\s+\d+\s+\d+\.\d+',lines.strip()) is not None:
                if lines.strip().split()[5] not in check_list:
                    break
                else:
                    text_area.insert(tk.INSERT,'SPARKY converted to NMRSTAR3.1 Detected\n')
                    text_area.update_idletasks()
                    regex_search='^\d+\s+\d+\s+\d+\s+[A-Z]{3}'
                    residues=1
                    amino_acids=3
                    atoms=4
                    shifts=7
                    break
    if shifts == 0:
        text_area.insert(tk.INSERT,'File is not the proper forma\n')
        text_area.update_idletasks()

    return nmrstar(residues,amino_acids,atoms,shifts,regex_search,nmrstarfile)





def nmrstar(residues,amino_acids,atoms,shifts,regex_search,nmrstarfile):
    temp_list=[]
    list_containing_desired_atoms=[]
    list_in_proper_format=[]
    counter=0
    with open(nmrstarfile) as file:
        for lines in file:
            if re.search(regex_search,lines.strip()) is not None:
                counter+=1
                residue_number=lines.strip().split()[residues]
                amino_acid=lines.strip().split()[amino_acids]
                atom_type=lines.strip().split()[atoms]
                chemical_shift=lines.strip().split()[shifts]
                if counter < 2:
                    temp_list.append(f'{residue_number} {amino_acid} {atom_type} {chemical_shift}')
                    continue
                if residue_number != temp_list[0].split()[0]:
                    if temp_list[0].split()[1] == 'GLY':
                        for entries in temp_list:
                            atom_in_list=entries.split()[2]
                            if atom_in_list in glycine_desired:
                                list_containing_desired_atoms.append(entries)
                        for values in glycine_desired:
                            missing_flag=True
                            for entry in list_containing_desired_atoms:
                                number=entry.split()[0]
                                residue=entry.split()[1]
                                atom=entry.split()[2]
                                if values == atom:
                                    missing_flag=False
                            if missing_flag is True:
                                list_containing_desired_atoms.append(f'{number} {residue} {values} 1000.00')
                        list_in_proper_format+=sorted(list_containing_desired_atoms,key=format_order_glycine)
                        temp_list.clear()
                        list_containing_desired_atoms.clear()
                    else:
                        for entries in temp_list:
                            atom_in_list=entries.split()[2]
                            if atom_in_list in desired_format:
                                list_containing_desired_atoms.append(entries)
                        for values in desired_format:
                            missing_flag=True
                            for entry in list_containing_desired_atoms:
                                number=entry.split()[0]
                                residue=entry.split()[1]
                                atom=entry.split()[2]
                                if values == atom:
                                    missing_flag=False
                            if missing_flag is True:
                                list_containing_desired_atoms.append(f'{number} {residue} {values} 1000.00')
                        list_in_proper_format+=sorted(list_containing_desired_atoms,key=format_order)
                        temp_list.clear()
                        list_containing_desired_atoms.clear()
                temp_list.append(f'{residue_number} {amino_acid} {atom_type} {chemical_shift}')
    return list_in_proper_format

acid_map = {
          'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
          'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
          'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
          'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
          'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
        }

def make_sequence_list(seq_file,seq_start,seq_directory):
    sequence_list=[]
    counter=(0+seq_start)-1
    os.chdir(seq_directory)
    with open(seq_file) as file:
        for line in file:
            for lines in line:
                if lines == '\n':
                    continue
                counter+=1
                sequence_list.append(f'{counter} {lines}')
    return sequence_list

def fill_in_missing_data(seq_file,nmrstarfile,seq_start,text_area,seq_directory):
    counter=0
    sequence_list=make_sequence_list(seq_file,seq_start,seq_directory)
    check_output=check(nmrstarfile,text_area)
    completed_list=[]
    for values in sequence_list:
        number=values.split()[0]
        for entry in check_output:
            residue_number=entry.split()[0]
            residue=acid_map[entry.split()[1]]
            if int(number) > int(residue_number):
                continue
            if values == residue_number+' '+residue:
                counter+=1
                if counter < 6:
                    completed_list.append(entry)
                if counter == 6:
                    completed_list.append(entry)
                    counter=0
                    break
            else:
                for items in desired_format:
                    completed_list.append(f'{values} {items} 1000.00')
                break
    return completed_list
