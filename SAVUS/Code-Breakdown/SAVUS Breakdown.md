Here I will present a breakdown of the code for SAVUS, both for my sanity, and for anyone wishing to understand what's going on. There is a lot of reptition, especially in the nmrstar file code, so I will only cover the variations between the functions. 

The sparta file generation is the same for every function, so we will start with that here. 

#####sparta gen only#####
The first set will make a sequence list, which contains the residue and its residue number. 
```
amino_acid_count=10
sequence_list=[]
with open('seq.txt') as sequence_file:
    for amino_acid in sequence_file:
        stripped_amino_acid=amino_acid.strip().upper()
        for word in stripped_amino_acid:
            amino_acid_count+=1
            sequence_list.append(str(amino_acid_count)+word)

```
The sequence files will be formatted as such:
```
MSYQVLARKWRPQTFADVVGQEHVLTALANGLSLGRIHH
SFNALLKTL
```
Thus the first loop:
```
for amino_acid in sequence_file:
        stripped_amino_acid=amino_acid.strip().upper()
        ```
Will go line by line, and remove leading or trailing white spaces. It will also convert all letters to uppercase (peaklists and all files below only use upper case letters for residues). 
The 2nd loop:
```
for word in stripped_amino_acid:
            amino_acid_count+=1
            sequence_list.append(str(amino_acid_count)+word)
            ```
 The 2nd loop will go through the every single amino acid. Rather than using a residue number list, one is instead generated with amino_acid_count. The user inputs the starting residue number, and it simply adds upon that. This is then concatenated with the amino acid to give a singular output. ```1Y```` Thus, now we have a sequence list we can later use to indicate which amino acids in the sparta file we want to use. 
 
 
 The next set is doing a variety of things. It is extracting the requried parameters from sparta, in addition to filling in missing info for prolines. 
 ```
 counter=0
y=0
sparta_file_list1=[]
sparta_file_list2=[]
with open('sparta_pred.tab') as sparta_predictions:
    for line in sparta_predictions:
        modifier=line.strip().upper()
        print(modifier)
        if re.findall('^\d+',modifier):
            A=modifier.split()
            print(A)
            del A[5:8]
            del A[3]
            A[0:3]=["".join(A[0:3])]
            joined=" ".join(A)
            sparta_file_list1.append(joined)
            proline_searcher=re.search('\BP',joined)
            if proline_searcher==None:
                continue
            else:
                y+=1
                if y==4:
                    proline_count=re.search('^\d+',joined)
                    sparta_file_list1.append(f'{proline_count.group(0)}PN'+' 1000'+' 1000')
                    sparta_file_list1.append(f'{proline_count.group(0)}PHN'+' 1000'+' 1000')
                    y=0
```
Sparta file outputs have a variety of info in the header prior to getting to the predicition values. 
```
REMARK SPARTA+ Protein Chemical Shift Prediction Table
REMARK  
REMARK  All chemical shifts are reported in ppm:
REMARK  
REMARK  SHIFT    is the predicted chemical shift.
REMARK  SS_SHIFT is the predicted secondary chemical shift.
REMARK  RC_SHIFT is the random coil chemical shift.
REMARK  HM_SHIFT is the ring current shift; a correction
REMARK           of 0.6 times this value is applied.
...
   3    Y   HA     0.000     4.561     4.550     0.018     0.000     0.201

```
This is is stuff we don't want. However, we know the lines with our data will start with a residue number. Thus, the first loop goes through the sparta file line by line, and then a regex value is used to only extract the lines that start with a number (our data). 
```
with open('sparta_pred.tab') as sparta_predictions:
    for line in sparta_predictions:
        modifier=line.strip().upper()
        if re.findall('^\d+',modifier):
        ````
