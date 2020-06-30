import re
import os


#The NMRSTAR file is sorted HA,C,CA,CB,H,N, we want to format it N,HA,C<CA,CB,H
#The below function stores the residue number of each amino acid, then stores the appropriate atom in the appropriate list
#Using the residue_number_list we will know when we have moved on to the next amino acids
#When you move onto the next amino acid, the previous amino acids atoms are sorted into the appropriate order
def atom_ordering(exctracted_and_compiled_data):
    sorted_atom_types=[]
    residue_number_list=[]
    hydrogen_value=[]
    nitrogen_value=[]
    side_chain_cabonyl_values=[]
    x=0
    for amino_acids in exctracted_and_compiled_data:
        splitter2=amino_acids.split()
        x+=1
        if x >= 2:
            if splitter2[0] != residue_number_list[0]:
                list_compiler=nitrogen_value+side_chain_cabonyl_values+hydrogen_value
                sorted_atom_types.append(list_compiler)
                residue_number_list.clear()
                hydrogen_value.clear()
                nitrogen_value.clear()
                side_chain_cabonyl_values.clear()
                residue_number_list.append(splitter2[0])
                if splitter2[2] == 'H':
                    hydrogen_value.append(amino_acids)
                elif splitter2[2] == 'N':
                    nitrogen_value.append(amino_acids)
                else:
                    side_chain_cabonyl_values.append(amino_acids)
            else:
                if splitter2[2] == 'H':
                    hydrogen_value.append(amino_acids)
                elif splitter2[2] == 'N':
                    nitrogen_value.append(amino_acids)
                else:
                    side_chain_cabonyl_values.append(amino_acids)
        else:
            residue_number_list.append(splitter2[0])
            if splitter2[2] == 'H':
                hydrogen_value.append(amino_acids)
            elif splitter2[2] == 'N':
                nitrogen_value.append(amino_acids)
            else:
                side_chain_cabonyl_values.append(amino_acids)
    return sorted_atom_types

#Due to the above concatenation of lists, we form a list of lists that needs to be flattened_list
#Additionally, we wish to add a hyphen between the residue number and atom type that will be used for regex later
def flatten_list(exctracted_and_compiled_data):
    flattened_list=[]
    for lists in atom_ordering(exctracted_and_compiled_data):
        for elements in lists:
            splitting=elements.split()
            joined=''.join(splitting[0:2])
            flattened_list.append(joined+'-'+splitting[2]+ ' ' + splitting[3])
    return flattened_list

#Not every residue will have a chemical shift value for every atom types
#We want to fill in placeholders for all the missing data, but maintain that N,HA,C,CA,CB,H format
#At this point, every atom will only have the 6 desired atom types, in the appropriate atom order
#Therefore, we go through every atom for each amino acid, and check to see if we have data for that atom types in the N,HA,C order
def fill_empty_data(exctracted_and_compiled_data):
    missing_values_added=[]
    atom_value_holder=[]
    count=0
    for values in flatten_list(exctracted_and_compiled_data):
        atom_find=re.search('^-*\d+[A-Z]',values)
        count+=1
        atom_value_holder.append(atom_find.group(0))
        if count == 1:
            if re.findall('-N',values) != []:
                missing_values_added.append(values+'\n')
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-N 1000\n')
                count+=1
        if count == 2:
            if re.findall('-HA',values) != []:
                missing_values_added.append(values+'\n')
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-HA 1000\n')
                count+=1
        if count == 3:
            if re.findall('-C\s',values) != []:
                missing_values_added.append(values+'\n')
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-C 1000\n')
                count+=1
        if count == 4:
            if re.findall('-CA',values) != []:
                missing_values_added.append(values+'\n')
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-CA 1000\n')
                count+=1
        if count == 5:
            if re.findall('-CB',values) != []:
                missing_values_added.append(values+'\n')
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-CB 1000\n')
                count+=1
        if count == 6:
            if re.findall('-H\s',values) != []:
                missing_values_added.append(values+'\n')
                count=0
                atom_value_holder.clear()
            else:
                missing_values_added.append(f'{atom_value_holder[0]}-H 1000\n')
                atom_value_holder.clear()
                if re.findall('-N',values) != []:
                    missing_values_added.append(values+'\n')
                    count=1
                if re.findall('-HA',values) != []:
                    missing_values_added.append(f'{atom_find.group(0)}-N 1000\n')
                    missing_values_added.append(values+'\n')
                    count=2
                if re.findall('-C',values) != []:
                    missing_values_added.append(f'{atom_find.group(0)}-N 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-HA 1000\n')
                    missing_values_added.append(values+'\n')
                    count=3
                if re.findall('-CA',values) != []:
                    missing_values_added.append(f'{atom_find.group(0)}-N 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-HA 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-C 1000\n')
                    missing_values_added.append(values+'\n')
                    count=4
                if re.findall('-CB',values) != []:
                    missing_values_added.append(f'{atom_find.group(0)}-N 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-HA 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-C 1000\n')
                    missing_values_added.append(f'{atom_find.group(0)}-CA 1000\n')
                    missing_values_added.append(values+'\n')
                    count=5
    return missing_values_added

