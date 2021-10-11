AVS Version 3

Assignment Verification using Sparta+

This program takes NMR assignments and calculates the RMSD of the assignments to either SPARTA+ or BMRB values. 
Additionally, it generates files that are in the appropriate format to be used for APS. 
A module has also been added that takes SPARKY peaklist files and converts them into NMRSTAR 3.1.

The code for AVS has been rehauled and a couple of new features have been added. 

New Features for Version 2:

1. For those proteins that don't have structures, you may now use BMRB average chemical shift values https://bmrb.io/ref_info/csstats.php?set=full&restype=aa&output=html 
2. Can now convert SPARKY peaklist files to NMRSTAR 3.1 format. This format can readily be plugged into AVS, TALOS+, and BMRB NRMSTAR conversion tools. Additionally, the program will check all entries in the various peaklists to ensure the peaklists are labeled correctly. The user may also set a standard deviation value to determine peaks are centered and aligned properly between the various spectra. BMRB comparisons may also be made to compare assigned peaks with BMRB values https://bmrb.io/ref_info/csstats.php?set=full&restype=aa&output=html
3. Mutations can now be added in their proper format
4. Can check assignment percentage progress/completion, and check individual atoms and amino acid percentage completion. 
5. Can now be run via the terminal

Version 3: 

1. New experiment options have been added (HNCACO, CBCACONH, HCCONH) and program has been slightly rewritten to easily include more if desired. 
2. Bruker dimenions vary from Varians. A converter has been added so you may now input peaklists obtained from Bruker data. You may choose to keep this converted format if you had a mixture of Bruker and Varian data. 
3. Progress bar has been added for the Sparky NMRSTAR conversion. 
4. A Sparta file generator has been added, enabling users to truncate their pdb file, add hydrogens either to the full or truncated pdb file, and run sparta on this file generating the pred.tab file needed for AVS. 
