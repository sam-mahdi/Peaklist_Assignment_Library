import re
import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time

"""
Parameters

Sequence file should be single letter amino acid with no modifications (i.e. MSQYDGAS)

Add in peaklists, if no peaklist then leave as is. I.E. NHSQC_file = 'nhsqc.list'

save file is the name of your nmrstar HNCA_file

standard_deviation_value is the cutoff for the standard deviation of yoru values, if you have a peak that is improperly labeled or has proper labeling but simply has a improper value, this will be conveyed here.
I would not recommend going above a standard deviation of 0.25
"""

class ProgressBar(object):
    def __init__(self, second_window):
        self.pbWindow = Toplevel(second_window)
        self.pbWindow.update_bar=Label(self.pbWindow,text='')
        self.pbWindow.update_bar.grid(column=0,row=3)
        self.pbWindow.progress=Label(self.pbWindow,text='0%')
        self.pbWindow.progress.grid(row=3,column=2)
        self.pbWindow.pb=ttk.Progressbar(self.pbWindow, orient='horizontal',mode='determinate',length=280)
        self.pbWindow.pb.grid(row=2,column=0)
        self.pbWindow.pb2=ttk.Progressbar(self.pbWindow, orient='horizontal',mode='determinate',length=280)
        self.pbWindow.pb2.grid(row=0,column=0)
        self.pbWindow.progress2=Label(self.pbWindow,text='0%')
        self.pbWindow.progress2.grid(row=1,column=2)

def sequence_list(sequence_file,seq_directory,seq_start_value):
    os.chdir(seq_directory)
    seq_list=[]
    counter=int(seq_start_value)-1
    with open(sequence_file) as file:
        for values in file:
            strip_values=values.strip()
            for entries in strip_values:
                counter+=1
                seq_list.append(f'{counter}{entries}')
    return seq_list
def regex_list(sequence_file,seq_directory,seq_start_value):
    new_list=[]
    Alanine_Values=['C','CA','CB','HA','HB','HD21','HD22','H','N','ND2']
    Arganine_Values=['C','CA','CB','CD','CG','HA','HB2','HB3','HD2','HD3','HG2','HG3','H','N']
    Aspartic_Acid_Values=['C','CA','CB','HA','HB2','HB3','H','N']
    Glutamine_Values=['C','CA','CB','CG','HA','HB2','HB3','HE21','HE22','HG2','HG3','H','N','NE2']
    Glycine_Values=['C','CA','HA2','HA3','H','N']
    Isoleucine_Values=['C','CA','CB','CD1','CG1','CG2','HA','HB','HD1','HG12','HG13','HG2','H','N']
    Luecine_Values=['C','CA','CB','CD1','CD2','CG','HA','HB2','HB3','HD1','HD2','HG','H','N']
    Lysine_Values=['C','CA','CB','CD','CE','CG','HA','HB2','HB3','HD2','HD3','HE2','HE3','HG2','HG3','H','N']
    Methionine_Values=['C','CA','CB','CE','CG','HA','HB2','HB3','HE','HG2','HG3','H','N']
    Proline_Values=['C','CA','CB','CD','CG','HA','HB2','HB3','HD2','HD3','HG2','HG3','H','N']
    Serine_Values=['C','CA','CB','HA','HB2','HB3','H','N']
    Threanine_Values=['C','CA','CB','CG2','HA','HB','HG2','H','N']
    Tryptophan_Values=['C','CA','CB','HA','HB2','HB3','H','HE1','N','NE1']
    Valine_Values=['C','CA','CB','CG1','CG2','HA','HB','HG2','H','N']
    for amino_acids in sequence_list(sequence_file,seq_directory,seq_start_value):
        if amino_acids[-1] == 'M':
            methionine=[amino_acids+'-'+atom for atom in Methionine_Values]
            new_list+=methionine
        if amino_acids[-1] in {'D','N','C','F','S','Y','H'}:
            aspartic_acid=[amino_acids+'-'+atom for atom in Aspartic_Acid_Values]
            new_list+=aspartic_acid
        if amino_acids[-1] == 'A':
            alanine=[amino_acids+'-'+atom for atom in Alanine_Values]
            new_list+=alanine
        if amino_acids[-1] in {'Q','E'}:
            glutamine=[amino_acids+'-'+atom for atom in Glutamine_Values]
            new_list+=glutamine
        if amino_acids[-1] == 'G':
            glycine=[amino_acids+'-'+atom for atom in Glycine_Values]
            new_list+=glycine
        if amino_acids[-1] == 'R':
            arginine=[amino_acids+'-'+atom for atom in Arganine_Values]
            new_list+=arginine
        if amino_acids[-1] == 'I':
            isoleucine=[amino_acids+'-'+atom for atom in Isoleucine_Values]
            new_list+=isoleucine
        if amino_acids[-1] == 'L':
            leucine=[amino_acids+'-'+atom for atom in Luecine_Values]
            new_list+=leucine
        if amino_acids[-1] == 'K':
            lysine=[amino_acids+'-'+atom for atom in Lysine_Values]
            new_list+=lysine
        if amino_acids[-1] == 'P':
            proline=[amino_acids+'-'+atom for atom in Proline_Values]
            new_list+=proline
        if amino_acids[-1] == 'T':
            threanine=[amino_acids+'-'+atom for atom in Threanine_Values]
            new_list+=threanine
        if amino_acids[-1] == 'V':
            valine=[amino_acids+'-'+atom for atom in Valine_Values]
            new_list+=valine
        if amino_acids[-1] == 'W':
            tryptophan=[amino_acids+'-'+atom for atom in Tryptophan_Values]
            new_list+=tryptophan
    return new_list

