import re
import os

#This creates a sequence list that will later be used to filter residues in the sparta file outside the range we want
def create_seq_list(seq_file,seq_directory,seq_start):
    os.chdir(seq_directory)
    amino_acid_count=(0+seq_start)-1
    sequence_list=[]
    with open(seq_file) as sequence_file:
        for amino_acid in sequence_file:
            stripped_amino_acid=amino_acid.strip().upper()
            for word in stripped_amino_acid:
                amino_acid_count+=1
                sequence_list.append(str(amino_acid_count)+word)
    return sequence_list
#SPARTA files contain a lot of miscellanious info, this removes that and only extracts the residue type, number, atom type, chemical shift, and error values
#Additioanlly, prolines only contain info for 4 atom types, placeholders are set in for the nitrogen and hydrogen
def format_sparta(sparta_file,sparta_directory):
    os.chdir(sparta_directory)
    sparta_extracted_value_list=[]
    proline_counter=0
    with open(sparta_file) as sparta_predictions:
        for line in sparta_predictions:
            if re.findall('^\d+',line.strip()):
                residue_number=line.strip().split()[0]
                amino_acid=line.strip().split()[1]
                atom_type=line.strip().split()[2]
                chemical_shift=line.strip().split()[4]
                error=line.strip().split()[-1]
                new_line=f'{residue_number} {amino_acid} {atom_type} {chemical_shift} {error}'
                if amino_acid == 'P':
                    proline_counter+=1
                    if proline_counter<2:
                        sparta_extracted_value_list.append(f'{residue_number} P N'+' 1000.00'+' 1000.00')
                    else:
                        if proline_counter == 4:
                            sparta_extracted_value_list.append(new_line)
                            sparta_extracted_value_list.append(f'{residue_number} P HN'+' 1000.00'+' 1000.00')
                            proline_counter=0
                            continue
                sparta_extracted_value_list.append(new_line)
    return sparta_extracted_value_list

#The user may have a protein that has a mutation, causing the sequence of the sparta file to differ from theirs
#The sparta predicted value for that mutant is useless, thus it is replaced with a placeholder
def add_mutation(mutation_list,sparta_file,sparta_directory):
    sparta_mutations_added_list=[]
    counter=0
    if mutation_list==():
        for amino_acids in format_sparta(sparta_file,sparta_directory):
            sparta_mutations_added_list.append(amino_acids)
    else:
        for mutations in mutation_list.split():
            original_amino_acid=mutations[0]
            new_amino_acid=mutations[-1]
            residue_number=mutations[1:-1]
            for amino_acids in format_sparta(sparta_file,sparta_directory):
                if amino_acids in sparta_mutations_added_list:
                    continue
                if residue_number + original_amino_acid == ''.join(amino_acids.split()[0:2]):
                    split_line_to_list=amino_acids.split()
                    split_line_to_list[1] = new_amino_acid
                    sparta_mutations_added_list.append(f"{' '.join(split_line_to_list[0:3])} 1000 1000")
                    counter+=1
                    if mutations == mutation_list.split()[-1]:
                        counter=0
                    if counter == 6:
                        counter=0
                        break
                elif residue_number == amino_acids.split()[0]:
                    continue
                else:
                    sparta_mutations_added_list.append(amino_acids)
    return sparta_mutations_added_list
#The SPARTA file may have residues beyond the scope of the users protein, those residues are filtered out
def filter_sparta_using_seq(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start):
    sparta_filtered_list=[]
    sparta_comparison=create_seq_list(seq_file,seq_directory,seq_start)
    for amino_acid in add_mutation(mutation_list,sparta_file,sparta_directory):
        residue_number=amino_acid.strip().split()[0]
        amino_acid_type=amino_acid.strip().split()[1]
        compiler=re.compile((residue_number+amino_acid_type))
        sparta_sequence_comparison=list(filter(compiler.match,sparta_comparison))
        if sparta_sequence_comparison != []:
            sparta_filtered_list.append(amino_acid)      
    return sparta_filtered_list

#The first amino acid and last amino acid will only have 4 and 5 atom respectively, breaking the rule of 6
#If the user picks somewhere in the middle of the protein, than this is not the case, thus a check is done, and if the entire protein is not divisible by 6
#The sides are removed
def check_sparta_file_boundaries(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start):
    residue_number=[]
    number_of_residues_looped_through=0
    sparta_filtered_list=filter_sparta_using_seq(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
    for checker in sparta_filtered_list:
        residue_number.append(checker.strip().split()[0])
        number_of_residues_looped_through+=1
        if number_of_residues_looped_through==5:
            if int(checker.strip().split()[0])==int(residue_number[0]):
                break
            else:
                del sparta_filtered_list[0:4]
                break
    if len(sparta_filtered_list)%6 != 0:
        del sparta_filtered_list[-5:]
    return sparta_filtered_list