Additionally, the leading/trailing white lines are removed (otherwise the lines would all start with white spaces instead of numbers). 
The sparta prediction have a variety of info, from errors, to a range of chemical shift values, etc. We only care about 1 chemical shift value, the residue number, residue type, and atom type. 
```
 3    Y   HA     0.000     4.561     4.550     0.018     0.000     0.201
```
Thus we split the string into its various elements, and extract only those parameters.
```
A=modifier.split()
            del A[5:8]
            del A[3]
            A[0:3]=["".join(A[0:3])]
            joined=" ".join(A)
            sparta_file_list1.append(joined)
            ```
            
 Gives the output:
 ```
 ['368', 'P', 'CB', '0.000', '31.693', '31.700', '-0.012', '0.000', '0.726']
 ```
 Additionally, we want to combine the residue type, number, and atom type but have it seperate from the chemical shift value ```3YHA 4.561```
 This is achieved by first joining ```A[0:3)]```, but keeping it as a list. Then combining the rest of the elements (at this point only the chemical shift) by a space. Then appending this value to your list. Thus the next results is:
 ```
 3YHA 4.561 0.201
3YC 175.913 1.272
3YCA 58.110 1.940
```
Additionally, prolines lack the amide hydrogen. Thus you won't have chemical shifts for the amide nitrogen and hydrogen. For each line we do a regex search for P, and if we find it (indicating a proline) we want to add a placeholder. This is because all below functions assume you have 6 atom types for every amino acid (N,HA,C,CA,CB). It simplifies calculations. While we have a proline, we don't want to add our placeholders everytime a proline is detected (since proline has 4 atom types, it will add our placeholder 4 times, when we only want it added once). To get around this, a counter is simply place. So that only when 4 prolines are found, it adds our placeholder (thus the placeholder is only added once, at the end). 
```
proline_searcher=re.search('\BP',joined)
            if proline_searcher==None:
                continue
            else:
                y+=1
                if y==4:
                    proline_count=re.search('^\d+',joined)
                    sparta_file_list1.append(f'{proline_count.group(0)}PN'+' 1000'+' 1000')
                    sparta_file_list1.append(f'{proline_count.group(0)}PHN'+' 1000'+' 1000')
                    y=0
```
We also want to account for mutations as well. If your protein has a mutation that is not present in the crystal structure, it will give an artificially high rmsd value. As a result, we wish to replace these mutated amino acids, with placeholders of the appropriate mutation residue type. Additionally, we will be using the peaklist to filter out what will be kept and what isn't. The seuence used will have the mutation, thus to include all the amino acids, the sparta file sequence must match the sequence file. 

```
if mutation_list1==() or mutation_list2==():
            for amino_acids in sparta_file_list1:
                sparta_file_list2.append(amino_acids)
        else:
            for mutations,mutations2 in zip(mutation_list1,mutation_list2):
                for amino_acids in sparta_file_list1:
                    if re.findall(mutations,amino_acids):
                        splitting=amino_acids.split()
                        mutation=re.sub(mutations,mutations2,splitting[0])
                        mutation_value=re.sub('\d+.\d+',' 1000',splitting[1])
                        mutation_value2=re.sub('\d+.\d+',' 1000',splitting[2])
                        mutation_replacement=mutation+mutation_value+mutation_value2
                        sparta_file_list2.append(mutation_replacement)
                    else:
                        sparta_file_list2.append(amino_acids)
                        
```                        
The way this is done is the original mutation is first defined by the user ```mutation_list1``` and then what that amino acid was mutated to is defined next ```mutation_list2```
There many be multiple mutations, so we want to loop through each mutation first. ```for mutations,mutations2 in zip(mutation_list1,mutation_list2):``` Then we want to loop through every amino acid, and if you find the amino acid using regex, you split the string into its individual values. Thus, if mutation is R133A: the split output would be:
```
['133RN', '122.819', '2.211']
['133RHA', '3.837', '0.240']
['133RC', '178.156', '1.144']
['133RCA', '59.329', '0.992']
['133RCB', '29.636', '0.869']
['133RHN', '8.828', '0.462']
```
Thus we use re.sub to change the original mutation, to the mutated version. And the other values are replaced by the placeholder, 1000. These are individual actions. Thus, these replacements are then all added, and appended to the list. 

Now that are sparta file is complete with its modifications, we can filter it to only include the amino acids within our sequence. Often times crystal structures will have multiple chains, different domains, etc. We only want to focus on the domain/section that our data includes. We will be using the sequence_list created above to define this. 