def NHSQC_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,NHSQC_file,NHSQC_directory):
    with open(NHSQC_file) as nhsqc:
        for nhsqc_lines in nhsqc:
            if re.search('^\w\d+\w+',nhsqc_lines.strip()) is None:
                continue
            nhsqc_split=nhsqc_lines.strip().split()
            if amino_acid+residue_number+atom == nhsqc_split[0].split('-')[0]:
                temp_list.append(float(nhsqc_split[1]))
                spectra_list.append('NHSQC')
            if atom == nhsqc_split[0].split('-')[1] and amino_acid+residue_number == (re.search('[A-Z]\d+',nhsqc_split[0].split('-')[0])).group(0):
                temp_list.append(float(nhsqc_split[2]))
                spectra_list.append('NHSQC')
def HNCA_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCA_file,HNCA_directory):
    with open(HNCA_file) as hnca:
        for hnca_lines in hnca:
            if re.search('^\w\d+\w+',hnca_lines.strip()) is None:
                continue
            hnca_split=hnca_lines.strip().split()
            if amino_acid+residue_number == hnca_split[0].split('-')[0][0:-1] and atom == hnca_split[0].split('-')[1]:
                temp_list.append(float(hnca_split[2]))
                spectra_list.append('HNCA')
            if amino_acid+residue_number+atom == hnca_split[0].split('-')[1]:
                temp_list.append(float(hnca_split[2]))
                spectra_list.append('HNCA')
def HNCACB_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCACB_file,HNCACB_directory):
    with open(HNCACB_file) as hncacb:
        for hncacb_lines in hncacb:
            if re.search('^\w\d+\w+',hncacb_lines.strip()) is None:
                continue
            hncacb_split=hncacb_lines.strip().split()
            if amino_acid+residue_number == hncacb_split[0].split('-')[0][0:-1] and atom == hncacb_split[0].split('-')[1]:
                temp_list.append(float(hncacb_split[2]))
                spectra_list.append('HNCACB')
            if amino_acid+residue_number+atom == hncacb_split[0].split('-')[1]:
                temp_list.append(float(hncacb_split[2]))
                spectra_list.append('HNCACB')
def CBCACONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CBCACONH_file,CBCACONH_directory):
    with open(CBCACONH_file) as cbcaconh:
        for cbcaconh_lines in cbcaconh:
            if re.search('^\w\d+\w+',cbcaconh_lines.strip()) is None:
                continue
            cbcaconh_split=cbcaconh_lines.strip().split()
            if amino_acid+residue_number == cbcaconh_split[0].split('-')[0][0:-1] and atom == cbcaconh_split[0].split('-')[1]:
                temp_list.append(float(cbcaconh_split[2]))
                spectra_list.append('CBCACONH')
            if amino_acid+residue_number+atom == cbcaconh_split[0].split('-')[1]:
                temp_list.append(float(cbcaconh_split[2]))
                spectra_list.append('CBCACONH')
def HCCONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HCCONH_file,HCCONH_directory):
    with open(HCCONH_file) as hcconh:
        for hcconh_lines in hcconh:
            if re.search('^\w\d+\w+',hcconh_lines.strip()) is None:
                continue
            hcconh_split=hcconh_lines.strip().split()
            if amino_acid+residue_number == hcconh_split[0].split('-')[0][0:-1] and atom == hcconh_split[0].split('-')[1]:
                temp_list.append(float(hcconh_split[2]))
                spectra_list.append('HCCONH')
            if amino_acid+residue_number+atom == hcconh_split[0].split('-')[1]:
                temp_list.append(float(hcconh_split[2]))
                spectra_list.append('HCCONH')
def HNCACO_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCACO_file,HNCACO_directory):
    with open(HNCACO_file) as hnco_i:
        for hnco_i_lines in hnco_i:
            if re.search('^\w\d+\w+',hnco_i_lines.strip()) is None:
                continue
            hnco_i_split=hnco_i_lines.strip().split()
            if amino_acid+residue_number+atom == hnco_i_split[0].split('-')[1]:
                temp_list.append(float(hnco_i_split[2]))
                spectra_list.append('HNCACO')
def HNCOCA_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCOCA_file,HNCOCA_directory):
    with open(HNCOCA_file) as hnca1:
        for hnca1_lines in hnca1:
            if re.search('^\w\d+\w+',hnca1_lines.strip()) is None:
                continue
            hnca1_split=hnca1_lines.strip().split()
            if amino_acid+residue_number+atom == hnca1_split[0].split('-')[1]:
                temp_list.append(float(hnca1_split[2]))
                spectra_list.append('HNCOCA')
def HNCO_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCO_file,HNCO_directory):
    with open(HNCO_file) as hnco:
        for hnco_lines in hnco:
            if re.search('^\w\d+\w+',hnco_lines.strip()) is None:
                continue
            hnco_split=hnco_lines.strip().split()
            if amino_acid+residue_number+atom == hnco_split[0].split('-')[1]:
                temp_list.append(float(hnco_split[2]))
                spectra_list.append('HNCO')
def CHSQC_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CHSQC_file,CHSQC_directory):
    with open(CHSQC_file) as chsqc:
        for chsqc_lines in chsqc:
            if re.search('^\w\d+\w+',chsqc_lines.strip()) is None:
                continue
            chsqc_split=chsqc_lines.strip().split()
            if amino_acid+residue_number+atom == chsqc_split[0].split('-')[0]:
                temp_list.append(float(chsqc_split[1]))
                spectra_list.append('CHSQC')
            if atom == chsqc_split[0].split('-')[1] and amino_acid+residue_number == (re.search('[A-Z]\d+',chsqc_split[0].split('-')[0])).group(0):
                temp_list.append(float(chsqc_split[2]))
                spectra_list.append('CHSQC')
def HBHACONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HBHACONH_file,HBHACONH_directory):
    with open(HBHACONH_file) as hbhaconh:
        for hbhaconh_lines in hbhaconh:
            if re.search('^\w\d+\w+',hbhaconh_lines.strip()) is None:
                continue
            hbhaconh_split=hbhaconh_lines.strip().split()
            if amino_acid+residue_number+atom == hbhaconh_split[0].split('-')[1]:
                temp_list.append(float(hbhaconh_split[2]))
                spectra_list.append('HBHACONH')
def CCH_TOCSY_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CCH_TOCSY_file,CCH_TOCSY_directory):
    with open(CCH_TOCSY_file) as ccc_tocsy:
        for ccc_tocsy_lines in ccc_tocsy:
            if re.search('^\w\d+\w+',ccc_tocsy_lines.strip()) is None:
                continue
            ccc_tocsy_split=ccc_tocsy_lines.strip().split()
            if amino_acid+residue_number == (re.search('[A-Z]\d+',ccc_tocsy_split[0].split('-')[0])).group(0) and atom == ccc_tocsy_split[0].split('-')[1]:
                temp_list.append(float(ccc_tocsy_split[2]))
                spectra_list.append('CCH TOCSY')
