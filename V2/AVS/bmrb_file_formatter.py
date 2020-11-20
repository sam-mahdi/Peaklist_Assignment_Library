import os

acid_map = {
          'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
          'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
          'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
          'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
          'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
        }

desired_format=['N','HA','C','CA','CB','H']
glycine_desired=['N','HA2','HA3','C','CA','H']
def make_sequence_list(seq_file,seq_directory,seq_start):
    os.chdir(seq_directory)
    sequence_list=[]
    counter=(0+seq_start)-1
    with open(seq_file) as file:
        for line in file:
            for lines in line:
                if lines == '\n':
                    continue
                counter+=1
                sequence_list.append(f'{counter} {lines}')
    return sequence_list

def make_bmrb_list(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start):
    seq_list=make_sequence_list(seq_file,seq_directory,seq_start)
    os.chdir(sparta_directory)
    bmrb_list=[]
    for amino_acids in seq_list:
        residue_number=amino_acids.split()[0]
        residue=amino_acids.split()[1]
        if mutation_list != ():
            for mutations in mutation_list.split():
                original_amino_acid=mutations[0]
                number=mutations[1:-1]
                mutation_to=mutations[-1]
                if residue == original_amino_acid and residue_number == number:
                    residue = mutation_to
        if residue == 'G':
            for atoms in glycine_desired:
                with open(sparta_file) as file:
                    for lines in file:
                        if lines.split(',')[0] == 'comp_id':
                            continue
                        amino_acid=acid_map[lines.split(',')[0]]
                        atom=lines.split(',')[1]
                        chemical_shift=lines.split(',')[5]
                        error=lines.split(',')[6]
                        if residue == amino_acid and atoms == atom:
                            bmrb_list.append(f'{residue_number} {amino_acid} {atom} {chemical_shift} {error}')
        else:
            for atoms in desired_format:
                if residue == 'P' and atoms == 'H':
                    atoms= 'H2'
                with open(sparta_file) as file:
                    for lines in file:
                        if lines.split(',')[0] == 'comp_id':
                            continue
                        amino_acid=acid_map[lines.split(',')[0]]
                        atom=lines.split(',')[1]
                        chemical_shift=lines.split(',')[5]
                        error=lines.split(',')[6]
                        if residue == amino_acid and atoms == atom:
                            bmrb_list.append(f'{residue_number} {amino_acid} {atom} {chemical_shift} {error}')
    return bmrb_list
