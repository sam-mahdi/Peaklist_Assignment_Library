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
    sparta_file_list1=[]
    proline_counter=0
    with open(sparta_file) as sparta_predictions:
        for line in sparta_predictions:
            modifier=line.strip().upper()
            if re.findall('^\d+',modifier):
                A=modifier.split()
                del A[5:8]
                del A[3]
                A[0:3]=["".join(A[0:3])]
                joined=" ".join(A)
                proline_searcher=re.search('\BP',joined)
                if proline_searcher is not None:
                    proline_counter+=1
                    proline_count=re.search('^\d+',joined)
                    if proline_counter<2:
                        sparta_file_list1.append(f'{proline_count.group(0)}PN'+' 1000'+' 1000')
                    else:
                        if proline_counter == 4:
                            sparta_file_list1.append(joined)
                            sparta_file_list1.append(f'{proline_count.group(0)}PHN'+' 1000'+' 1000')
                            proline_counter=0
                            continue
                sparta_file_list1.append(joined)
    return sparta_file_list1

#The user may have a protein that has a mutation, causing the sequence of the sparta file to differ from theirs
#The sparta predicted value for that mutant is useless, thus it is replaced with a placeholder
def add_mutation(mutation_list1,mutation_list2,sparta_file_list1):
    sparta_file_list2=[]
    if mutation_list1==() or mutation_list2==():
        for amino_acids in format_sparta(sparta_file,sparta_directory):
            sparta_file_list2.append(amino_acids)
    else:
        for mutations,mutations2 in zip(mutation_list1,mutation_list2):
            for amino_acids in format_sparta(sparta_file,sparta_directory):
                if re.findall(mutations,amino_acids):
                    splitting=amino_acids.split()
                    mutation=re.sub(mutations,mutations2,splitting[0])
                    mutation_value=re.sub('\d+.\d+',' 1000',splitting[1])
                    mutation_value2=re.sub('\d+.\d+',' 1000',splitting[2])
                    mutation_replacement=mutation+mutation_value+mutation_value2
                    sparta_file_list2.append(mutation_replacement)
                else:
                    sparta_file_list2.append(amino_acids)
    return sparta_file_list2
#The SPARTA file may have residues beyond the scope of the users protein, those residues are filtered out
def filter_sparta_using_seq(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start):
    sparta_file_list3=[]
    sparta_comparison=create_seq_list(seq_file,seq_directory,seq_start)
    for aa in add_mutation(mutation_list1,mutation_list2,sparta_file,sparta_directory):
        modifiers=aa.strip()
        splitter=modifiers.split()
        searcher=re.search('^\d+[A-Z]',splitter[0])
        compiler=re.compile(searcher.group(0))
        sparta_sequence_comparison=list(filter(compiler.match,sparta_comparison))
        if sparta_sequence_comparison != []:
            sparta_file_list3.append(aa)

    return sparta_file_list3

#The first amino acid and last amino acid will only have 4 and 5 atom respectively, breaking the rule of 6
#If the user picks somewhere in the middle of the protein, than this is not the case, thus a check is done, and if the entire protein is not divisible by 6
#The sides are removed
def check_sparta_file_boundaries(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start):
    residue_number=[]
    number_of_residues_looped_through=0
    sparta_filtered_list=filter_sparta_using_seq(seq_file,seq_directory,mutation_list1,mutation_list2,sparta_file,sparta_directory,seq_start)
    for checker in sparta_filtered_list:
        remove_whitespace=checker.strip()
        split_values=remove_whitespace.split()
        exctract_residue_number=re.search('^\d+',split_values[0])
        residue_number.append(exctract_residue_number.group(0))
        number_of_residues_looped_through+=1
        if number_of_residues_looped_through==5:
            if int(exctract_residue_number.group(0))==int(residue_number[0]):
                break
            else:
                del sparta_filtered_list[0:4]
                break
    if len(sparta_filtered_list)%6 != 0:
        del sparta_filtered_list[-5:-1]

    return sparta_filtered_list