#Glycines do not have CBs, and they have additional HA. The above script will add an CB, this creates a new list without it
def add_glycine_HA(exctracted_and_compiled_data):
    glycine_search_list=[]
    for stuff in fill_empty_data(exctracted_and_compiled_data):
        if re.findall('\BG-HA',stuff) != []:
            splitting=stuff.split()
            glycine_search_list.append(stuff)
            glycine_search_list.append(f'{splitting[0]}2 1000\n')
        elif re.findall('\BG-CB',stuff) != []:
            pass
        else:
            glycine_search_list.append(stuff)
    return glycine_search_list


#This function creates a dictionary of residue numbers to residue type, that will be used below
amino_acid_dict={}
def dict_create(seq_file,seq_start,seq_directory):
    os.chdir(seq_directory)
    x=(0+seq_start)-1
    global amino_acid_dict
    with open(seq_file) as sequence_file:
        for line in sequence_file:
            white_spaces_removed=line.strip().upper()
            for word in white_spaces_removed:
                x+=1
                amino_acid_dict[x]=word

#The above function filled in missing data only for amino acids that had some data, but were missing data for other atom types
#This fills in placeholders for amino acids that have no data for any atom type
def fill_missing_data(exctracted_and_compiled_data,seq_start):
    outskirts_added=[]
    current_amino_acid=[]
    x=0
    y=0
    for atoms in add_glycine_HA(exctracted_and_compiled_data):
        current_aa_residue_number=re.search('^-*\d+',atoms)
        outskirts_added.append(atoms)
        x+=1
        y+=1
        if x == 6:
            if len(current_amino_acid)>0:
                if int(current_aa_residue_number.group(0)) == (int(current_amino_acid[0])+1):
                    x=0
                    current_amino_acid.clear()
                    current_amino_acid.append(current_aa_residue_number.group(0))
                    pass
                else:
                    number_of_missing_amino_acid=int(current_amino_acid[0])+1
                    offset=0
                    while number_of_missing_amino_acid != int(current_aa_residue_number.group(0)):
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-H  1000\n')
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-CB 1000\n')
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-CA 1000\n')
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-C 1000\n')
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-HA 1000\n')
                        outskirts_added.insert((y+offset-6),f'{number_of_missing_amino_acid}{amino_acid_dict[number_of_missing_amino_acid]}N-HN 1000\n')
                        number_of_missing_amino_acid+=1
                        offset+=6
                    x=0
                    y+=offset
                    current_amino_acid.clear()
                    current_amino_acid.append(current_aa_residue_number.group(0))
            else:
                current_amino_acid.append(current_aa_residue_number.group(0))
                x=0
    return outskirts_added