def HCCH_TOCSY_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HCCH_TOCSY_file,HCCH_TOCSY_directory):
    with open(HCCH_TOCSY_file) as hcch_tocsy:
        for hcch_tocsy_lines in hcch_tocsy:
            if re.search('^\w\d+\w+',hcch_tocsy_lines.strip()) is None:
                continue
            hcch_tocsy_split=hcch_tocsy_lines.strip().split()
            if amino_acid+residue_number == (re.search('[A-Z]\d+',hcch_tocsy_split[0].split('-')[0])).group(0) and atom == hcch_tocsy_split[0].split('-')[2]:
                temp_list.append(float(hcch_tocsy_split[3]))
                spectra_list.append('HCCH TOCSY')

def check_peaklist_labels(NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,progress_bar):
    import checker as ch
    progress_bar.update_idletasks()
    progress_bar.pb2['value'] = 0
    progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
    if NHSQC_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 8.3
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.NHSQC_checker(NHSQC_file,NHSQC_directory,text_area)
    if HNCA_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 16.6
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HNCA_checker(HNCA_file,HNCA_directory,text_area)
    if HNCACB_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 24.9
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HNCACB_checker(HNCACB_file,HNCACB_directory,text_area)
    if HNCOCA_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 33.2
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HNCOCA_checker(HNCOCA_file,HNCOCA_directory,text_area)
    if HNCACO_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 41.6
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HNCACO_checker(HNCACO_file,HNCACO_directory,text_area)
    if CBCACONH_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 49.8
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.CBCACONH_checker(CBCACONH_file,CBCACONH_directory,text_area)
    if HCCONH_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 58.1
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HCCONH_checker(HCCONH_file,HCCONH_directory,text_area)
    if HNCO_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 66.4
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HNCO_checker(HNCO_file,HNCO_directory,text_area)
    if CHSQC_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 74.7
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.CHSQC_checker(CHSQC_file,CHSQC_directory,text_area)
    if HBHACONH_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 83
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HBHACONH_checker(HBHACONH_file,HBHACONH_directory,text_area)
    if CCH_TOCSY_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 91.3
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.CCH_TOCSY_checker(CCH_TOCSY_file,CCH_TOCSY_directory,text_area)
    if HCCH_TOCSY_file != ():
        progress_bar.update_idletasks()
        progress_bar.pb2['value'] == 100
        progress_bar.progress2['text']=int(progress_bar.pb['value']),'%'
        ch.HCCH_TOCSY_checker(HCCH_TOCSY_file,HCCH_TOCSY_directory,text_area)

def convert_bruker_files(HNCA_file,HNCACB_file,HNCO_file,HNCA_directory,HNCACB_directory,HNCO_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory):
    import convert_bruker as cb
    if HNCA_file != ():
        HNCA_file=cb.write_varian_file(HNCA_file,HNCA_directory)
    if HNCACB_file != ():
        HNCACB_file=cb.write_varian_file(HNCACB_file,HNCACB_directory)
    if HNCOCA_file != ():
        HNCOCA_file=cb.write_varian_file(HNCOCA_file,HNCOCA_directory)
    if HNCACO_file != ():
        HNCACO_file=cb.write_varian_file(HNCACO_file,HNCACO_directory)
    if CBCACONH_file != ():
        CBCACONH_file=cb.write_varian_file(CBCACONH_file,CBCACONH_directory)
    if HCCONH_file != ():
        HCCONH_file=cb.write_varian_file(HCCONH_file,HCCONH_directory)
    if HNCO_file != ():
        HNCO_file=cb.write_varian_file(HNCO_file,HNCO_directory)
    if HBHACONH_file != ():
        HBHACONH_file=cb.write_varian_file(HBHACONH_file,HBHACONH_directory)
    if CCH_TOCSY_file != ():
        CCH_TOCSY_file=cb.write_varian_file(CCH_TOCSY_file,CCH_TOCSY_directory)
    if HCCH_TOCSY_file != ():
        HCCH_TOCSY_file=cb.write_varian_file(HCCH_TOCSY_file,HCCH_TOCSY_directory)
    return HNCA_file, HNCACB_file, HNCOCA_file, HNCACO_file, HNCO_file, CBCACONH_file, HCCONH_file, HBHACONH_file, CCH_TOCSY_file, HCCH_TOCSY_file

