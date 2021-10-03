import re
import os


def convert_3D(file,directory):
    os.chdir(directory)
    header=[]
    new_order=[]
    with open(file) as nmr_file:
        for lines in nmr_file:
            if lines.strip().split() == []:
                continue
            if lines.strip().split()[0] == 'Assignment':
                header.append(lines+'\n')
                continue
            old_title=lines.strip().split()[0]
            F2_title=old_title.split('-')[0]
            F1_title=old_title.split('-')[1]
            try:
                if F1_title == 'N':
                    F1_title=re.search('[A-Z]\d+',F2_title).group(0)+'N'
                    F2_title=re.sub('[A-Z]\d+','',F2_title)
                    F3_title=old_title.split('-')[2]
                else:
                    F3_title=(re.search('[A-Z]\d+',F1_title).group(0))+old_title.split('-')[2]
            except:
                F3_title=old_title.split('-')[2]
            new_title=f'{F1_title}-{F2_title}-{F3_title}'
            F2=lines.strip().split()[1]
            F1=lines.strip().split()[2]
            F3=lines.strip().split()[3]
            new_order.append(f'{new_title}\t{F1}\t{F2}\t{F3}\n')
    return new_order

def write_varian_file(file,directory):
    pathway_and_name=os.path.join(directory,'new'+file)
    with open(pathway_and_name,'w') as new_file:
        list_to_write=convert_3D(file,directory)
        for lines in list_to_write:
            new_file.write(lines)
    return ('new'+file)

def delete_varian_file(file,directory):
    os.chdir(directory)
    os.remove(file)
