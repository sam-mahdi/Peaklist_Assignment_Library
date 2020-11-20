These tests show both the capabilites of confirming assignments, and assigning peaks even when you only have the i and i-1
Using the avs_sparta_input file with assigned_peak_list file with a threshold of 2, generates this output
Diagonal Sum
```
Diagonal Sum (sorted by rmsd value)
84Q-88V rmsd=1.06
34L-38H rmsd=1.67
8R-12P rmsd=1.73
193E-197A rmsd=1.86
159P-163P rmsd=1.91
233S-237V rmsd=1.97
```
Combined RMSD
```
Collective RMSD (sorted by rmsd value)
84Q-88V rmsd=1.10
8R-12P rmsd=1.71
34L-38H rmsd=1.83
193E-197A rmsd=1.94
233S-237V rmsd=1.98
198H-202A rmsd=1.99
```
Combined Sum
```
Combined sum (sorted by rmsd)
84Q-88V rmsd=1.08
34L-38H rmsd=1.75
8R-12P rmsd=1.72
193E-197A rmsd=1.90
233S-237V rmsd=1.97
```

Using the avs_sparta_input file with the unassigned_peak_list file (generated using SAG) using a threshold of 1.2, generates this output:

Diagonal Sum
```
Diagonal Sum (sorted by rmsd value)
84Q-85G rmsd=0.76
212G-213S rmsd=0.94
241L-242G rmsd=1.03
194E-195H rmsd=1.20
```
Collective RMSD
```
Collective RMSD (sorted by rmsd value)
84Q-85G rmsd=0.77
212G-213S rmsd=0.99
194E-195H rmsd=1.08
241L-242G rmsd=1.11
```
Combined Sum
```
Combined sum (sorted by rmsd)
84Q-85G rmsd=0.77
212G-213S rmsd=0.96
241L-242G rmsd=1.07
194E-195H rmsd=1.14
```
Confirming our uknown peaks are in fact Q84 and G85