def remove_converted_varian_files(HNCA_file,HNCACB_file,HNCO_file,HNCA_directory,HNCACB_directory,HNCO_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory):
    import convert_bruker as cb
    if HNCA_file != ():
        HNCA_file=cb.delete_varian_file(HNCA_file,HNCA_directory)
    if HNCACB_file != ():
        HNCACB_file=cb.delete_varian_file(HNCACB_file,HNCACB_directory)
    if HNCOCA_file != ():
        HNCOCA_file=cb.delete_varian_file(HNCOCA_file,HNCOCA_directory)
    if HNCACO_file != ():
        HNCACO_file=cb.delete_varian_file(HNCACO_file,HNCACO_directory)
    if CBCACONH_file != ():
        CBCACONH_file=cb.delete_varian_file(CBCACONH_file,CBCACONH_directory)
    if HCCONH_file != ():
        HCCONH_file=cb.delete_varian_file(HCCONH_file,HCCONH_directory)
    if HNCO_file != ():
        HNCO_file=cb.delete_varian_file(HNCO_file,HNCO_directory)
    if HBHACONH_file != ():
        HBHACONH_file=cb.delete_varian_file(HBHACONH_file,HBHACONH_directory)
    if CCH_TOCSY_file != ():
        CCH_TOCSY_file=cb.delete_varian_file(CCH_TOCSY_file,CCH_TOCSY_directory)
    if HCCH_TOCSY_file != ():
        HCCH_TOCSY_file=cb.delete_varian_file(HCCH_TOCSY_file,HCCH_TOCSY_directory)


def nmrstar_file(sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,seq_start_value,progress_bar):
    aa_dict={'D':'Asp','T':'Thr','S':'Ser','E':'Glu','P':'Pro','G':'Gly','A':'Ala','C':'Cys','V':'Val',
    'M':'Met','I':'Ile','L':'Leu','Y':'Tyr','F':'Phe','H':'His','K':'Lys','R':'Arg','W':'Trp','Q':'Gln','N':'Asn'}
    reg_list=regex_list(sequence_file,seq_directory,seq_start_value)
    progress_bar.pb2['value'] = 0
    progress_bar.progress2['text']=int(progress_bar.pb2['value']),'%'
    reg_list_size=len(reg_list)
    temp_list=[]
    nmrstar_list=[]
    spectra_list=[]
    counter=0
    for values in reg_list:
        if counter <= reg_list_size:
            progress_bar.update_idletasks()
            progress_bar.pb2['value'] += 100/reg_list_size
            progress_bar.progress2['text']=int(progress_bar.pb2['value']),'%'
        split_values=values.split('-')
        amino_acid=split_values[0][-1]
        residue_number=split_values[0][0:-1]
        atom=split_values[1]
        if NHSQC_file != ():
            os.chdir(NHSQC_directory)
            NHSQC_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,NHSQC_file,NHSQC_directory)
        if HNCA_file != ():
            os.chdir(HNCA_directory)
            HNCA_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCA_file,HNCA_directory)
        if HNCACB_file != ():
            os.chdir(HNCACB_directory)
            HNCACB_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCACB_file,HNCACB_directory)
        if CBCACONH_file !=():
            os.chdir(CBCACONH_directory)
            CBCACONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CBCACONH_file,CBCACONH_directory)
        if HCCONH_file !=():
            os.chdir(HCCONH_directory)
            HCCONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HCCONH_file,HCCONH_directory)
        if HNCACO_file !=():
            os.chdir(HNCACO_directory)
            HNCACO_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCACO_file,HNCACO_directory)
        if HNCOCA_file != ():
            os.chdir(HNCOCA_directory)
            HNCOCA_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCOCA_file,HNCOCA_directory)
        if HNCO_file != ():
            os.chdir(HNCO_directory)
            HNCO_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HNCO_file,HNCO_directory)
        if CHSQC_file != ():
            os.chdir(CHSQC_directory)
            CHSQC_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CHSQC_file,CHSQC_directory)
        if HBHACONH_file != ():
            os.chdir(HBHACONH_directory)
            HBHACONH_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HBHACONH_file,HBHACONH_directory)
        if CCH_TOCSY_file != ():
            os.chdir(CCH_TOCSY_directory)
            CCH_TOCSY_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,CCH_TOCSY_file,CCH_TOCSY_directory)
        if HCCH_TOCSY_file != ():
            os.chdir(HCCH_TOCSY_directory)
            HCCH_TOCSY_peaklist(amino_acid,residue_number,atom,temp_list,spectra_list,HCCH_TOCSY_file,HCCH_TOCSY_directory)
        if len(temp_list) == 0:
            continue
        counter+=1
        average=(sum(temp_list))/(len(temp_list))
        standard_deviation = (sum([((x - average) ** 2) for x in temp_list]) / len(temp_list))**0.5
        if standard_deviation > standard_deviation_value:
            text_area.insert(tk.INSERT,f'{values}\n')
            text_area.insert(tk.INSERT,f'{spectra_list}\n')
            text_area.insert(tk.INSERT,f'{temp_list}\n')
            text_area.update_idletasks()
        if atom[0] == 'C':
            nmrstar_list.append(f'{counter} {residue_number} {residue_number} {aa_dict[amino_acid]} {atom} C 13 {round(average,3)} {round(standard_deviation,2)} 0 1')
        if atom[0] == 'N':
            nmrstar_list.append(f'{counter} {residue_number} {residue_number} {aa_dict[amino_acid]} {atom} N 15 {round(average,3)} {round(standard_deviation,2)} 0 1')
        if atom[0] == 'H':
            nmrstar_list.append(f'{counter} {residue_number} {residue_number} {aa_dict[amino_acid]} {atom} H 1 {round(average,3)} {round(standard_deviation,2)} 0 1')
        temp_list.clear()
        spectra_list.clear()
    rows = [line.split() for line in nmrstar_list]
    columns = zip(*rows)
    col_widths = [max(len(e) for e in column) for column in columns]

    new_data = []
    for row in rows:
        new_row = ''
        for e, width in zip(row, col_widths):
            new_row += f"{e:>{width}} "
        new_data.append(new_row)
    os.chdir(save_directory)
    with open(save_file,'w') as file:
        file.write('loop_\n    _Atom_chem_shift.ID\n    _Atom_chem_shift.Comp_index_ID\n    _Atom_chem_shift.Seq_ID\n    _Atom_chem_shift.Comp_ID\n    _Atom_chem_shift.Atom_ID\n    _Atom_chem_shift.Atom_type\n    _Atom_chem_shift.Atom_isotope_number\n    _Atom_chem_shift.Val\n    _Atom_chem_shift.Val_err\n    _Atom_chem_shift.Ambiguity_code\n     _Atom_chem_shift.Assigned_chem_shift_list_ID\n')
        for row in new_data:
            file.write(f'{row.upper()}\n')
        file.write('stop_')




