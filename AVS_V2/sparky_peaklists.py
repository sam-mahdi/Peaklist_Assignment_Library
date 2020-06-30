import re
import os


list2=[]
dict={}
def sequence_list(seq_directory,seq_file,seq_start):
    os.chdir(seq_directory)
    global list2
    global dict
    amino_acid_count=(0+seq_start)-1
    with open(seq_file) as sequence_file:
        for line in sequence_file:
            remove_white_spaces=line.strip().upper()
            for amino_acid in remove_white_spaces:
                amino_acid_count+=1
                dict[amino_acid_count]=amino_acid
                list2.append(amino_acid_count)
#This portion compiles data from various data files into 1 list.

def compile_peaklist(NHSQC_file,NHSQC_directory,HNCA_file,HNCA_directory,HNCO_file,HNCACB_file):
    os.chdir(NHSQC_directory)
    list5=[]
    with open(NHSQC_file) as NHSQC:
        for line in NHSQC:
            modifications=line.strip().upper()
            if re.findall('^[A-Z]-*\d+[A-Z]',modifications):
    #This portion fills in any gaps in the data
                C=re.search(r'-*\d+',modifications)
                for a in list2:
                    if a == int(C.group(0)):
                        break
                    elif a>int(C.group(0)):
                        break
                    else:
                        for z in list5:
                            if re.findall(f'^[A-Z]{a}N',z):
                                break
                        else:
                            list5.append(f'{dict[a]}{a}N-HN' + ' 1000' + '\n')
                            list5.append(f'{dict[a]}{a}N-HA' + ' 1000' +'\n')
                            list5.append(f'{dict[a]}{a}N-C' + ' 1000' +'\n')
                            list5.append(f'{dict[a]}{a}N-CA' + ' 1000' +'\n')
                            list5.append(f'{dict[a]}{a}N-CB' + ' 1000' +'\n')
                            list5.append(f'{dict[a]}{a}N-HN' + ' 1000' +'\n')
                splitting1=modifications.split()
                list5.append(splitting1[0]+ ' '+ splitting1[1] + '\n')
                A=re.search(r'[A-Z]-*\d+',modifications)
                list5.append(f'{A.group(0)}N-HA'+ ' 1000' + '\n')
                glycine_search=re.search(r'^G',modifications)
                if glycine_search != None:
                    list5.append(f'{A.group(0)}N-HA2'+ ' 1000' + '\n')
                with open(HNCA_file) as HNCA,open(HNCO_file) as HNCO, open (HNCACB_file) as HNCACB:
                    for line3 in HNCO:
                        modifications3=line3.strip().upper()
                        if re.findall(f'{A.group(0)}C',modifications3):
                            splitting3=modifications3.split()
                            list5.append(f'{A.group(0)}C' + ' '+  splitting3[2]+'\n')
                            break
                    else:
                        list5.append(f'{A.group(0)}C-HN'+ ' 1000' +'\n')
                    for line2 in HNCA:
                        modifications2=line2.strip().upper()
                        if re.findall(f'{A.group(0)}N-CA',modifications2):
                            splitting2=modifications2.split()
                            list5.append(splitting2[0] + ' ' + splitting2[2]+ '\n')
                            break
                    else:
                        list5.append(f'{A.group(0)}N-CA'+ ' 1000' +'\n')
                    for line4 in HNCACB:
                        modifications4=line4.strip().upper()
                        splitting4=modifications4.split()
                        if glycine_search != None:
                            break
                        if re.findall(f'{A.group(0)}N-CB',modifications4):
                            list5.append(splitting4[0] + ' '+splitting4[2]+'\n')
                            break
                    else:
                        list5.append(f'{A.group(0)}N-CB'+ ' 1000' +'\n')
                list5.append(splitting1[0]+ ' '+ splitting1[2] + '\n')
    return list5
