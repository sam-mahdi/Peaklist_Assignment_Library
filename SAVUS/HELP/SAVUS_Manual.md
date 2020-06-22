This is the manual for SAVUS. This program is written in python 3.7, and uses tkinter, PIL, and webbrowser. 
The program requires a sparta prediction file, sequence file, NHSQC peaklist, HNCA peaklist, HNCACB peaklist, and the HNCO peaklist. 
The program calculates the RMSD values between the experimental values and the predicted values obtained from SPARTA+. 
The program prints the amino acids that were excluded from the calculation, and the amino acids that had RMSD values below the set threshold. 
Additionally, the program writes the modified sparta and compiled peaklist files, for use in SAPUS. 
Requirements:
1. The peaklists must be in a SPARKY format, ordered by resonance number (or NMRSTAR V2,V3, and SPARKY Converted NMRSTAR V3). 
2. The sparta file must be in the same format as the direct output of SPARTA+ (pred.tab)
3. The peaklist numbering must be identical to the number format used in the crystal structure 
4. Each file must be uploaded using the browse option. Furthermore each value must be entered by clicking enter. 

To run program, simply upload all files, fill in all the blanks (if no mutations, don't input anything), and click run. 

You may also click the generate sparta file only, this will skip the calculations and generate a sparta file for SOPUS use. To do so, simply upload the pred.tab and sequence files, indicate the sequence start number and any mutations you have, and indicate the sparta save file. 

To quick search the manual, ctrl+f search these titles for each section:

1. #SPARTA File#
2. #Sequence File#
3. #NHSQC File#
4. #HNCA/HNCACB/HNCO File#
5. #Save SPARTA and Peaklist Files#
6. #Mutations#
7. #Sequence Number Start#
8. #Threshold#
9.#NMRSTAR V2,V3, or SPARKY Converted V3#
10.#Offset#


#############SPARTA File###########

The sparta file must be the original sparta format:
```
   3    Y   HA     0.000     4.561     4.550     0.018     0.000     0.201
```
This file is obtained by using SPARTA+ on the crystal structure of your protein. The output of SPARTA+ will be pred.tab.
However, you may rename the file whatever you'd like. The program is designed to work with the direct output of SPARTA+, so no modifications are needed. 
You can load this by clicking the browse button, navigating to the folder that contains the pred.tab file, and simply clicking on it. 

#############Sequence File###########

The sequence file must be single-letter abbreviation:
```
MSYQVLAR...
```
It should be a txt file containing only the sequences (no header). I might change the script later to include seq files with headers and other variations later, but current file only accepts single-letter abbreviation with no other artifacts. **If protein contains any kind of tag, include it in the sequence**
You can load this by clicking the browse button, navigating to the folder that contains the pred.tab file, and simply clicking on it. 

#############NHSQC File###########

The NHSQC peaklist must be in the SPARKY format and sorted by resonance:
```
           Y3N-HN    121.699      7.992 
           Q4N-HN    121.973      8.343 
           V5N-HN    120.902      8.008 

```
This is designed to work with the direct SPARKY .list output. Unassigned peaks, and the header are ignored. 
Thus, no modifications are required. 
**It is important that all peaklist files are in the same folder.**
You can load this by clicking the browse button, navigating to the folder that contains the pred.tab file, and simply clicking on it.

#############HNCA/HNCACB/HNCO File###########
These peaklists must be in the SPARKY format and sorted by resonance:
```
HNCA
    Y3N-S2CA-Y3HN    121.666     58.259      7.984 
        Y3N-CA-HN    121.666     57.616      7.992 
    Q4N-Y3CA-Q4HN    121.973     57.586      8.341 

HNCACB

    Y3N-S2CA-Y3HN    121.666     58.064      7.994 
    Y3N-S2CB-Y3HN    121.690     63.849      7.995 
        Y3N-CA-HN    121.666     57.600      7.998 
        Y3N-CB-HN    121.666     38.934      7.998 
    Q4N-Y3CA-Q4HN    121.973     57.564      8.335 
    Q4N-Y3CB-Q4HN    121.973     39.059      8.337 
        Q4N-CA-HN    121.973     55.731      8.341 
        Q4N-CB-HN    121.973     30.087      8.336 

HNCO
     Y3N-S2C-Y3HN    121.666    173.775      7.997 
     Q4N-Y3C-Q4HN    121.973    175.460      8.339 
     V5N-Q4C-V5HN    120.902    175.123      8.015 
     
 ```    

This is designed to work with the direct SPARKY .list output. Unassigned peaks, and the header are ignored. 
Thus, no modifications are required. 
**It is important that all peaklist files are in the same folder.**
You can load this by clicking the browse button, navigating to the folder that contains the pred.tab file, and simply clicking on it.

#############Save SPARTA and Peaklist Files###########

The script modifies the SPARTA file to only include the amino acids within your sequence. Any other amino acids in the pred.tab will be removed. Additionally, if the portion of the sequence you are using is the start of the crystal structure, the first amino acid will be removed (since it lacks both the amide nitrogen and hydrogen). If the portion of the sequence you are using ends at the end of the crystal structure, the last amino acid will be removed (it lacks a carbonyl). Prolines have their amide nitrogen and hydrogen added (with values of 1000 given to them). The final file will only contain the residue number, residue type, atom type, predicted chemical shift, and error. 

```
4QN 123.306 2.598
4QHA 4.510 0.237
4QC 173.967 0.914
4QCA 55.623 1.065
4QCB 32.000 1.586
4QHN 8.504 0.484
```
The script modifies the peaklist file to only include the amino acids that are also included in your SPARTA+ predictions. Any other amino acids will be removed. Any amino acids that are in the SPARTA file but unassigned in the peaklist file will be added with values of 1000 given to them. Additionally, all amino acids will be given an HA with the value of 1000. The final file will only contain the residue number, residue type, atom type, and experimental chemical shift.  
```
Q4N-HN 121.973
Q4N-HA 1000
Q4C 175.123
Q4N-CA-HN 55.802
Q4N-CB-HN 30.087
Q4N-HN 8.343
```
**Use the browse button to indicate the save names of these files**

#############Mutations############

Any mutations that cause a variation in the sequenuence of the crystal structure, versus the sequence of your protein, must be accounted for. Since SPARTA+ will not contain predictions for these amino acids, the residue in the pred.tab file will be replaced with the mutation and its value will be changed to 1000. 
There are 2 entry boxes: 
One to enter in the original residue number and residue type
The other to enter in the mutated residue number and residue type

For Example:
If you have a mutated residue number 133 from an arginine to and alanine (R133A)
The first entry would be: 133R
The second entry would be: 133A

If you have a double, triple, etc. mutant, seperate these with spaces
```
133R 137Q 182Y 220N

133A 137V 182L 220A
```
**Click enter after done typing in mutations**
**If you have no mutations, leave these entries blank.** 

#############Sequence Number Start############

The sequence may be the start of the protein, it might be in the middle of the protein. It is important to specify what the residue number of the first amino acid in the sequence file is. 

If sequence is:
```
1   5    
MSYQVLAR...
```
Then enter 1
```
If sequence is:
5
VLAR...
```
Then enter 5

**Click enter to input entry**

#############Threshold############

The threshold allows you to set whatever RMSD threshold you want (2, 2.2, 2.25, 2.253, etc.). Generally, an RMSD between 2-3 means your assignment is "accurate" (assuming the crystal structure is an accurate representation of your protein). 

**Click enter to input entry**

#############NMRSTAR V2,V3, or SPARKY Converted V3############
You may now upload NMRSTAR V2 or V3 files from BMRB and SAVUS will convert them into the appropriate format for rmsd calculations with SPARTA+. SPARKY Converted V3 files are also supported, however, the nomenclature for the atoms must follow the SPARKY/NMRSTAR format (N,HA,C,CA,CB,H). 
#############Offset############
Often times a protein may contain tags, either for purification or solubility. To account for these tags, simply indicate the size of the tag (I.E. A His-Tag for pETDuet is 14 amino acids, thus the offset would be 14). 
