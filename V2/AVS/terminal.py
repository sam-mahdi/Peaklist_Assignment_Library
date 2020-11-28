import re
import sys
import os

import tkinter.scrolledtext as st
import tkinter as tk
import functools
class ReadOnlyText(st.ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state=tk.DISABLED)

        self.insert = self._unlock(super().insert)
        self.delete = self._unlock(super().delete)

    def _unlock(self, f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            print(args[1])
            self.config(state=tk.NORMAL)
            r = f(*args, **kwargs)
            self.config(state=tk.DISABLED)
            return r
        return wrap

def get_parameters(terminal_line):
    sparta_file=(re.search('-in (\w+\.\w+)',terminal_line)).group(1)
    save_directory=os.getcwd()
    seq_directory=os.getcwd()
    sparta_directory=os.getcwd()
    save_file_sparta=(re.search('-out (\w+\.\w+)',terminal_line)).group(1)
    seq_file=(re.search('-seq (\w+\.\w+)',terminal_line)).group(1)
    seq_start=int((re.search('-seq_start (\w+)',terminal_line)).group(1))
    mutation_list=(re.search('-mutation (([A-Z]\d+[A-Z]\s+)+)',terminal_line))
    if mutation_list is None:
        mutation_list=()
    else:
        mutation_list=mutation_list.group(1)
    return sparta_file,save_file_sparta,save_directory,seq_file,seq_start,mutation_list,seq_directory,sparta_directory


def terminal_run():
    text_area = ReadOnlyText(width = 40,height = 10,font = ("Times New Roman",12))
    terminal_line=' '.join(sys.argv)
    if re.search('-sparta_only',terminal_line) is not None:
        sparta_file,save_file_sparta,save_directory,seq_file,seq_start,mutation_list,seq_directory,sparta_directory=get_parameters(terminal_line)
        from sparta_file_formatter import check_sparta_file_boundaries
        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        with open(save_file_sparta,'w') as file:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
    if re.search('-bmrb_only',terminal_line) is not None:
        sparta_file,save_file_sparta,save_directory,seq_file,seq_start,mutation_list,seq_directory,sparta_directory=get_parameters(terminal_line)
        from bmrb_file_formatter import make_bmrb_list
        bmrb_file_boundaries=make_bmrb_list(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        with open(save_file_sparta,'w') as file:
            for stuff_to_write in bmrb_file_boundaries:
                file.write(stuff_to_write+'\n')
    if re.search('-run_AVS_sparta',terminal_line) is not None:
        sparta_file,save_file_sparta,save_directory,seq_file,seq_start,mutation_list,seq_directory,sparta_directory=get_parameters(terminal_line)
        nmrstarfile=(re.search('-nmrstarfile (\w+\.\w+)',terminal_line)).group(1)
        save_file_peaklist=(re.search('-peaklist_out (\w+\.\w+)',terminal_line)).group(1)
        nmrstarfile_directory=os.getcwd()
        save_directory=os.getcwd()
        set_threshold=int((re.search('-threshold (\w+)',terminal_line)).group(1))
        from sparta_file_formatter import check_sparta_file_boundaries
        from nmrstar import fill_in_missing_data
        from RMSD_Calculator import RMSD_calc
        from RMSD_Calculator import filter_peaklist_to_sparta

        sparta_file_boundaries=check_sparta_file_boundaries(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        data_files=fill_in_missing_data(seq_file,nmrstarfile,seq_start,text_area)
        RMSD_calc(set_threshold,sparta_file_boundaries,data_files,text_area)
        data_file_to_save=filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area)

        #Both files are saved for use in other programs
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as filsequence_file_entry:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_writsequence_file_entry in data_file_to_save:
                    filsequence_file_entry.write(stuff_to_writsequence_file_entry+'\n')
    if re.search('-run_AVS_bmrb',terminal_line) is not None:
        sparta_file,save_file_sparta,save_directory,seq_file,seq_start,mutation_list,seq_directory,sparta_directory=get_parameters(terminal_line)
        nmrstarfile=(re.search('-nmrstarfile (\w+\.\w+)',terminal_line)).group(1)
        save_file_peaklist=(re.search('-peaklist_out (\w+\.\w+)',terminal_line)).group(1)
        nmrstarfile_directory=os.getcwd()
        save_directory=os.getcwd()
        set_threshold=int((re.search('-threshold (\w+)',terminal_line)).group(1))
        from bmrb_file_formatter import make_bmrb_list
        from nmrstar import fill_in_missing_data
        from RMSD_Calculator import RMSD_calc
        from RMSD_Calculator import filter_peaklist_to_sparta

        sparta_file_boundaries=make_bmrb_list(seq_file,seq_directory,mutation_list,sparta_file,sparta_directory,seq_start)
        data_files=fill_in_missing_data(seq_file,nmrstarfile,seq_start,text_area)
        RMSD_calc(set_threshold,sparta_file_boundaries,data_files,text_area)
        data_file_to_save=filter_peaklist_to_sparta(sparta_file_boundaries,data_files,text_area)

        #Both files are saved for use in other programs
        os.chdir(save_directory)
        with open(save_file_sparta,'w') as file, open(save_file_peaklist,'w') as filsequence_file_entry:
            for stuff_to_write in sparta_file_boundaries:
                file.write(stuff_to_write+'\n')
            for stuff_to_writsequence_file_entry in data_file_to_save:
                    filsequence_file_entry.write(stuff_to_writsequence_file_entry+'\n')
    if re.search('-SPARKYtoNMRSTAR3p1',terminal_line) is not None:
        terminal_flag=True
        from sparky2nmrstar import sparky2nmrstar_parameters
        sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,HNCOCA_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,HNCOCA_directory,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,bmrb_file,bmrb_directory=sparky2nmrstar_parameters(terminal_line)
        from SPARKYtoNMRSTAR3p1 import main_loop
        main_loop(sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,HNCOCA_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,HNCOCA_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,bmrb_file,bmrb_directory,terminal_flag)
    if re.search('-assign_percent',terminal_line) is not None:
        sequence_file=(re.search('-seq (\w+\.\w+)',terminal_line)).group(1)
        save_file=(re.search('-nmrstar (\w+\.\w+)',terminal_line)).group(1)
        seq_directory=os.getcwd()
        save_directory=os.getcwd()
        from percent_assigned import calculate_percentage
        calculate_percentage(sequence_file,seq_directory,save_file,save_directory,text_area)
    if re.search('-custom_percent',terminal_line) is not None:
        from terminal_custom_assignment import custom_percent_parameters
        ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL = custom_percent_parameters(terminal_line)
        atom_list=(re.search('-atoms ((N*C*H*[A-Z]\d*\s+)+)',terminal_line)).group(1)
        save_file=(re.search('-nmrstarfile (\w+\.\w+)',terminal_line)).group(1)
        save_directory=os.getcwd()
        seq_directory=os.getcwd()
        sequence_file=(re.search('-seq (\w+\.\w+)',terminal_line)).group(1)
        from custom_assignment import custom_assignment
        custom_assignment(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory,text_area)
    if re.search('-special_percent',terminal_line) is not None:
        from terminal_custom_assignment import custom_percent_parameters
        ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL = custom_percent_parameters(terminal_line)
        atom_list=(re.search('-atoms ((N*C*H*[A-Z]\d*\s+)+)',terminal_line)).group(1)
        save_file=(re.search('-nmrstarfile (\w+\.\w+)',terminal_line)).group(1)
        save_directory=os.getcwd()
        seq_directory=os.getcwd()
        sequence_file=(re.search('-seq (\w+\.\w+)',terminal_line)).group(1)
        from custom_assignment import special_assignmnet
        special_assignmnet(ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL,atom_list,save_file,save_directory,sequence_file,seq_directory,text_area)
