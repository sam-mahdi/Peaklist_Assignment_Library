from pymol import cmd, stored, math
import pymol
import os
import sys
import re

def pymol_mapS2(NMRSTAR_directory,pdb_file,pdb_directory,startaa):
    s2_only=[]
    pymol.finish_launching()
    os.chdir(pdb_directory)
    cmd.load(pdb_file)
    mol=pdb_file[0:-4]
    os.chdir(NMRSTAR_directory)
    with open('predS2.tab') as s2_file:
        for lines in s2_file:
            searcher=re.search('\d+\.\d{3}',lines)
            if searcher != None:
                if int(lines.strip().split()[0]) < int(startaa):
                    continue
                s2_only.append(searcher.group(0))
    obj=cmd.get_object_list(mol)
    cmd.alter(mol,"b=-1.0")
    counter=int(startaa)
    bfacts=[]
    for line in s2_only:
        bfact=((1/(float(line)))-float(line))/1.5
        bfacts.append(bfact)
        cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
        counter=counter+1
        cmd.show_as("cartoon",mol)
        cmd.cartoon("putty", mol)
        cmd.set("cartoon_putty_scale_min", min(bfacts),mol)
        cmd.set("cartoon_putty_scale_max", max(bfacts),mol)
        cmd.set("cartoon_putty_transform", 7,mol)
        cmd.set("cartoon_putty_radius", max(bfacts),mol)
        cmd.spectrum("b","white red", "%s and n. CA " %mol)
        cmd.ramp_new("color_bar", mol, [min(bfacts), max(bfacts)],["white","red"])
        cmd.recolor()

pymol_mapS2(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
