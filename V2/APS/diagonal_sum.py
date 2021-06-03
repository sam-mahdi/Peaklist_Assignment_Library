import math
import re
import numpy as np
import os

def extract_predictions(sparta_file,sparta_directory):
    os.chdir(sparta_directory)
    dict={}
    amino_acid_number=-1
    counter=0
    predicted_values=[]
    with open(sparta_file) as predictions:
        for sparta in predictions:
            counter+=1
            predicted_values.append(sparta)
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+\s+[A-Z]',sparta.strip())
                dict[amino_acid_number]=atom_type.group(0)
        return dict,predicted_values

def extract_experimental(data_file,data_directory):
    os.chdir(data_directory)
    experimental_values=[]
    with open(data_file) as experimental:
        for data in experimental:
            if data == '' or data == '\n':
                continue
            experimental_values.append(data)
    return experimental_values


#Stores an amino acids values (all 6), then calculates the rmsd of that amino acid with each amino acid in SPARTA
#Each row will be the rmsd of the SPARTA amino acid, with the columns the experimental amino acid
def calculate_rmsd(sparta_file,sparta_directory,data_file,data_directory,set_threshold):
    experimental_values=extract_experimental(data_file,data_directory)
    dict,predicted_values=extract_predictions(sparta_file,sparta_directory)
    rows_divided=int(len(predicted_values)/6)
    columns_divided=int(len(experimental_values)/6)
    matrix=np.zeros((columns_divided,rows_divided))
    predict_value=[]
    error_value=[]
    experiment_value=[]
    square_deviations=[]
    number=0
    count=0
    numpy_list=[]
    iterations=-1
    for experiments in experimental_values:
        if experiments == '' or experiments == '\n':
            continue
        experiment_value.append(re.search('\d+\.\d+',experiments).group(0))
        number+=1
        if number == 6:
            number=0
            iterations+=1
            for prediction in predicted_values:
                prediction_value=prediction.strip().split()[3]
                prediction_error=prediction.strip().split()[4]
                predict_value.append(prediction_value)
                error_value.append(prediction_error)
                count+=1
                if count ==6:
                    count=0
                    for predict,experiment,error in zip(predict_value,experiment_value,error_value):
                        square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                        if square_deviation>500:
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
    return matrix
#The diagonal array rmsd is when the amino acid matches with the sparta+ values
def find_diagonal(sparta_file,sparta_directory,data_file,data_directory,set_threshold):
    residues=[]
    rmsd=[]
    list_of_matches=[]
    x_axis=[]
    experimental_values=extract_experimental(data_file,data_directory)
    dict,predicted_values=extract_predictions(sparta_file,sparta_directory)
    rows_divided=int(len(predicted_values)/6)
    columns_divided=int(len(experimental_values)/6)
    matrix=calculate_rmsd(sparta_file,sparta_directory,data_file,data_directory,set_threshold)
    for i in range(rows_divided):
        diagonal=np.diag(matrix,i)
        if len(diagonal)==columns_divided:
            summed_diagonal=(sum(diagonal))/(len(diagonal))
            if summed_diagonal<set_threshold:
                x_axis.append(int((re.search('\d+',dict[i])).group(0)))
                residues.append(dict[i])
                rmsd.append(summed_diagonal)
                tuples=(f'{dict[i]}-{dict[i+columns_divided-1]} rmsd=',summed_diagonal)
                list_of_matches.append(tuples)
        else:
            break
    return residues,rmsd,list_of_matches,x_axis
