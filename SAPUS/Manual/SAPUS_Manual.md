
This is the manual for SAPUS (Sparky Assignment prediction using SPARTA+). This was written in python3 and uses numpy, matplotlib, tkinter, webbrowser, and mplcursors. The program requires a modified SPARTA+ file generated from SAVUS, and a chemical shift file of your unknown assignment(s). It calculates the rmsd value of your unknown peaks with predicted SPARTA+ values to determine which amino acid your unknowns would be.   T

Requirements: 
1. SPARTA+ file must be formatted properly (use SAVUS)
2. Peaklist file formatting must match SPARTA+ formatting (you can use SAVUS for peaks you have assigned, and SAG for unknowns)

To run the program simply upload the sparta file and peaklist file to predict. Set the threshold rmsd value, and pick which calculation you want done. A list of rmsd sorted from best match to worst (low to high rmsd) will be printed, and a plot of those rmsds will be generated.

**The prediction software requires data from at least 2 amino acids. The more information, the better the match.**

To quick search the manual, ctrl+f search these titles for each section:

1. Running the program
  a)#SPARTA File#
  b)#Chemical shift File#
  c)#Set threshold#
2. Calculation Options
  a)#Diagonal Sum#
  b)#RMSD Sum#
  C)#Combined Sum#
3. How to use results to assign peaks
  a)#Use for i+1 or i-1#
  b)#Use for unknown/unassigned peaks#
  c)#Confirming Assignment of peaks#

#############SPARTA File###########
The SPARTA+ format must follow the SAVUS format. There is an option in SAVUS to only generate a SPARTA+ file. Simply upload the raw pred.tab SPARTA+ file with your sequence, indicate sequence number and any mutations in you sample that deviate from the crystal structure used for SPARTA. 

#############Chemical shift File###########
You may make your own chemical shift file, or use SAG to generate one. SAVUS also generates a compiled chemical shift file from the NHSQC, HNCA, HNCO, HNCACB peaklists that is properly formatted. To make your own, the format must follow:

```
X1N-HN 113.882
X1N-HA 1000
X1C 176.4
X1CA-HN 55.9
X1CB-HN 29.636
X1HN-HN 7.615
```
With the amino acid followed by its value, in the order of N, HA, C, CA, CB, HN. **Any atom that does not have a value must have its value input as 1000** For prolines, simply add a nitrogen and hydrogen in the proper area, and add value of 1000. 
Glycines lack CB and have 2 HAs, thus the format must follow:
```
X2N-HN 108.969
X2N-HA 1000
X2HA2-HA 1000
X2C 174.921
X2CA-HN 46.815
X2HN-HN 7.837
```
With the amino acid followed by its value, in the order of N, HA, HA2, C, CA, HN. 
**Any atom that does not have a value must have its value input as 1000**



#############Set threshold###########
Only the values that are below the rmsd threshold will be displayed. If you set your threshold too high, you'll get too many matchs. If you set your threshold too low, you might not get any matches. Usually values below 2-3 are considered acceptable. 


#############Calculation Options###########


#############Diagonal Sum###########
This method calculates the rmsd of each amino acid with every single amino acid in SPARTA. Generating an array of RMSDs. 
```
                       Q4    V5  Y6 ....Sparta amino acids  
Unknown Amino Acid 1  1.56 2.38 0.92
```
Each Amino Acid will generate an array of rmsd values.
```
                       Q4    V5  Y6 ....Sparta amino acids  
Unknown Amino Acid 1  1.56 2.38 0.92
Unknown Amino Acid 2  3.25 1.12 2.65
Unknown Amino Acid 3  0.65 3.25 1.21
```
While the rmsd match between each one may generate similar rmsd values, with multiple rmsd values being lower than the proper fit, taking a diagonal array will reduce the chances of a false postive. 
The 3 amino acids are sequential. In other words, i-2, i-1, i. As a result, the proper match will be a diagonal vector. Thus, instead of looking at the individual rmsd of each amino acid, we look at the sum of the diagonal vector for each each amino acid. 

```
                       Q4    V5  Y6 ....Sparta amino acids  
Unknown Amino Acid 1  1.56 2.38 0.92
Unknown Amino Acid 2  3.25 1.12 2.65
Unknown Amino Acid 3  0.65 3.25 1.21

Diagonal Vector 1 = 1.56, 1.12, 1.21
Diagonal Vector 2 = 2.38 2.65, ...etc. 
```
Before, unknown amino acid 1 seemed to fit Y6N, but using a diagonal vector, now we can see it is in fact Q4. The rmsd values displayed are thus the summed average of the multiple diagonal vectors within the matrix of rmsd values generated. 


