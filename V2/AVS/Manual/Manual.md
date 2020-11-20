This is the AVS Version 2 Manual

While a lot under the hood has changed, the general use of the program is still relatively similar. There are still only 3 format accepted. BMRB NMRSTAR V2 and V3, as well as the NMRSTAR 3.1 that is generated from uploading SPARKY files. 

There are 9 lines. 

Line 1 ***If Using SPARKY Peaklist Files***
This will open a new window, where one may upload SPARKY peaklist files. Currently NHSQC, HNCA, HNCACB, HNCO, HNCOCA, HBHACONH, CHSQC, CCH_TOCSY, and CCC_TOCSYs are accepted. 

The sequence list must be single-letter format with no headers or symbols. 
```
MSQYSDSG
```
The peaklists themselves should be sorted in order of residue number
```
1M-N
1M-HN
2S-N
2S-HN
```
The NMRSTAR save file just designates filename and location the NMRSTAR file will be saved. 

The standard deviation value will print anything above the set value. Chemical shifts from multiple spectra are averaged, however if peaks in some spectra are not aligned or centered properly, then you will get a high deviation. Peaks should not have a deviation above 0.2

You may add a BMRB file for your peaks to be compared to (make sure you download and use the csv). https://bmrb.io/ref_info/csstats.php?set=full&restype=aa&output=html

***Output***
A series of outputs will be printed out. 

The program will go through and check the labeling first. If anything is mislabeled, it will tell you want spectra the unlabeled peak is in, and what the error is. 
It's important to note, this can take a minute or two, and interacting with the program will make it crash. Its best to let it run, and only interact when its done. 
```
Checking NHSQC
Checking HNCA
Amino Acid F43N-L42CA-S44HN nitrogen or amide is improperly labeled
```
If there is no error, you will only get a ```Checking``` output. 

If there are errors, please fix them and rerun the programs until no errors are reported. 

Then any value that is above the standard deviation will be printed. 
```
13Q-CB
['HNCACB', 'HNCACB', 'CHSQC', 'CHSQC']
[30.734, 31.061, 30.752, 30.706]
```
As can be seen, the atom for that residue is printed, and the spectrum values were obtained from as well. A printout of the values is also revealed so one can identify what spectrum the error is from and correct it. 

Finally, if the user uploads the BMRB file, a printout of assignments that are outside of their range will be printed. 
```
Comparing to BMRB Values
ALA 27 HB value 1.718 is outside of range 1.072-1.632
```
In the above example, the HB of that alanine is slightly above its usual range. There is a 5% deviation that is allowed, so you don't get values that are off by just 0.01 for example. 

The final NMRSTAR file is then made
```
loop_
    _Atom_chem_shift.ID
    _Atom_chem_shift.Comp_index_ID
    _Atom_chem_shift.Seq_ID
    _Atom_chem_shift.Comp_ID
    _Atom_chem_shift.Atom_ID
    _Atom_chem_shift.Atom_type
    _Atom_chem_shift.Atom_isotope_number
    _Atom_chem_shift.Val
    _Atom_chem_shift.Val_err
    _Atom_chem_shift.Ambiguity_code
     _Atom_chem_shift.Assigned_chem_shift_list_ID
   1   1   1 MET   CA C 13  55.496 0.07 0 1 
   2   1   1 MET   CB C 13  33.103 0.03 0 1 
   3   1   1 MET   CE C 13  17.091 0.02 0 1 
```
This can be readily inputted into multiple programs (including AVS) and run. 



***Line 2 Sparta or BMRB file***
A pred.tab file generated from sparta+ can be inputted here. If a structure of the protein is unavailable, then a csv https://bmrb.io/ref_info/csstats.php?set=full&restype=aa&output=html file can be added. Simply browse and click the desired file. 

***Line 3 Sequence File***

The sequence list must be single-letter format with no headers or symbols. 
```
MSQYSDSG
```

***Line 4 Save Sparta or BMRB file***
This will generate a Sparta or BMRB file that is in the appropriate format for APS (if you wish to use that). 

***Line 5 Save Peaklist File***
This will generate a file of your peaklists (from the NMRSTAR file you inputted) that is in the appropriate format for APS. 

***Line 6 Mutations***
If there are any variations between your sequence and the PDB file used, they can be added here. If there are multiple, simply seaparate with a space. 
```
R133A Q234T
```
***Line 7 Sequence Start***
Type in whatever the first sequence number in the provided sequence is. Make sure this coincides with the PDB file if using Sparta+. I.E. Amino acid 1 should be the same residue as whatever amino acid 1 in the PDB file is (i.E. 1M in your assignments should be 1M in the pdb). 

***Line 8 Set Threshold***
Any value above this RMSD threshold will be printed out. These RMSDs are calculated from either SPARTA+ or BMRB values depending on which option was selected. 

***Line 9 NMRSTAR Files***
This is where the peaklist is uploaded. Only 3 formats are currently accepted. BMRB NMRSTAR V2 and V3, as well as the NMRSTAR 3.1 that is generated from uploading SPARKY files.

***Button Options***
There are 4 options. 
You may calculate RMSDs from either SPARTA+ or BMRB using your experimental data. 
Or 
You may generate only the SPARTA+ or BMRB files that are in the appropriate for APS, and skip the RMSD calculations to your peaklists. 
