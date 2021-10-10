import re
from pymol import cmd, stored, math
import pymol
import os


def read_pdb(pdb_file,start,end,chain):
    new_pdb=[]
    with open(pdb_file) as input_file:
        for lines in input_file:
            atom_lines=re.search(f'^[A-Z]{{4}}\s+\d+\s+\w+\s+[A-Z]{{3}}\s+{chain}\s+\d+',lines.strip())
            if atom_lines is not None:
                amino_acid=int(lines.strip().split()[5])
                if  amino_acid >= start and amino_acid <= end:
                    new_pdb.append(lines)
    return new_pdb

def write_new_pdb(pdb_file,start,end,chain):
    new_pdb_file=read_pdb(pdb_file,start,end,chain)
    with open('modified_'+pdb_file,'w') as file:
        for lines in new_pdb_file:
            file.write(lines+'\n')

def add_hydrogen(file):
    new_pdb_file=file
    object=str(new_pdb_file[0:-4])
    cmd.load(new_pdb_file)
    cmd.h_add(object)
    cmd.save(object+'_hydrogens_added.pdb',object)


def run_sparta(file):
    pdb_file_sparta=file
    os.system(f'sparta+ -in {pdb_file_sparta}')