def compare_to_bmrb(bmrb_file,bmrb_directory,save_file,save_directory,text_area,progress_bar):
    text_area.insert(tk.INSERT,'Comparing to BMRB Values\n')
    text_area.update_idletasks()
    os.chdir(save_directory)
    num_lines = (sum(1 for line in open(save_file)))-13
    progress_bar.pb2['value'] = 0
    progress_bar.progress2['text']=int(progress_bar.pb2['value']),'%'
    progress_bar.update_idletasks()
    with open(save_file) as file:
        for lines in file:
            progress_bar.update_idletasks()
            progress_bar.pb2['value'] += 100/num_lines
            progress_bar.progress2['text']=int(progress_bar.pb2['value']),'%'
            if re.search('^\d+',lines.strip()) is None:
                continue
            star_residue=lines.split()[1]
            star_amino_acid=lines.split()[3].upper()
            star_atom=lines.split()[4]
            star_value=lines.split()[7]
            os.chdir(bmrb_directory)
            with open(bmrb_file) as file2:
                for lines2 in file2:
                    if lines2 == '\n':
                        continue
                    split_lines=lines2.split(',')
                    residue=split_lines[0]
                    if residue == 'comp_id':
                        continue
                    atom=split_lines[1]
                    chemical_shift=float(split_lines[5])
                    std=float(split_lines[6])
                    lower_half=chemical_shift-std
                    upper_half=chemical_shift+std
                    if star_amino_acid == residue and star_atom == atom:
                        if float(star_value) > (upper_half+(0.05*upper_half)):
                            text_area.insert(tk.INSERT,f'{star_amino_acid} {star_residue} {star_atom} value {star_value} is outside of range {round(lower_half,3)}-{round(upper_half,3)}\n')
                            text_area.update_idletasks()
                        if float(star_value) < (lower_half-(0.05*lower_half)):
                            text_area.insert(tk.INSERT,f'{star_amino_acid} {star_residue} {star_atom} value {star_value} is outside of range {round(lower_half,3)}-{round(upper_half,3)}\n')
                            text_area.update_idletasks()

