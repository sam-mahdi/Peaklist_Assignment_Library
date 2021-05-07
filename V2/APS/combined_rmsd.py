import re
import math
import os


def extract_predictions(sparta_file,sparta_directory):
    os.chdir(sparta_directory)
    predict_value=[]
    error_value=[]
    dict={}
    counter=0
    amino_acid_number=-1
    with open(sparta_file) as predicted_values:
        for sparta in predicted_values:
            counter+=1
            prediction_value=sparta.strip().split()[3]
            prediction_error=sparta.strip().split()[4]
            predict_value.append(prediction_value)
            error_value.append(prediction_error)
            if counter==6:
                counter=0
                amino_acid_number+=1
                atom_type=re.search('^\d+\s+[A-Z]',sparta.strip())
                dict[amino_acid_number]=atom_type.group(0)
    return predict_value,error_value,dict
def extract_experimental(data_file,data_directory):
    os.chdir(data_directory)
    experiment_values=[]
    with open(data_file) as experimental_values:
        for data in experimental_values:
            if data == '' or data == '\n':
                continue
            experimental_value=(re.search('\d+\.\d+',data.strip())).group(0)
            experiment_values.append(experimental_value)
    return experiment_values

#The experimental value is taken as a whole (instead of one by one) and the rmsd is calculated with SPARTA values
def calculate_combined_rmsd(sparta_file,sparta_directory,data_file,data_directory,set_threshold):
    predict_value,error_value,dict=extract_predictions(sparta_file,sparta_directory)
    experiment_values=extract_experimental(data_file,data_directory)
    list_of_matches=[]
    square_deviation_list=[]
    residues=[]
    rmsd=[]
    x_axis=[]
    for i in range(len(predict_value)):
        temp_predict_value=predict_value[(i*6):(i*6)+len(experiment_values)]
        temp_error_value=error_value[(i*6):(i*6)+len(experiment_values)]
        if ((i*6)+len(experiment_values))>(len(predict_value)):
            break
        else:
            for predict,experiment,error in zip(temp_predict_value,experiment_values,temp_error_value):
                square_deviation=(((float(predict)-float(experiment))**2)/((float(error))**2))
                if square_deviation>500:
                    pass
                else:
                    square_deviation_list.append(square_deviation)
            if len(square_deviation_list)==0:
                pass
            else:
                summed_rmsd=math.sqrt(((1/int(len(square_deviation_list)))*(sum(square_deviation_list))))
                if summed_rmsd<set_threshold:
                    x_axis.append(int((re.search('\d+',dict[i])).group(0)))
                    residues.append(dict[i])
                    rmsd.append(summed_rmsd)
                    tuples=(f'{dict[i]}-{dict[i+(len(experiment_values)/6)-1]} rmsd=',summed_rmsd)
                    list_of_matches.append(tuples)
            square_deviation_list.clear()
    return residues,rmsd,list_of_matches,x_axis
