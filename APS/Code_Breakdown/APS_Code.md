Using AVS, the sparta file and peaklist file are now the proper format. Both have 6 atoms for each amino acid, and are the same size. 

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

Now we want to take the diagonal sum. To do this, we can use the built in diagonal option of numpy:
```
list1=[]
    for i in range(columns_divided):
        diagonal=np.diag(matrix,i)
        if len(diagonal)==rows_divided:
            summed_diagonal=(sum(diagonal))/(len(diagonal))
            if summed_diagonal<set_threshold:
                ax.scatter(i,summed_diagonal)
                tuples=(f'{dict[i]}-{dict[i+rows_divided-1]} rmsd=',summed_diagonal)
                list1.append(tuples)
        else:
            break
```
This takes the diagonal, starting at index i in our matrix. Thus, we go through the number of amino acids we have, and take the sum of the diagonal. However, what would be more useful is the average value of that sum. (easier to compare 1.1 and 2.4 than 50.5 and 53.2). Then we filter using a threshold the user sets, and use a tuple to store it. Using a tuple will enable us to then sort it from lowest rmsd to highest. 
```
A=sorted(list1, key=lambda rmsd:rmsd[1])
    listed=list(A)
    for value in listed:
        two_decimal_points='%.2f' % value[1]
        text_area.insert(tk.INSERT,f'{value[0]}{two_decimal_points}\n')
```
This basically just sorts the list using the rmsd value.

######RMSD Sum####
As before, we make our list of predictions and experimental values. However, instead of calculating the rmsd of a single amino acid, we now calculate the rmsd using all of the atoms of our predictions list. I.E. Instead of 1 amino acid comapred to 1 sparta value, it is now 4 amino acids with 4 sparta values. 

To do so, we first create a list of our experimental values:
```
        count=0
        iterations=0
        dmitry_list=[]
        dmitry_experiment_value=[]
        dmitry_predict_value=[]
        dmitry_error_value=[]
        dmitry_square_deviations=[]
        for experiments in experimental_values:
            modifier=experiments.strip()
            splitting=modifier.split()
            dmitry_experiment_value.append(splitting[1])
            iterations+=1
            if iterations == len(experimental_values):
                for prediction in predicted_values:
                    modifier2=prediction.strip()
                    splitting2=modifier2.split()
                    dmitry_predict_value.append(splitting2[1])
                    dmitry_error_value.append(splitting2[2])
```                    
We then have an iterator that will determine how many sparta values will be added. Thus defining the size of the sparta prediction list is the same as our experimental list. Next, we want to incremenet the chunks by 1. So if experimental value size is 4, then we want prediction amino acids 1:4, then 2:5, etc. 
```
        below_rmsd_list=[]
        for i in range(len(dmitry_predict_value)):
            temp_predict_value=dmitry_predict_value[(i*6):(i*6)+len(dmitry_experiment_value)]
            temp_error_value=dmitry_error_value[(i*6):(i*6)+len(dmitry_experiment_value)]
            if ((i*6)+len(dmitry_experiment_value))>(len(dmitry_predict_value)):
                break
```
i starts at 0, so this takes the values 0:size of experimental value list. We also want to only take chunks that are the same size as our experimental list. Thus, if the size of our chunk becomes larger than the experimental, then we end the loop. The rest of the script is identical to the diagonal sum. Since the experimental and predictions list are now the proper size, and contain all the amino acids to check, we just calculate the square deviation using all the atoms now, and rmsd similarly. Then sort them by rmsd value. 


####Combined Sum#####
Finally, you may wish to combined the values of the 2 techniques. The do this, we first go through the diagonal sum rmsd list, and exctract the residue number/type. Then we search through the RMSD sum and see if this amino acid exists in that list as well. If it does, then we search through list2, once we find the appropriate hit using regex (i.e. Y3N in list1 == Y3N in list2), then we combine their RMSD values. 

```
combined_list=[] 
    for values in listed:
        amino_acid_search=re.search('^\d+[A-Z]',values[0])
        r=re.compile(amino_acid_search.group(0))
        rmsd_find=list(filter(r.match,[i[0] for i in listed2]))
        if rmsd_find !=[]:
            rmsd_find_string=''.join(rmsd_find)
            for values2 in listed2:
                if values2[0]==rmsd_find_string:
                    summed_values='%.2f' % ((values[1]+values2[1])/2)
                    combined_list.append(f'{values2[0]}{summed_values}')
```
Since both lists were already listed from least to greatest. There is no need to sort this list. 
