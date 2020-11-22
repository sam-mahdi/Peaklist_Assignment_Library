import re
import os
import tkinter as tk

backbones={'D':1,'T':1,'S':1,'E':1,'G':1,'A':1,'C':1,'V':1,'M':1,'I':1,'L':1,'Y':1,'F':1,'H':1,'K':1,'R':1,'W':1,'Q':1,'N':1}
alphas_betas={'D':2,'T':2,'S':2,'E':2,'P':2,'G':1,'A':2,'C':2,'V':2,'M':2,'I':2,'L':2,'Y':2,'F':2,'H':2,'K':2,'R':2,'W':2,'Q':2,'N':2}
gammas={'T':1,'E':1,'P':1,'V':2,'M':1,'I':2,'L':1,'K':1,'R':1,'Q':1}
deltas={'P':1,'M':1,'I':1,'L':2,'K':1,'R':1}
epsilons={'M':1,'K':1}
methyls={'I':2,'L':2,'V':2,'T':1}
Total_atoms={'D':4,'T':5,'S':4,'E':5,'G':3,'A':4,'C':4,'V':6,'M':7,'I':7,'L':7,'Y':4,'F':4,'H':4,'K':7,'R':6,'W':4,'Q':6,'N':5}

def calculate_percentage(sequence_file,seq_directory,save_file,save_directory,text_area):
    alphas_betas_count=0
    gammas_count=0
    deltas_count=0
    epsilons_count=0
    methyl_count=0
    backbone_count=0
    total_atom_count=0
    #using the above dictionary, these calculate how many alphas, betas, gammas, detlas, and epsilons you have based off
    #your sequence
    os.chdir(seq_directory)
    with open(sequence_file) as seq_file:
        for lines in seq_file:
            for amino_acid in lines:
                if amino_acid == '>' or amino_acid == '\n':
                    continue
                backbone = backbones.get(amino_acid)
                alpha_beta = alphas_betas.get(amino_acid)
                gamma = gammas.get(amino_acid)
                delta = deltas.get(amino_acid)
                epsilon = epsilons.get(amino_acid)
                methyl = methyls.get(amino_acid)
                all_atoms=Total_atoms.get(amino_acid)
                if alpha_beta is not None:
                    alphas_betas_count+=alpha_beta
                if gamma is not None:
                    gammas_count+=gamma
                if delta is not None:
                    deltas_count+=delta
                if epsilon is not None:
                    epsilons_count+=epsilon
                if methyl is not None:
                    methyl_count+=methyl
                if backbone is not None:
                    backbone_count+=backbone
                if all_atoms is not None:
                    total_atom_count+=all_atoms

    alphas_assigned=0
    betas_assigned=0
    gammas_assigned=0
    deltas_assigned=0
    epsilons_assigned=0
    methyls_assigned=0
    backbone_assigned=0
    total_atoms_assigned=0
    #counds how many alphas,betas...you have assigned in your peaklist
    #all secondary assignments are removed so each CD2, CG2, is counted only as 1 assignment
    os.chdir(save_directory)
    with open(save_file) as file:
      for letter in file:
          searcher=re.search('^\d+',letter.strip())
          if searcher is None:
              continue
          atom_type=letter.strip().split()[4]
          amino_acid_type=letter.strip().split()[3].upper()
          if atom_type == 'N':
              backbone_assigned+=1
          if atom_type == 'CE':
            epsilons_assigned+=1
          if atom_type in {'CD1','CD2','CD'}:
              deltas_assigned+=1
          if atom_type in {'CG','CG1','CG2'}:
              gammas_assigned+=1
          if atom_type == 'CB':
            betas_assigned+=1
          if atom_type == 'CA':
            alphas_assigned+=1
          if amino_acid_type in {'THR','ILE','LEU','VAL'} and atom_type in {'CD1','CD2','CG1','CG2'}:
              if amino_acid_type == 'ILE' and atom_type == 'CG1':
                  continue
              methyls_assigned+=1
          if atom_type in {'N','C','CA','CB','CG','CG1','CG2','CD1','CD2','CD','CE','NE2'}:
              total_atoms_assigned+=1

    percent_alphas_betas_assigned=int(((alphas_assigned+betas_assigned)/alphas_betas_count)*100)
    percent_gammas_assigned=int((gammas_assigned/gammas_count)*100)
    percent_deltas_assigned=int((deltas_assigned/deltas_count)*100)
    percent_epsilons_assigned=int((epsilons_assigned/epsilons_count)*100)
    percent_methyls_assigned=int((methyls_assigned/methyl_count)*100)
    percent_backbone_assigned=int((backbone_assigned/backbone_count)*100)
    percent_total_assigned=int((total_atoms_assigned/total_atom_count)*100)

    text_area.insert(tk.INSERT,f'\nAssignment Percent Completion\n')
    text_area.insert(tk.INSERT,f'Percentage of backbone assigned: {percent_backbone_assigned}%\n')
    text_area.insert(tk.INSERT,f'Percentage of alphas and betas assigned: {percent_alphas_betas_assigned}% \n')
    text_area.insert(tk.INSERT,f'Percentage of deltas assigned:  {percent_deltas_assigned}% \n')
    text_area.insert(tk.INSERT,f'Percentage of gammas assigned: {percent_gammas_assigned}% \n')
    text_area.insert(tk.INSERT,f'Percentage of epsilons assigned: {percent_epsilons_assigned}%\n')
    text_area.insert(tk.INSERT,f'Percentage of methyls assigned: {percent_methyls_assigned}%\n')
    text_area.insert(tk.INSERT,f'Percentage of all atoms assigned: {percent_total_assigned}%\n')
    text_area.update_idletasks()
