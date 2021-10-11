import re
import math
import tkinter as tk

iteration=0

acid_map = {
          'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
          'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
          'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
          'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
          'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
        }

def filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area):
    global iteration
    iteration+=1
    peaklist_filtered_to_match_sparta=[]
    count=0
    for lines in data_files:
        number_search=re.search('^(\d+)\s+([A-Z]+)',lines)
        try:
            atom=acid_map[number_search.group(2)]
        except:
            atom=number_search.group(2)
        number_atom=(number_search.group(1)+' '+atom)
        r=re.compile(number_atom)
        comparison_to_sparta=list(filter(r.match,sparta_file_boundaries))
        if comparison_to_sparta != []:
            peaklist_filtered_to_match_sparta.append(lines.strip())
        else:
            count+=1
            if count==6:
                #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                count=0
                if iteration > 1:
                    continue
                text_area.insert(tk.INSERT,f"{number_atom} was excluded\n")
    return peaklist_filtered_to_match_sparta

def RMSD_calc(set_threshold,sparta_file_boundaries,data_files,text_area):
    experimental_list=filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area)
    amino_acid_square_deviation_values=[]
    number=0
    for experimental,predictions in zip(experimental_list,sparta_file_boundaries):
        number+=1
        experimental_data=experimental.split()[3]
        predictions_data=predictions.split()[3]
        predictions_error=predictions.split()[4]
        square_deviation=((float(predictions_data)-float(experimental_data))**2)/((float(predictions_error))**2)
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
                    text_area.insert(tk.INSERT,f"{' '.join(experimental.split()[0:2])} had a rmsd of {rmsd}\n")
