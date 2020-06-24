Here I will present a breakdown of the code for AVS, both for my sanity, and for anyone wishing to understand what's going on. There is a lot of reptition, especially in the nmrstar file code, so I will only cover the variations between the functions. 

ctrl+f search to go to a specific section:
1.#sparta gen only#
2.#Peaklist compiler (fun)#
3.#NMRSTAR V3#
4.#NMRSTAR V2# (very similar to nmrstar v3)
5.#SPARKY Converted NMRSTAR V3 files# (identical to nmrstar v2)

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
 The 2nd loop will go through the every single amino acid. Rather than using a residue number list, one is instead generated with amino_acid_count. The user inputs the starting residue number, and it simply adds upon that. This is then concatenated with the amino acid to give a singular output. ```1Y``` Thus, now we have a sequence list we can later use to indicate which amino acids in the sparta file we want to use. 
 
 
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
We use a regex search to first eliminate that, and only focus on the assigned peaks. The loop will go through every amide, and continue down to the other peaklists, however, it appends as it goes. Thus, any missing amino acids need to be added within the loop (as it goes). Thus, we have another loop setup. 
```
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
                                
```
List2 is the size of your sequence, indicating how many peaks/amino acids you should have. C is a regex that isolates the residue number. So if you have the amide for a particular amino acid, the loop is broken and it is added to the overall list. There may be instances where your sequence has values that are beyond your peaklist, if that is the case, but since we only care about the values within your peaklist, then those are removed. Otherwise, then you go to the 2nd loop. This first searches through the overall list to search for the value of a. If it finds it, it breaks the loop. This is to ensure you don't get duplicate additions (since you will go through your sequence list for every amide in your peaklist). If it doesn't find it, it adds the placeholder values using the dictionary to determine the residue type. 

The next few lines then use the amide as a base template, search through the other peaklist files using the amides residue number+type, and extract the required info. 
```
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
```

   Again, you add as you go along. First you add the Nitrogen value, or a place holder if its missing, then you add the alpha hydrogen, carbonyl carbon, alpha carbon, beta carbon, and finally the amid enitrogen. Placeholders are added at each place if the value is missing. Glycines have an HA2 and don't have an CB, as a result, a search is also done for glycines to add HA2 values, and break the loop for the CBs (since it won't be there). 
   
 Each amino acid should have its 6 values now ordered N,HA,C,CA,CB. Thus the peaklists are compiled into the proper format. The next step is to modify the peaklist files, so it only contains values within sparta. Chemical shifts for solubility tags, or other domains present in your protein but not in the crystal structure (and thus the sparta file), are removed.  
 
 ```
        for lines in list5:
            modify=lines.strip()
            splitting5=modify.split()
            number_search=re.search('\d+',splitting5[0])
            amino_acid_search=re.search('^[A-Z]',splitting5[0])
            string_to_be_searched=number_search.group(0)+amino_acid_search.group(0)+'N'
            r=re.compile(string_to_be_searched)
            comparison_to_sparta=list(filter(r.match,sparta_file_list3))
            if comparison_to_sparta != []:
                list3.append(modify)
            else:
                count+=1
                if count==6:
                    #if any amino acid is the peaklist, but not SPARTA file, it will be excluded and printed out here
                    count=0
                    text_area.insert(tk.INSERT,f'{splitting5[0]} was excluded\n')
```
The amino acids in your peaklists however are formatted residue type first, followed by residue number (Y3N), whereas in sparta they are reveresed (3YN). Thus first the peaklist factors are flipped to match sparta. Then you go through each amino acid, and search the sparta file to see if its there. If it is, they are added to the list, otherwise they are excluded and a printout to tell the user what has been excluded. Since you don't want duplicates being printed, you only print the amide hydrogen value. 

Now that the sparta file and compiled peaklist files are the same size and formatted properly, we can go through them and calculate the rmsd of each amino acid with its predicted sparta value. 

```
        list4=[]
        number=0
        for experimental,predictions in zip(list3,sparta_file_list3):
            number+=1
            splitting6=experimental.split()
            splitting7=predictions.split()
            square_deviation=((float(splitting7[1])-float(splitting6[1]))**2)/((float(splitting7[2]))**2)
            if square_deviation>100:
                square_deviation=0
            else:
                list4.append(square_deviation)
            if number%6 ==0:
                if len(list4)==0:
                    continue
                else:
                    rmsd=math.sqrt((1/int(len(list4)))*sum(list4))
                    list4.clear()
                    if rmsd>float(set_threshold):
                        text_area.insert(tk.INSERT,f'{splitting6[0]} had a rmsd of {rmsd}\n')
```
Since the sizes of the 2 files are the same. We can simply go through each, calculate the square deviation, store it in a list, and take the sum of that list to get the rmsd. The reason the placeholders were 1000 were to eliminate them from the calculations. If the square deviation is above 1000, then the value is not used for calculatons. 


