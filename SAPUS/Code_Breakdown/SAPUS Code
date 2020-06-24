Using SAVUS, the sparta file and peaklist file are now the proper format. Both have 6 atoms for each amino acid, and are the same size. 

There are a variety of ways to calculate the rmsd. 

###Daigonal Sum###
You can create a array of rmsd values for each unknown or amino acid, with each column being its rmsd with the sparta match. With multiple amino acids making a matrix. Since the amino acids/unknowns are sequential (i.e. you would be looking at the i, and i-1, i-2, i-3, etc.), the correct match of each amino acid/unknown with the sparta value will form a diagonal array. 

Thus, first we must make a matrix of the appropriate size, to fill in all the rmsd values. 
```
experimental_values=[]
    predicted_values=[]
    dict={}
    amino_acid_number=-1
    counter=0
    with open(sparta_file) as predictions, open(dat_file) as experimental:
        rows=0
        columns=0
        for lines in predictions:
            dict_modifier=lines.strip()
            counter+=1
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+[A-Z]',dict_modifier)
                dict[amino_acid_number]=atom_type.group(0)
            rows+=1
            predicted_values.append(lines)
        for lines2 in experimental:
            columns+=1
            experimental_values.append(lines2)
        columns_divided=int(rows/6)
        rows_divided=int(columns/6)
        matrix=np.zeros((rows_divided,columns_divided))
        
 ```
 A number of things are going on here. First we are creating a dictionary so we can use later when printing out what amino acids have what rmsds (since your unknowns won't have residue type). Secondly, we create columns using the number of unknowns we're calculating, and the rows for the sparta predictions we have. We divide by 6 since the rmsd will compile 6 values. Thus for every 6 value in each file, we will only get 1 rmsd. 
 
 Now we need to calculate the rmsd. As stated before, for this technique, every amino acid will be compared to every amino acid in the prediction individually. 
 ```
 for experiments in experimental_values:
        modifier=experiments.strip()
        splitting=modifier.split()
        experiment_value.append(splitting[1])
        number+=1
        if number == 6:
            number=0
            iterations+=1
            for prediction in predicted_values:
                modifier2=prediction.strip()
                splitting2=modifier2.split()
                predict_value.append(splitting2[1])
                error_value.append(splitting2[2])
                count+=1
                if count ==6:
                    count=0
                    shit+=1
                    for predict,experiment,error in zip(predict_value,experiment_value,error_value):
                        square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                        if square_deviation>100:
                            pass
                        else:
                            square_deviations.append(square_deviation)
                    if len(square_deviations)==0:
                        rmsd_filler=0
                        numpy_list.append(rmsd_filler)
                    else:
                        rmsd=math.sqrt(((1/int(len(square_deviations)))*(sum(square_deviations))))
                        numpy_list.append(rmsd)
                    predict_value.clear()
                    square_deviations.clear()
                    error_value.clear()
            experiment_value.clear()
            arr=np.array(numpy_list)
            matrix[iterations,:]=arr
            numpy_list.clear()
```
We start with the unknown amino acid, and create a list of the chemical shifts of all the atoms (6). Then when done, we then go through the amino acids in the sparta file. Now each list is going be in 2 columns:
```
Q4N-HN 121.973
Q4N-HA 1000
Q4C 175.123
```
The sparta file is going to have error values as well:
```
4QN 123.306 2.598
4QHA 4.510 0.237
4QC 173.967 0.914
4QCA 55.623 1.065
4QCB 32.000 1.586
```
Thus these are each stored seperately. The RMSD is then taken. If an atom is missing, each atom type will have a value of 1000, thus it will be ignored and not added to a list. As a result, the list will be empty. These atoms will have an rmsd of 0. These values are then added to a list. When you have gone through every amino acid in the sparta file, the list is then converted into an array, and stored into the matrix. The iteration counter will be used to add it into the appropriate row (row 1 is the first amino acid, row 2 the 2nd, etc.). The list is then cleared and we start over. 
