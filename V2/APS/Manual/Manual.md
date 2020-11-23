This is APS Version 2 Manual

Most of the program is the same, the old AG has merged with this, and the files have been split. 

This program can be used for calculating the RMSD from either SPARTA+ or the BMRB average chemical shift files generated from AVS, to assist in assigning unknown peaks. 

If you are looking for RMSD calculation option to use, or how they work, look here: https://github.com/sam-mahdi/Peaklist_Assignment_Library-PAL-/blob/master/V2/APS/Manual/Calculation_Options.MD

In short, all 3 methods should give relatively similar methods. 

***Line 1 Upload SPARTA+ or BMRB File***
These files are generated from AVS, and can be inputted as is. 

***Line 2 Chemical shift file***
The chemical shift file is simply a text file containing chemical shift values. 

You may use the file generator to generate them, use AVS to generate the portions that are assigned, or make your own ***text*** file. 
****IF YOU MAKE YOUR OWN, MAKE SURE YOU START WITH I-1 CHEMICAL SHIFTS, AND FOLLOW THE ORDER N,HA,C,CA,CB,HN OR N,HA2,HA3,CA,HN FOR GLYCINE.
ATOMS THAT DON'T HAVE CHEMICAL SHIFT VALUES, ADD VALUE 1000.00****
I.E.
```
53 GLN N 121.616
53 GLN HA 4.212
53 GLN C 1000.00
53 GLN CA 55.345
53 GLN CB 29.357
53 GLN H 8.047
54 PHE N 120.217
54 PHE HA 4.648
54 PHE C 1000.00
54 PHE CA 56.824
54 PHE CB 39.522
54 PHE H 7.956
```
You may use any format you wish. 
I.E.
```
53 GLN N 121.616
53 GLN 121.616
53 Q 121.616
Q 121.616
121.616
```
All the above format will work, just make sure the line with your chemical shift value does not also have another decimal placed number. 

```
I.E. Do not have this
123.34 43.23
```

***File Generator***
If you choose to use the file generator to make the files properly setup. Then simply input your chemical shift values starting with i-1 and moving forward. 
Do not add a header, just the chemical shift value (i.e. 123.345)
If no value, then leave blank. 
If you suspect you have a glycine, but do not have protons or specifically HA2 values, then leave CB blank but add 1000.00 in HA2 
Otherwise, for all other amino acids leave alpha hydrogen2 blank. 
Type enter after entering info for all atoms, and then add the i amino acid chemical shifts. Click enter, and add the i+1 amino acid chemical shifts. 
Continue this for all subsequent i+n entries. 
When done entering sequence of chemical shifts, click save/write file. Then upload this file for RMSD calculations. 

If you entered a value incorrectly, you may start over at any time. Just keep in mind this deletes all entries you made before (so you will have to start with i-1). 

While this program is great for assigning peaks, it can also be used to confirm your assignment. 

This program can be useful for assigning competing matches that border assigned amino acids

```
54 PHE N 120.217
54 PHE HA 4.648
54 PHE C 1000.00
54 PHE CA 56.824
54 PHE CB 39.522
54 PHE H 7.956
X N 122.52
X HA 1000.00
X C 1000.00
X CA 65.43
X CB 44.23
X H 7.55
```
VS. 
```
54 PHE N 120.217
54 PHE HA 4.648
54 PHE C 1000.00
54 PHE CA 56.824
54 PHE CB 39.522
54 PHE H 7.956
X N 122.52
X HA 1000.00
X C 1000.00
X CA 55.32
X CB 32.32
X H 8.97
```
One set may give a lower rmsd than the other (indicating which one is the i+1). The same logic may apply to the i-1. 

You may also use this to determine chains of amino acids that are connected, but the assignment is still vague. 

```
I-1 X N 121.616
I-1 X HA 4.212
I-1 X C 1000.00
I-1 X CA 55.345
I-1 X CB 29.357
I-1 X H 8.047
I X N 120.217
I X HA 4.648
I X C 1000.00
I X CA 56.824
I X CB 39.522
I X H 7.956
```

There are multiple ways to use this information to assist in assignment. 


***CH3 Shift***

This uses the direct output from CH3 shift, to calculate the RMSD between the inputted carbon and hydrogen values, to the CH3 Shift predicted values. 
RMSD values are sorted lowest to highest, and you can choose how many are displayed. 

Sometimes the CH3Shift spectra does not overlap with the CHSQC. You may use the carbon and hydrogen adjustment values to reference the CH3 Shift values to the experimental. 

Personally have not had much luck with CH3Shift, but it is there for those who may wish to use it. 