#######NMRSTAR V3###########

Many other programs, including sparky, have the option to convert their files into the NMRSTAR V3 format. Additionally, the bmrb databank (which would be used for testing the script) uses NMRSTAR V3 format as well. The sparta file manipulation and rmsd calculation is the same as before in this case. So I will only cover converting NMRSTAR V3 into the sparta format. 

NMRSTAR V3 files are formatted as such:
```
Content for NMR-STAR saveframe, "assigned_chem_shift_list_1"
    save_assigned_chem_shift_list_1
   _Assigned_chem_shift_list.Sf_category                   assigned_chemical_shifts
   _Assigned_chem_shift_list.Sf_framecode                  assigned_chem_shift_list_1
   _Assigned_chem_shift_list.Entry_ID                      26909
   _Assigned_chem_shift_list.ID                            1
   _Assigned_chem_shift_list.Sample_condition_list_ID      1
   _Assigned_chem_shift_list.Sample_condition_list_label   $sample_conditions_1
   _Assigned_chem_shift_list.Chem_shift_reference_ID       1
   _Assigned_chem_shift_list.Chem_shift_reference_label    $chemical_shift_reference_1
   _Assigned_chem_shift_list.Chem_shift_1H_err             .
   _Assigned_chem_shift_list.Chem_shift_13C_err            .
   _Assigned_chem_shift_list.Chem_shift_15N_err            .
   _Assigned_chem_shift_list.Chem_shift_31P_err            .
   _Assigned_chem_shift_list.Chem_shift_2H_err             .
   _Assigned_chem_shift_list.Chem_shift_19F_err            .
   _Assigned_chem_shift_list.Error_derivation_method       .
   _Assigned_chem_shift_list.Details                       .
   _Assigned_chem_shift_list.Text_data_format              .
   _Assigned_chem_shift_list.Text_data                     .

   loop_
      _Chem_shift_experiment.Experiment_ID
      _Chem_shift_experiment.Experiment_name
      _Chem_shift_experiment.Sample_ID
      _Chem_shift_experiment.Sample_label
      _Chem_shift_experiment.Sample_state
      _Chem_shift_experiment.Entry_ID
      _Chem_shift_experiment.Assigned_chem_shift_list_IDfamily_title
      ...
      1      .   1   1   2     2     SER   HA     H   1    4.477     0.003   .   1   .   .   .   .   .   -1    Ser   HA     .   26909   1
      2      .   1   1   2     2     SER   HB2    H   1    3.765     0.001   .   1   .   .   .   .   .   -1    Ser   HB2    .   26909   1
      3      .   1   1   2     2     SER   HB3    H   1    3.765     0.001   .   1   .   .   .   .   .   -1    Ser   HB3    .   26909   1
      4      .   1   1   2     2     SER   C      C   13   173.726   0.2     .   1   .   .   .   .   .   -1    Ser   C      .   26909   1
      5      .   1   1   2     2     SER   CA     C   13   58.16     0.047   .   1   .   .   .   .   .   -1    Ser   CA     .   26909   1
      6      .   1   1   2     2     SER   CB     C   13   64.056    0.046   .   1   .   .   .   .   .   -1    Ser   CB     .   26909   1
      7      .   1   1   3     3     HIS   H      H   1    8.357     0.004   .   1   .   .   .   .   .   0     His   H      .   26909   1
      8      .   1   1   3     3     HIS   HA     H   1    4.725     0.003   .   1   .   .   .   .   .   0     His   HA     .   26909   1
      
```
There is a lot info, so our regex search and exctraction must be more stringent as before. Additionally, NMRSTAR uses 3 letter abbreviations for amino acids, instead of the 1 in sparta, and while sometimes the peaklist label will be included (-1, 0 values on the right) that is not always the case. Finally, the atoms are ordered HA, C, CA, CB, N,H instead of N,HA,C,CA,CB,H. 

