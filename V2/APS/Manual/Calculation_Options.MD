There are 2 methods to determine RMSD. 

****Diagonal Sum****

This method calculates the RMSD of each assigned/unassigned amino acid to every amino acid in SPARTA+/BMRB. 

I.E. If your protein is 50 amino acids, you will have 50 RMSD values for every single (un)assigned amino acid. 

If you have 2 unknown amino acids (i-1,i), then you will have 100 RMSD values combined. This creats a matrix of values

```
                       Q4    V5  Y6 ....Sparta amino acids  
Unknown Amino Acid 1  1.56 2.38 0.92
Unknown Amino Acid 2  3.25 1.12 2.65
Unknown Amino Acid 3  0.65 3.25 1.21
```
Since the amino acids are sorted from i-1 forward, the diagonal vector would represent the proper assigned rmsd. Thus, the diagonal vector for every amino acid is calculated. 

```
                       Q4    V5  Y6 ....Sparta amino acids  
Unknown Amino Acid 1  1.56 2.38 0.92
Unknown Amino Acid 2  3.25 1.12 2.65
Unknown Amino Acid 3  0.65 3.25 1.21

Diagonal Vector 1 = 1.56, 1.12, 1.21
Diagonal Vector 2 = 2.38 2.65, ...etc. 
```
The diagonal vector where all the RMSD values are below the threshold, will be displayed. 

****RMSD Sum****

Instead of calculating the RMSD of each un(assigned) amino acid individually, they are now calculated as a group. 
I.E. If you have 6 amino acids in your file, the RMSD equation is now being calculated with 6 amino acids from SPARTA+/BMRB. 

```
RMSD=sqrt((nXexp1-npred1)^2/error^2+(nXexp1-npred1)^2/error^2)...nX+1/N
```

where n is the atom (N, HA, C, CA, CB, HN) and N is the number of atoms, and X is the amino acid being looked at. 
In the diagonal sum, N is 6 and X is 1 since you are only looking at a single amino acid. 
However, for combined sum, N and X are the number of amino acids in the file. 

****Combined Sum****

This combines the above two methods. This can be useful since sometimes an RMSD value might be calculated higher using one method than the other. Thus filtering out bad mathces.
However, one method may give you a better answer than the other, thus combining them may cause you to get a higher RMSD than accurate. 
