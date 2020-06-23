This is the manual for SAC (Sparky assignment checker). This program was written in python3.7, and uses tkinter and functools.
This program checks SPARKY converted NMRSTAR files to ensure there are no peaklist errors in the file.
To run just upload your sequence, the converted NMRSTAR file, the sequence start number (what is the residue number of the first amino acid in your sequence), and the offset (the number acids in the tag). If no tag used for your protein, then leave it blank. 

If errors are found, error messages will pop up, and you will only see:
```
Run complete, if errors were found, please correct and run again. No need to reload files, simply click "Run Checker"
```
If errors are found (look below for different types of errors). **Simply correct the problem, and click run again. There is no need to reupload the file or restart the program**

The SPARKY converted NMRSTAR file is formatted:
```
    36   14   14   THR     C  C 13  174.939   0.00 0  1
    37   14   14   THR    CA  C 13   59.749   0.03 0  1
    38   14   14   THR    CB  C 13   72.258   0.00 0  1
    39   14   14   THR    HN  H  1    7.846   0.01 0  1
    40   14   14   THR     N  N 15  109.050   0.03 0  1
    41   15   15   PHE     C  C 13  177.398   0.00 0  1
    42   15   15   PHE    CA  C 13   60.558   0.04 0  1
    43   15   15   PHE    CB  C 13   38.119   0.08 0  1
    44   15   15   PHE    HN  H  1    8.730   0.00 0  1
    45   15   15   PHE     N  N 15  120.211   0.01 0  1
    46   16   16   ALA     C  C 13  177.778   0.00 0  1
    47   16   16   ALA    CA  C 13   54.058   0.03 0  1
    48   16   16   ALA    CB  C 13   18.595   0.03 0  1
    49   16   16   ALA    HN  H  1    7.979   0.00 0  1
    50   16   16   ALA     N  N 15  119.482   0.01 0  1
 ```
 This program breaks this down into 4 values:
 ```
 14   THR     C  174.393 
 ```
 The residue number, residue type, atom type, and chemical shift. 
 This program checks for 3 errors:
 1. Improperly assigned residue number. 
 2. Improperly assigned residue type. 
 3. Improperly assigned atom type. 
 
The SPARKY converter compiles info from all the peaklists, thus, even if the peaks are properly labeled in the NHSQC, HNCA, and HNCACB, if they are improperly assigned in the HNCO then an error may pop up. Thus, if SAC does give an error, even if you correct your SPARKY converted file, it is recommended you check the peaklist of every experiment to find and correct the problem there as well. 

If a residue number is improperly labeled:
```
    36   14   14   THR     C  C 13  174.939   0.00 0  1
    37   14   14   THR    CA  C 13   59.749   0.03 0  1
    38   14 **15** THR    CB  C 13   72.258   0.00 0  1
    39   14   14   THR    HN  H  1    7.846   0.01 0  1
    40   14   14   THR     N  N 15  109.050   0.03 0  1
    41   15   15   PHE     C  C 13  177.398   0.00 0  1
    42   15   15   PHE    CA  C 13   60.558   0.04 0  1
    43   15   15   PHE    CB  C 13   38.119   0.08 0  1
    44   15   15   PHE    HN  H  1    8.730   0.00 0  1
    45   15   15   PHE     N  N 15  120.211   0.01 0  1
```
You will receive this type of error:
```
Error in residue 14T-HN 7.846

 Either residue number or atom type is assigned incorrectly. Check assignments and change accordingly
```
The error message will indicate which amino acid is imporperly assigned. 

If the residue type is imporperly assigned:
```
    36   14   14   THR     C  C 13  174.939   0.00 0  1
    37   14   14   THR    CA  C 13   59.749   0.03 0  1
    38   14   14   THR  **CA**C 13   72.258   0.00 0  1
    39   14   14   THR    HN  H  1    7.846   0.01 0  1
    40   14   14   THR     N  N 15  109.050   0.03 0  1
    41   15   15   PHE     C  C 13  177.398   0.00 0  1
    42   15   15   PHE    CA  C 13   60.558   0.04 0  1
    43   15   15   PHE    CB  C 13   38.119   0.08 0  1
    44   15   15   PHE    HN  H  1    8.730   0.00 0  1
    45   15   15   PHE     N  N 15  120.211   0.01 0  1
```
You will receive a similar error message:
```
Error in residue 14T-C 1000

 Either residue number or atom type is assigned incorrectly. Check assignments and change accordingly
```
If you have an error in the residue type:
```
    36   14   14   THR     C  C 13  174.939   0.00 0  1
    37   14   14   THR    CA  C 13   59.749   0.03 0  1
    38   14   14 **PHE**  CB  C 13   72.258   0.00 0  1
    39   14   14   THR    HN  H  1    7.846   0.01 0  1
    40   14   14   THR     N  N 15  109.050   0.03 0  1
    41   15   15   PHE     C  C 13  177.398   0.00 0  1
    42   15   15   PHE    CA  C 13   60.558   0.04 0  1
    43   15   15   PHE    CB  C 13   38.119   0.08 0  1
    44   15   15   PHE    HN  H  1    8.730   0.00 0  1
    45   15   15   PHE     N  N 15  120.211   0.01 0  1
```  

You will receive this type of error message:
```
Residue 14F-CB 72.258
 is incorrect. Check residue number and change residue type accordingly
Residue 14T-HN 7.846
 is incorrect. Check residue number and change residue type accordingly
 ```
 Again indicating the amino acid that is imporperly labled. 