```
acid_map = {
              'ASP':'D', 'THR':'T', 'SER':'S', 'GLU':'E',
              'PRO':'P', 'GLY':'G', 'ALA':'A', 'CYS':'C',
              'VAL':'V', 'MET':'M', 'ILE':'I', 'LEU':'L',
              'TYR':'Y', 'PHE':'F', 'HIS':'H', 'LYS':'K',
              'ARG':'R', 'TRP':'W', 'GLN':'Q', 'ASN':'N'
            }
        os.chdir(nmrstarfile_directory)
        final_list=[]
        x=0
        with open(nmrstarfile) as file:
          for lines in file:
            modifier=lines.strip()
            A=re.search(r'\b\d+\s+[A-Z]{3}\s+\w+\s+\w+\s+\d+\s+\d+',modifier)
            if A != None:
                atom_search=A.string
                C=atom_search.split()
                amino_acid_number=str(int(C[5])+int(seq_start)-1)
                residue_type=C[6]
                atom_type=C[7]
                converted=acid_map[residue_type]
                chemical_shift=C[10]
                G=[amino_acid_number]+[converted]+[atom_type]+[chemical_shift]
                if atom_type == 'N' or atom_type == 'HA' or atom_type =='CA' or atom_type == 'CB' or atom_type=='H' or atom_type=='C':
                    joined=' '.join(G)
                    final_list.append(joined)
```
Thus first we need a dictionary to convert the 3 letter abbreviations into one letter needs to be made. Then we go through the nmrstar file, extracting only the lines with the data. While the formats may change, you will always have a residue number, followed by 3 letter abbreviation of the residue type, followed by atom type, isotope type, and finally the chemical shift and error. The string is split into a list, the various values are extracted, moved around in the proper format, and recompiled. The residue number (amino_acid_number) may vary from the sequence. Since solubility tags or any other additions are counted as part of the protein, the numbering in the NMRSTAR file will not represent the numbering of the protein. The user indicates the first residue number, and we build from there. Finally, NMRSTAR files contain side chain data as well, but sparta does not predict those. Thus, only the backbone atoms are added. 

As stated prior, NMRSTAR atom types are formatted differently. They are stored as HA,C,CA,CB,H,N where we want them to be N,HA,C,CA,CB,H. 
```
final_list2=[]
        atom_number_list=[]
        temp_list=[]
        temp_list2=[]
        temp_list3=[]
        for amino_acids in final_list:
            splitter2=amino_acids.split()
            x+=1
            if x >= 2:
                if splitter2[0] != atom_number_list[0]:
                    list_compiler=temp_list2+temp_list3+temp_list
                    final_list2.append(list_compiler)
                    atom_number_list.clear()
                    temp_list.clear()
                    temp_list2.clear()
                    temp_list3.clear()
                    atom_number_list.append(splitter2[0])
                    if splitter2[2] == 'H':
                        temp_list.append(amino_acids)
                    elif splitter2[2] == 'N':
                        temp_list2.append(amino_acids)
                    else:
                        temp_list3.append(amino_acids)
                else:
                    if splitter2[2] == 'H':
                        temp_list.append(amino_acids)
                    elif splitter2[2] == 'N':
                        temp_list2.append(amino_acids)
                    else:
                        temp_list3.append(amino_acids)
            else:
                atom_number_list.append(splitter2[0])
                if splitter2[2] == 'H':
                    temp_list.append(amino_acids)
                elif splitter2[2] == 'N':
                    temp_list2.append(amino_acids)
                else:
                    temp_list3.append(amino_acids)
```
To do this, we go through each amino acid, and store its residue number/type into a list. Since the HA,C,CA,CB are the proper order, we keep those in one list, and keep the H and N in a seperate list. We also add an x>2 clause, since we do need a start point. When the residue number/type does not match the previous one (i.e. you have finished one amino acid and moved on to the next), then you compile the amino acids in the proper order. The lists are cleared to start anew. 

This forms a list of lists however, thus we want to flatten our list. Additionally, we want to add a hyphen, it makes seperating/extracting the atom type from residu type/number easier. 
```
final_list3=[]
        for lists in final_list2:
            for elements in lists:
                splitting=elements.split()
                joined=''.join(splitting[0:2])
                final_list3.append(joined+'-'+splitting[2]+ ' ' + splitting[3])
```
Thus we simply join the list of lists, and add a - and space in the process.

