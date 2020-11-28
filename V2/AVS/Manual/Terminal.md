This is the manual to run AVS using the command line/terminal. 

Commands:

***Sparta Only****

To generate SPARTA or BMRB files only type in ```-sparta only``` or ```-bmrb_only``` respectively.  

Sequence files can be uploaded with ```-seq```

Sparta files can be uploaded with ```-in```

To add mutations you can add them with ```-mutation```

To define the sequence start: ```-seq_start```

Define the sparta save file with ```-out```


```AVS -sparta_only -in protein.tab -seq sequence.txt -mutation V55A Q44R -seq_start 48 -out save_sparta.txt```

***Running AVS****

To run AVS using sparta or bmrb type ```-run_AVS_sparta``` or ```run_AVS_bmrb``` respecitvely. 

Sparta, bmrb, sequence files, and mutation are all added the same as above. 

NMRSTAR files can be uploaded with: ```-nmrstarfile```

The threshold can be set with ```-threshold```

The peaklist save file with ```-peaklist_out```

```AVS -run_AVS_sparta -in protein.tab -seq sequence.txt -mutation V55A Q44R -seq_start 48 -out save_sparta.txt -nmrstarfile protein_V3.txt -threshold 2 -peaklist_out save_peaklist.txt```

***Running SPARKY to NMRSTAR****

To run SPARKY to NMRSTAR ```-SPARKYtoNMRSTAR3p1```

sequence file can be defined as above.

The nmrstarfile can be saved with  (make sure not to use dots outside of the file extension for naming)```-out```

Currently NHSQC, HNCA, HNCACB, HNCO, HNCOCA, CHSQC, HBHACONH, CCC_TOCSY, and HCCH_TOCSY can be convert. Type in lower case names with a dash to upload each. 

```-nhsqc nhsqc.list -hnca hnca.list -hncacb hncacb.list```

If you want to compare to assigment values to bmrb values, you can upload the bmrb.csv with ```-bmrb```

The standard deviation can be set ```-std```

```AVS -SPARKYtoNMRSTAR3p1 -seq sequenct.txt -nhsqc nhsqc.list -chsqc chsqc.list -hnca hnca.list -ccc_tocsy ccc_tocsy.list -std 0.2 -bmrb bmrb.csv -out nmrstar3p1.txt```

***Determine Assignment and Custom Percentage***

To use the pre-built in assignment (ILVTA methyls, backbone, all heavy atoms, alpha+beta, gamma, delta, epislon) use ```-assign_percent```

sequence file can be uploaded as above (```-seq```)

assingment file can be uploaded with ```-nmrstar```

```AVS -assign_percent -seq sequent.txt -nmrstar nmrstarfile.txt```

To use custom percent ```-custom_percent```

To define what atoms to use ```-atoms```

Save file and seq as above (```-nmrstar```)

Each atom can be assigned by doing dash, and the triple letter followed by its numerical value (```-ALA 1```). 

```AVS -custom_percent -atoms CD1 CD2 CG1 CG2 -ILE 2 -LEU 2 -VAL 2```

To use special percent ```-special_percent```

The sequence file, atoms, and amino acid numerical representation is identical as above 

```AVS -special_percent -atoms CG1 CG2 -VAL 2