```
sparta_file_list3=[]
for aa in sparta_file_list2:
    modifiers=aa.strip()
    splitter=modifiers.split()
    searcher=re.search('^\d+[A-Z]',splitter[0])
    compiler=re.compile(searcher.group(0))
    sparta_sequence_comparison=list(filter(compiler.match,sequence_list))
    if sparta_sequence_comparison != []:
        sparta_file_list3.append(aa)
```
Each amino acid is split into its individual components (Y3HA and chemical shift value). Then you take the amino acid (Y3) and go through your sequence_list created above to see if you find a match. If you do, then you make a new list with that amino acid. If you don't, that line is ignored. In this manner, only the amino acids that are contained in your sequence list will be used for calculations. And the rest ignored. 

The very start of the crystal structure for many amino acids will only contain 4 amino acids:
```
   3    Y   HA     0.000     4.561     4.550     0.018     0.000     0.201
   3    Y    C     0.000   175.913   175.900     0.021     0.000     1.272
   3    Y   CA     0.000    58.110    58.100     0.017     0.000     1.940
   3    Y   CB     0.000    38.467    38.460     0.011     0.000     1.050
```
This causes issues with the rule of 6 we are using for everything below. To determine if this is also the case in our sparta list, we go through every amino acid, and keep a list of its residue number. 
```
temp_list=[]
temp_counter=0
for checker in sparta_file_list3:
    temp_modifier=checker.strip()
    temp_split=temp_modifier.split()
    temp_finder=re.search('^\d+',temp_split[0])
    temp_list.append(temp_finder.group(0))
    temp_counter+=1
    if temp_counter==5:
        if int(temp_finder.group(0))==int(temp_list[0]):
            break
        else:
            del sparta_file_list3[0:4]
            break
```
We use regex to extract the residue number, store it in a list, and we do this for 5 more amino acids. Since each amino acid should have 6 values, the 6th value should be identical to the 1st (since the sparta file is N,HA,C,CA,CB,HN 3YN will be the 1st, 3YHN will be the last, same number, so no need to remove anything). In our above example however, 3Y only has 4 atoms, thus when you reach the 5, you will have a different amino acid. Thus, these first 4 amino acids are removed. 

The same is true for the last amino. It will be lacking the carbonyl carbon. Thus, we do a final check, if the sparta file is not divisible by 6 at this point, that means the last amino acid lacks that carbonyl, thus the last 5 amino acids are removed. 

```
if len(sparta_file_list3)%6 != 0:
    del sparta_file_list3[-5:-1]
```
Now we have our properly formatted sparta prediction file for our protein. 


########Peaklist compiler (fun)######
The first thing we want to do is create a dictionary of amino acids that match to their corresponding residue number. This is going to be used later when we fill in the gaps in our data with placeholders. We want the placeholders to have the proper residue number and type. 

```
os.chdir(seq_directory)
        list2=[]
        x=(0+seq_start)-1
        dict={}
        with open(seq_file) as sequence_file:
            for line in sequence_file:
                B=line.strip().upper()
                for word in B:
                    x+=1
                    dict[x]=word
                    list2.append(x)

```
                    
            
Again, the same philosophy as in the sparta file list. Except now we are making a dictionary where the residue numbers key is the single letter amino acid abbreviation. 

Now we want to compile all our preaklists into 1, with the proper format. And fill in the missing information. There are many ways to do this. I decided to use the NHSQC as the base template, since if you don't have the amide value for it, you probably don't have enough information to calculate the rmsd for it (yes, this technique does get rid of data for any unassigned peaks where their ca/cb and carbonyl data may exist via i-1). This does not happen if you use the NMRSTAR files, so if you have major gaps in data, it might be best to just use that format than individual peaklists. Additionally, prolines lack the amide as well, so they are also ignored. 

```
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
```
A number of things are going on here, so we'll break it down. The peaklists may have a number of peaks unnassigned, thus they'll have ?-? as a label:
```
              ?-?    119.954      8.076 
           Y3N-HN    121.699      7.992 
           Q4N-HN    121.973      8.343 
```
We use a regex search to first eliminate that, and only focus on the assigned peaks. What
