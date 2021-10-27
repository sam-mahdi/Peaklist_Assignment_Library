This is the AVS Version 3 Manual

While a lot under the hood has changed, the general use of the program is still relatively similar. There are still only 3 format accepted. BMRB NMRSTAR V2 and V3, as well as the NMRSTAR 3.1 that is generated from uploading SPARKY files. 

There are 9 lines. 

Line 1 ***If Using SPARKY Peaklist Files***

This will open a new window, where one may upload SPARKY peaklist files. Currently NHSQC, HNCA, HNCACB, HNCO, HNCOCA, HBHACONH, CHSQC, CCH_TOCSY, and CCC_TOCSYs are accepted.

Peaklists should be labeled using the IUPAC for atoms. I.E. GLY HA2/HA3, ASP HB2/HB3, you may use SPARKYs dummy graph for a full list. 

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

The Seq Start line determines what number the amino acid in your sequence file is. I.E. The sequence numbering must match the peaklist numbering. If your protein has no tag, then this number would be 1. If your protein has no tag, and you are assigning a domain of your protein (i.e. first amino acid is 212 in the protien sequence), then this number would be 212. If your sequence contains the tag, make sure to include this in your number (i.e. if the tag is 5 amino acids, your sequence number would be -4). 

You may add a BMRB file for your peaks to be compared to (make sure you download and use the csv). https://bmrb.io/ref_info/csstats.php?set=full&restype=aa&output=html

Data obtained using Bruker systems has different dimensions than Varians. If you are using data that is from Bruker, make sure to check the Bruker check box in the bottom corner. This will convert your Bruker peaklist formats to Varians. If you wish to keep this format, check the "Keep" button next to it. ***Do not use Bruker and Varian files together. If you have data in both formats, convert the Bruker to Varian first, and then upload these new Varian files)***

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

***Generate Sparta File***

This will generate the pred.tab required for AVS. To run SPARTA+ on a pdb file, the pdb file must include hydrogens. If hydrogens are included (e.g. NMR Structure), then you may skip the hydrogen addition step. 

There are 3 options for this script. 

1. You may choose to truncate the pdb file, in which case you will have to define which chain, and the bounds of that chain you wish to truncate (start is where your truncated protein starts, and end is where your truncated protein ends). Make sure to click enter at each stage. You may also choose to use the entire pdb file, in which case simply leave the start, end, and chain lines blank and check the use entire PDB Structure box. 

2. You can then add hydrogens to either the entire PDB structure, or the truncated one by checking Add Hydrogens. This uses a basic pymol filling option, it does not optomize hydroxyl rotamers or reorientate ASN/GLN/HIS. You may wish to use another program (e.g. reduce from MolProbity) to add hydrogens, and upload that PDB file instead (in which case leave the Add Hydrogens unchecked). 

3. The run Sparta option is self explanatory. It will run sparta on your pdb file (truncated/full, added hydrogens or not). This *only* runs Sparta, so if Sparta+ fails, check the terminal to see what errors sparta gives out. These are errors from Sparta and not my program, so if your PDB file has an issue, it is not an issue introduced from my program. 

***Run TALOS***

This will run TALOS+ on an AVS generated NMRSTAR file. To run TALOS, simply upload the NMRSTAR file, and click run TALOS. 

You may also display TALOS via the typical java view, or you may map out the secondary structure predictions and S2 values on a PDB file. 

To map on the PDB file, you must indicate what amino acid in the sequence to start mapping. The PDB file must be a single chain. You may truncate the PDB file using the Generate Sparta File option. ***The program assumes the TALOS prediction outputs are all in the same directory as your NMRSTAR file. Thus, you must always upload your NMRSTAR to use any of the options, even if you've already run TALOS***. 


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

****Assignment Percentage Completion****
To calculate assignment completion, upload the converted NMRSTAR file (you don't need to rerun the converter program if you have the NMRSTAR file), and sequence file (same format as for AVS)
The program will calculate heavy atoms (N,C) backbone, alpha+beta,gamma,epislon, ILVTA methyls, and an all-atom percentage. 

***Custom Percentage***
You may decide to calculate your own custom percantage. To do so, simply upload your sequence (single letter, no header/symbols) and NMRSTAR file, and click custom. 

You may assign a value to each amino acid, for the atom which you want to search. Separate each atom with a space. 
I.E.
If you want to look for backbone assignment using Nitrogen. Input the number 1 for every amino acid (except proline), and in the atom list, type 'N'. 
If you want to look for alphas and betas, type in 2 for every amino acid except glycine (type in 1 for glycine since it lacks a CB). And type in 'CA CB'

If the amino acid has no value (i.e. you wish to search for CBs, but glycine doesn't have a CB) simply leave it blank

You can search any atom you wish. It's important to note, the 'enter' option is not amino acid specific, it is atom specific. 
I.E. If you look up CG2, remember to give THR a value of 1, since it also has a CG2.

If you wish to have amino acid AND atom specific, you may use the special run. This will look at any amino acid which has a value, using the specified atoms. 
I.E. If you want to know how many CG1 of Valines you've assigned (and not other CG1 such as LEU), add a value of 1 only to VAL, and type CG1 into the atom list. 

You may search multiple atoms for multiple amino acids. 
I.E. CG1 CG2 CD1 CD2 for VAL, LEU, ILE can be searched (keep in mind LEU has a CG1 that is not a methyl).
