This is the manual for SAG (Sparky assignment generator). This program was written in python3.7, and uses tkinter and functools. 
The program will generate properly formatted peaklist files for SAPUS. Simply input your chemical shift values, and click enter values. 
This will compile your amino acid in the proper format. To add more amino acids, simply type in the chemical shift values for the next 
amino acid, and click add values. **If there is no value for a particular atom, leave it blank.** 
You may add as many values as you wish. When done, choose your save file (use browse) and click save/write file. 

Input
```
Inputed Values:
113.882
176.400
55.9
29.636
7.615

Printout:
added amide nitrogen: 113.882
added carbonyl carbon: 176.400
added alpha carbon: 55.9
added beta carbon: 29.636
added amide hydrogen: 7.615
```

Written file:
```
X1N-HN 113.882
X2N-HA 1000
X1C 176.4
X1CA-HN 55.9
X1CB-HN 29.636
X1N-HN 7.615
```