#############RMSD Sum###########
Rather than compare the RMSD of one amino acid with one sparta amino acid, instead the RMSD of the entire group of amino acids is calculated with a group of SPARTA amino acids. 
```
Diagonal Sum (1 experimental with 1 predicted)

RMSD=sqrt((Nexp1-Npred1)^2/error^2+(HAexp1-HApred1)^2/error^2...)/6

where Nexp1 and HAexp1 is the nitrogen and alpha hydrogen experimental chemical shift of Unknown Amino Acid 1 and Npred1 and HApred1 is nitrogen and hydrogen chemical shift of Q4. You divide by the number of atoms used (6). 

RMSD Sum (the entire group of amino acids with a group of SPARTA amino acids)
RMSD=sqrt((Nexp1-Npred1)^2/error^2...+(Nexp2-Npred2)^2/error^2...+(Nexp3-Npred2)^2/error^2/18

where Nexp1, Nexp2, and Nexp3 is the nitrogen  experimental chemical shift of Unknown Amino acid 1, 2, and 3 and Npred1, Npred2, Npred 3 is nitrogen chemical shift of Q4, V5, and Y6. You divide by the number of atoms used (18)
```
The increase in parameters (number of atoms used to calculate RMSD) causes a greater variation in the rmsd values between matches. Thus you are less likely to get rmsd values lower than your actual match. 

#############Combined Sum###########
To maximize the differentiaton between various potential matches, you can combine the values from both techniques. While this may cause a greater differentiation between matches, it can also swing both ways. Neither of the 2 above techniques is completely false positive proof, and whereas one technique may provide a match with the lowest rmsd, the other may have a higher value. Combining the proper fit with the improper one may lead to a false postive, where the lowest rmsd is now not the best match. Thus, it is best to look across all 3 techniques to make the best decision. 

#############Uses###########

#############Use for i+1 or i-1##########
When trying to find an i-1 or i+1 of an amino acid, you may have multiple potential options. To narrow down your options and find the best fit, you can generate a file of your assigned amino acids using SAVUS, then the chemical shift values of your various potentials and determine which gives the lowest rmsd value. 
```
Known/Assigned peaks
R86N-HN 117.438
R86N-HA 1000
R86C 174.460
R86N-CA-HN 54.454
R86N-CB-HN 31.510
R86N-HN 8.172
F87N-HN 123.350
F87N-HA 1000
F87C 177.157
F87N-CA-HN 55.737
F87N-CB-HN 40.508
F87N-HN 8.442
V88N-HN 127.501
V88N-HA 1000
V88C-HN 1000
V88N-CA-HN 64.121
V88N-CB-HN 31.493
V88N-HN 8.459

For i-1, add prior:
X2N-HN 108.969
X2N-HA 1000
X2HA2-HA 1000
X2C 174.921
X2CA-HN 46.815
X2N-HN 7.837
R86N-HN 117.438
R86N-HA 1000
R86C 174.460
R86N-CA-HN 54.454
R86N-CB-HN 31.510
R86N-HN 8.172
F87N-HN 123.350
F87N-HA 1000
F87C 177.157
F87N-CA-HN 55.737
F87N-CB-HN 40.508
F87N-HN 8.442
V88N-HN 127.501
V88N-HA 1000
V88C-HN 1000
V88N-CA-HN 64.121
V88N-CB-HN 31.493
V88N-HN 8.459

For i+1, add at the end:
R86N-HN 117.438
R86N-HA 1000
R86C 174.460
R86N-CA-HN 54.454
R86N-CB-HN 31.510
R86N-HN 8.172
F87N-HN 123.350
F87N-HA 1000
F87C 177.157
F87N-CA-HN 55.737
F87N-CB-HN 40.508
F87N-HN 8.442
V88N-HN 127.501
V88N-HA 1000
V88C-HN 1000
V88N-CA-HN 64.121
V88N-CB-HN 31.493
V88N-HN 8.459
X2N-HN 108.969
X2N-HA 1000
X2HA2-HA 1000
X2C 174.921
X2CA-HN 46.815
X2N-HN 7.837
```
Cycle through your options, and see which amino acid gives you the lowest rmsd value in the appropriate range (for the above example, you would be looking at the lowest rmsd value for G85). 

#############Use for unknown/unassigned peaks##########
In many instances, you may not find any matches for a particular peak. However, you will have both the i CA,CB and i-1 CA,CB in addition the carbonly of the i-1 and the N and HN of the i. This alone may be enough to get a match. 
```
X1N-HN 113.882
X1N-HA 1000
X1C 176.4
X1CA-HN 55.9
X1CB-HN 29.636
X1N-HN 7.615
X2N-HN 108.969
X2N-HA 1000
X2HA2-HA 1000
X2C 174.921
X2CA-HN 46.815
X2N-HN 7.837
```
In other cases you may have 3 or 4 matches, however the chemical shifts are all in non-unique ranges. SPARTA is also particular useful for this as well. 
#############Confirming Assignment of peaks##########
During the assignment process, there are many isntances where you may doubt a series of your assignmnents or question their validity. While SOVUS can be used, that is designed more for the entire protein. Use SOVUS to generate a properly formatted/compiled peaklist file. Then use SOPUS to confirm the range of amino acids you are looking for has the lowest rmsd value. 

```
Assigned amino acids
R86N-HN 117.438
R86N-HA 1000
R86C 174.460
R86N-CA-HN 54.454
R86N-CB-HN 31.510
R86N-HN 8.172
F87N-HN 123.350
F87N-HA 1000
F87C 177.157
F87N-CA-HN 55.737
F87N-CB-HN 40.508
F87N-HN 8.442
V88N-HN 127.501
V88N-HA 1000
V88C-HN 1000
V88N-CA-HN 64.121
V88N-CB-HN 31.493
V88N-HN 8.459
```
The above list should have the lowest rmsd for amino acids R86 through V88. Thus confirming our assignment. 