def main_loop(sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,bmrb_file,bmrb_directory,terminal_flag,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,seq_start_value,Bruker_check,Keep_file_check,second_window):
    new_top=ProgressBar(second_window)
    progress_bar = new_top.pbWindow
    progress_bar.update_idletasks()
    progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
    progress_bar.update_bar['text']='Starting Program'
    text_area.insert(tk.INSERT,'Starting Program\n')
    if Bruker_check.get() != 0:
        progress_bar.update_idletasks()
        progress_bar.pb['value'] = 10
        progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
        progress_bar.update_bar['text']='Converting from Bruker format to Varian'
        text_area.insert(tk.INSERT,'Converting from Bruker format to Varian\n')
        HNCA_file, HNCACB_file, HNCOCA_file, HNCACO_file, HNCO_file, CBCACONH_file, HCCONH_file, HBHACONH_file, CCH_TOCSY_file, HCCH_TOCSY_file = convert_bruker_files(HNCA_file,HNCACB_file,HNCO_file,HNCA_directory,HNCACB_directory,HNCO_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory)
    progress_bar.update_idletasks()
    progress_bar.pb['value'] = 33
    progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
    progress_bar.update_bar['text']='Checking proper labeling and formatting in peaklists'
    check_peaklist_labels(NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,progress_bar)
    text_area.update_idletasks()
    progress_bar.update_idletasks()
    progress_bar.pb['value'] = 66
    progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
    progress_bar.update_bar['text']='Check Complete'
    text_area.insert(tk.INSERT,'Check Complete\n')
    text_area.insert(tk.INSERT,'\nIf any errors were found, please correct and rerun \n')
    if terminal_flag is True:
        question=input('If no errors were found, type "continue". Otherwise, type "quit", correct errors, and rerun: ')
        if question=='quit':
            sys.exit()
    progress_bar.update_bar['text']='Generating NMRSTAR File'
    text_area.insert(tk.INSERT,'\nGenerating NMRSTAR File (Takes a minute depending on size of protein)\n')
    text_area.update_idletasks()
    nmrstar_file(sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,seq_start_value,progress_bar)
    try:
        progress_bar.pb['value'] = 88
        progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
        progress_bar.update_bar['text']='Comparing to bmrb'
        compare_to_bmrb(bmrb_file,bmrb_directory,save_file,save_directory,text_area,progress_bar)
        progress_bar.pb['value'] = 100
        progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
        progress_bar.update_bar['text']='Program Complete'
        progress_bar.update_idletasks()
        time.sleep(1)
        progress_bar.destroy()
        text_area.insert(tk.INSERT,'Program Complete, Please exit window\n')
        text_area.update_idletasks()
    except:
        if Keep_file_check.get() == 0 and Bruker_check.get() != 0:
            remove_converted_varian_files(HNCA_file,HNCACB_file,HNCO_file,HNCA_directory,HNCACB_directory,HNCO_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory)
        elif Keep_file_check.get() != 0 and Bruker_check.get() != 0:
            text_area.insert(tk.INSERT,'Converted Bruker files are in the same directory as original files\n')
            progress_bar.pb['value'] = 100
            progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
            progress_bar.update_bar['text']='Program Complete'
            progress_bar.update_idletasks()
            time.sleep(1)
            progress_bar.destroy()
            text_area.insert(tk.INSERT,'Program Complete, Please exit window\n')
            text_area.update_idletasks()
        else:
            progress_bar.pb['value'] = 100
            progress_bar.progress['text']=int(progress_bar.pb['value']),'%'
            progress_bar.update_bar['text']='Program Complete'
            progress_bar.update_idletasks()
            time.sleep(1)
            progress_bar.destroy()
            text_area.insert(tk.INSERT,'Program Complete, Please exit window\n')
            text_area.update_idletasks()