Now that we have the proper format, it's time to fill in the blanks. As before we'll need to create a dictionary of amino acids with their residue number, to fill in the blanks properly. 
```
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
We cannot use the prior technique used for compiling peaklists, since that was just going through the amide peaks, whereas the NMRSTAR file contains all the peaks. Instead we go through by atom type. 

```
        final_list4=[]
        temp_list=[]
        count=0
        for values in final_list3:
            atom_find=re.search('^-*\d+[A-Z]',values)
            count+=1
            temp_list.append(atom_find.group(0))
            if count == 1:
                if re.findall('-N',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-N'+' 1000'+'\n')
                    count+=1
            if count == 2:
                if re.findall('-HA',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-HA'+' 1000'+'\n')
                    count+=1
            if count == 3:
                if re.findall('-C\s',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-C'+' 1000'+'\n')
                    count+=1
            if count == 4:
                if re.findall('-CA',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-CA'+' 1000'+'\n')
                    count+=1
            if count == 5:
                if re.findall('-CB',values) != []:
                    final_list4.append(values+'\n')
                else:
                    final_list4.append(temp_list[0]+'-CB'+' 1000'+'\n')
                    count+=1
            if count == 6:
                if re.findall('-H\s',values) != []:
                    final_list4.append(values+'\n')
                    count=0
                    temp_list.clear()
                else:
                    final_list4.append(temp_list[0]+'-H'+' 1000'+'\n')
                    temp_list.clear()
                    if re.findall('-N',values) != []:
                        final_list4.append(values+'\n')
                        count=1
                    if re.findall('-HA',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=2
                    if re.findall('-C',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=3
                    if re.findall('-CA',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-C'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=4
                    if re.findall('-CB',values) != []:
                        final_list4.append(atom_find.group(0)+'-N'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-HA'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-C'+' 1000'+'\n')
                        final_list4.append(atom_find.group(0)+'-CA'+' 1000'+'\n')
                        final_list4.append(values+'\n')
                        count=5
```
The way this works is we know the format now is N,HA,C,CA,CB,H. Thus, every amino acid should have those 6 values in that order. So we go through each amino acid, and store the residue type/number in a list. If that amino acid has a Nitrogen, then it is added to the list, otherwise it's placeholder is added. The same for every other atom. A counter is used keep track of which atom type you currently have. I.E. If the amino acid you are looking at is HA, that means it should be count=2. That way when you add the placeholder, you can add 1 to the count, pushing it to the HA section. If you are missing the hydrogen, that means you have moved on to the next peak. That next peak could be any atom type, thus you use the count one again to determine which one it is. In this manner, the missing amino acids are filled. Additionally, by using atom type instead of residue number/type, you can keep i-1 ca/cb and prolines as well (that you couldn't when compiling the peaklists). 

However, this technique does add a CB for glycine, additionally due to the above backbone filter we first used, glycines HA2 was not transffered over. 
```
        glycine_search_list=[]
        for stuff in final_list4:
            if re.findall('\BG-HA',stuff) != []:
                splitting=stuff.split()
                glycine_search_list.append(stuff)
                glycine_search_list.append(splitting[0]+'2'+' 1000'+'\n')
            elif re.findall('\BG-CB',stuff) != []:
                pass
            else:
                glycine_search_list.append(stuff)
```            
Thus we filter for gycine, add its HA2, and exclude its CB. 

While the above added in the missing values, it only added the missing values **for amino acids that had a value**. In other words, you needed to have at least one atom type assigned. However, we still need to fill in the placeholders for amino acids with no atom types assigned. 
```
        outskirts_added=[]
        temp_outskirt_list=[]
        x=0
        y=0
        for atoms in glycine_search_list:
            A=re.search('^-*\d+',atoms)
            outskirts_added.append(atoms)
            x+=1
            y+=1
            if x == 6:
                if len(temp_outskirt_list)>0:
                    if int(A.group(0)) == (int(temp_outskirt_list[0])+1):
                        x=0
                        temp_outskirt_list.clear()
                        temp_outskirt_list.append(A.group(0))
                        pass
                    else:
                        z=int(temp_outskirt_list[0])+1
                        offset=0
                        while z != int(A.group(0)):
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-H' + ' 1000' +'\n')
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-CB' + ' 1000' +'\n')
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-CA' + ' 1000' +'\n')
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-C' + ' 1000' +'\n')
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-HA' + ' 1000' +'\n')
                            outskirts_added.insert((y+offset-6),f'{z}{dict[z]}N-HN' + ' 1000' + '\n')
                            z+=1
                            offset+=6
                        x=0
                        y+=offset
                        temp_outskirt_list.clear()
                        temp_outskirt_list.append(A.group(0))
                else:
                    temp_outskirt_list.append(A.group(0))
                    x=0
 ```
 We know each amino acid now has 6 values. Thus, we can go through each amino acid, extract its residue number, and use that to determine when you've moved on to the next amino acid in the list. When you've gone through all 6, the next amino acid should be different by a factor of 1, which would indicate you've moved on to the next amino acid. If it isn't, that means it is missing a value. However, the current loop is on the next amino acid, and we want to add our placeholder in between the prior value, and the current one, so we cannot use append. Instead, we use another counter (y) to index how many values have been added to the list. We use z to determine what the residue number should be, and add placeholders until the value of z matches the residue number of the current loop. Since you only compare values when x==6, that means we already have 6 values added to the overall list. Thus, we need to subtract 6 to our y index. Additionally, there may be multiple amino acids in a row missing. Thus, we need to offset the index by a value 6, so we continuouslly add after the other. Fnally, since indexing pushes everything to the right, we the order is reveresed (H,CB,CA...etc). 
 
 Filtering the peaklist to match sparta and RMSD are done as before. 
 
 
 
 #######NMRSTAR V2######
 NMRSTAR V2 files are formatted slightly differently:
 
 ```
         1  -1   2 SER HA   H   4.477 0.003 1
         2  -1   2 SER HB2  H   3.765 0.001 1
         3  -1   2 SER HB3  H   3.765 0.001 1
         4  -1   2 SER C    C 173.726 0.2   1
         5  -1   2 SER CA   C  58.16  0.047 1
         6  -1   2 SER CB   C  64.056 0.046 1
         7   0   3 HIS H    H   8.357 0.004 1
         8   0   3 HIS HA   H   4.725 0.003 1
         9   0   3 HIS HB2  H   3.203 0.003 2
        10   0   3 HIS HB3  H   2.996 0.005 2
        11   0   3 HIS C    C 174.33  0.2   1
```
The placement of some things is moved around or removed. However, the order of the atoms and nomenclature is the same. Thus the only real change needed is at the very start:
```
with open(nmrstarfile) as file:
          for lines in file:
            modifier=lines.strip()
            A=re.search(r'\d+\s+[A-Z]{3}\s+\w+\s+\w+\s+\d+',modifier)
            if A != None:
                atom_search=A.string
                C=atom_search.split()
                amino_acid_number=str(int(C[2])+int(seq_start)-1)
                residue_type=C[3]
                atom_type=C[4]
                converted=acid_map[residue_type]
                chemical_shift=C[6]
```
As you'll if you cmopare, the only real different is the indexing. The rest of the script is identical. 


######SPARKY Converted NMRSTAR V3 files#####

SPARKY has a built in plug in that converts your peaklists in NMRSTAR V3 files.
```
     1    2    2   SER     C  C 13  173.775   0.00 0  1
     2    2    2   SER    CA  C 13   58.210   0.05 0  1
     3    2    2   SER    CB  C 13   63.849   0.00 0  1
     4    3    3   TYR     C  C 13  175.460   0.00 0  1
     5    3    3   TYR    CA  C 13   57.593   0.02 0  1
     6    3    3   TYR    CB  C 13   38.996   0.06 0  1
     7    3    3   TYR    HN  H  1    7.993   0.00 0  1
     8    3    3   TYR     N  N 15  121.671   0.01 0  1
     9    4    4   GLN     C  C 13  175.123   0.00 0  1
    10    4    4   GLN    CA  C 13   55.776   0.05 0  1
    11    4    4   GLN    CB  C 13   30.082   0.01 0  1
    12    4    4   GLN    HN  H  1    8.339   0.00 0  1
    13    4    4   GLN     N  N 15  121.971   0.01 0  1
    14    5    5   VAL    CA  C 13   63.013   0.02 0  1
```
 However, it compiles the format similarly to nmrstar v2, instead of 3, so the indexing is still similar. Additionally, the H and N are placed differently (NMRSTAR is C,CA,CB,N,H, not H,N as in the sparky converter). But our previous script can still rearrange this in the proper format. 

```
            atom_search=A.string
            C=atom_search.split()
            amino_acid_number=C[2]
            amino_acid_number=str(int(C[2])+int(seq_start)-1)
            residue_type=C[3]
            atom_type=C[4]
            converted=acid_map[residue_type]
            chemical_shift=C[7]
```
However, outside these subtle difference, everything else is the same. Thus the nmrstar v2 and v3 scripts work the same here as well. 
            
