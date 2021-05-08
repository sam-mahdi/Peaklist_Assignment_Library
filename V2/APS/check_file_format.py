import re
import os

def extract_predictions(sparta_file,sparta_directory):
    sparta_error=[]
    os.chdir(sparta_directory)
    with open(sparta_file) as predictions:
        for sparta in predictions:
            sparta_checker=re.search('^\d+\s+[A-Z]\s+\w+\s+\d+\.\d+\s+\d+\.\d+',sparta)
            if sparta_checker == None:
                sparta_error.append(f'Sparta file is not in proper format. Use AVS to convert to proper format\nError at line {sparta}')
    return sparta_error

def extract_experimental(data_file,data_directory):
    os.chdir(data_directory)
    data_error=[]
    counter=0

    with open(data_file) as experimental:
        for data in experimental:
            if data == '' or data == '\n':
                continue
            counter+=1
            data_checker=re.findall('\d+\.\d+',data)
            if len(data_checker) > 1:
                data_error.append(f'Peaklist file is not in proper format. There should only be one decimal value per line.\nError at line: {data}')
            if data_checker == []:
                data_error.append(f'Peaklist file is not in the proper format. Every line with text, should contain data. Data points must contain decimal (e.g. 100 should be 100.00)\nError at line: {data}')
    if counter % 6 != 0:
        data_error.append(f'Peaklist file is not in the proper format\nEach amino acid entry should have 6 entries [N,HA,C,CA,CB,HN] or [N,HA,HA2,C,CA,HN] for Glycines.\nYour file has {counter} (Should be divisible by 6). Add 1000.00 for atoms you do not have data for.')
    return data_error

def check(sparta_file,sparta_directory,data_file,data_directory):
     return extract_predictions(sparta_file,sparta_directory), extract_experimental(data_file,data_directory)
