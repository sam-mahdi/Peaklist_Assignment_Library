from pymol import cmd, stored, math
import pymol
import os
import sys
import re

def pymol_mapSS(NMRSTAR_directory,pdb_file,pdb_directory,startaa):
    ss_dict={'L':0,'H':2,'E':1,'X':0}
    ss_only=[]
    pymol.finish_launching()
    os.chdir(pdb_directory)
    cmd.load(pdb_file)
    mol=pdb_file[0:-4]
    os.chdir(NMRSTAR_directory)
    with open('predSS.tab') as ss_file:
        for lines in ss_file:
            searcher=re.search('^\d+',lines.strip())
            if searcher != None:
                if int(lines.strip().split()[0]) < int(startaa):
                    continue
                ss_only.append(ss_dict[lines.strip().split()[8]])
    obj=cmd.get_object_list(mol)
    cmd.alter(mol,"b=-1.0")
    counter=int(startaa)
    bfacts=[]
    for line in ss_only:
        bfact=float(line)
        bfacts.append(bfact)
        cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
        counter=counter+1
        cmd.cartoon("automatic",mol)
        cmd.spectrum("b","grey blue red", "%s and n. CA " %mol)
        cmd.recolor()

pymol_mapSS(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
