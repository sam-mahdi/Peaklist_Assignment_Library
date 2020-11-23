import math
import re
import os
import tkinter as tk


"""
Parameters

Modify CH3shift_file to be the CH3 output file with your predicted chemical shifts.

The carbon and hydrogen adjustment are for if there are any reference issues. I.E. If all the carbon or hydrogen values are shifted by a constant value, you may enter it here. If no adjustments needed, simply peek it 0.

The matches are sorted by RMSD lowest to highest. Displayed values will determine how many matches are displayed (i.e. top 5, top 10, top 20, etc.)
"""

def rmsd_calc(carbon,hydrogen,CH3shift_file,ch3_shift_directory,carbon_adjustment,hydrogen_adjustment,displayed_values,text_area):
    predict_carbon=[]
    predict_hydrogen=[]
    amino_acid_list=[]
    rmsd_list=[]
    counter=0
    os.chdir(ch3_shift_directory)
    with open(CH3shift_file) as predicted:
        for lines in predicted:
            modify_lines=lines.strip().upper().split()
            if modify_lines[0] == 'RESULT:' and modify_lines[2] != 'MET':
                counter+=1
                if counter == 3:
                    msd=(((float(predict_carbon[0])-float(carbon))**2)/(float(predict_carbon[1])**2))+(((float(predict_hydrogen[0])-float(hydrogen))**2)/(float(predict_hydrogen[1])**2))
                    rmsd=math.sqrt(msd)
                    rmsd_list.append((amino_acid_list[0],rmsd))
                    predict_carbon.clear()
                    predict_hydrogen.clear()
                    amino_acid_list.clear()
                    counter=1
                amino_acid=modify_lines[2]
                residue_number=modify_lines[4]
                atom=modify_lines[10]
                chemical_shift=modify_lines[12]
                error=modify_lines[16]
                if atom[0] == 'C':
                    predict_carbon.append(float(chemical_shift)+hydrogen_adjustment)
                    predict_carbon.append(error)
                if atom[0] == 'H':
                    predict_hydrogen.append((float(chemical_shift)+carbon_adjustment))
                    predict_hydrogen.append(error)
                    amino_acid_list.append(f'{amino_acid} {residue_number} {atom}')
    sorted_list=sorted(rmsd_list, key=lambda rmsd:rmsd[1])
    for number,values in enumerate(sorted_list):
        text_area.insert(tk.INSERT,values[0]+' '+'%.2f' % values[1]+'\n')
        if number == displayed_values:
            break
