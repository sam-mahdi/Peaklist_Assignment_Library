from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os
import functools
import tkinter.scrolledtext as st
from tkinter import ttk



NHSQC_file=()
NHSQC_directory=()
HNCA_file=()
HNCA_directory=()
HNCACB_file=()
HNCACB_directory=()
HNCO_file=()
HNCO_directory=()
HNCOCA_file=()
HNCOCA_directory=()
CBCACONH_file=()
CBCACONH_directory=()
HNCACO_file=()
HNCACO_directory=()
HCCONH_file=()
HCCONH_directory=()
CHSQC_file=()
CHSQC_directory=()
HBHACONH_file=()
HBHACONH_directory=()
CCH_TOCSY_file=()
CCH_TOCSY_directory=()
HCCH_TOCSY_file=()
HCCH_TOCSY_directory=()
sequence_file=()
seq_directory=()
save_file=()
save_directory=()
text_area=()
bmrb_file=()
bmrb_directory=()
seq_start_value=()
Bruker_check= IntVar()
Keep_file_check= IntVar()

standard_deviation_value=()

class ReadOnlyText(st.ScrolledText):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state=tk.DISABLED)

        self.insert = self._unlock(super().insert)
        self.delete = self._unlock(super().delete)

    def _unlock(self, f):
        @functools.wraps(f)
        def wrap(*args, **kwargs):
            self.config(state=tk.NORMAL)
            r = f(*args, **kwargs)
            self.config(state=tk.DISABLED)
            return r
        return wrap

class newTopLevel(object):
    def __init__(self, root):
        global text_area
        self.newWindow = Toplevel(root)
        self.newWindow.title("SPARKY to NMRSTAR 3.1")
        self.newWindow.geometry("1200x800")
        tk.Label(self.newWindow, text="Sequence File").grid(row=0)
        tk.Label(self.newWindow, text="NHSQC Peaklist").grid(row=1)
        tk.Label(self.newWindow, text="HNCA  Peaklist").grid(row=2)
        tk.Label(self.newWindow, text="HNCACB  Peaklist").grid(row=3)
        tk.Label(self.newWindow, text="HNCO  Peaklist").grid(row=4)
        tk.Label(self.newWindow, text="CHSQC  Peaklist").grid(row=5)
        tk.Label(self.newWindow, text="HBHACONH  Peaklist").grid(row=6)
        tk.Label(self.newWindow, text="CCH_TOCSY  Peaklist").grid(row=7)
        tk.Label(self.newWindow, text="HCCH_TOCSY  Peaklist").grid(row=8)
        tk.Label(self.newWindow, text="NMRSTAR Save File").grid(row=9)
        tk.Label(self.newWindow, text="Set Standard Deviation (click enter when done)").grid(row=10)
        tk.Label(self.newWindow, text="Sequence Start Value").grid(row=11)
        tk.Label(self.newWindow, text="If BMRB Comparison is desired, upload BMRB file here").grid(row=12)
        seq_line = tk.Entry(self.newWindow).grid(row=0, column=1)
        nhsqc_line = tk.Entry(self.newWindow).grid(row=1, column=1)
        hnca_line = tk.Entry(self.newWindow).grid(row=2, column=1)
        hncacb_line = tk.Entry(self.newWindow).grid(row=3, column=1)
        hnco_line = tk.Entry(self.newWindow).grid(row=4, column=1)
        chsqc_line = tk.Entry(self.newWindow).grid(row=5, column=1)
        hbhaconh_line = tk.Entry(self.newWindow).grid(row=6, column=1)
        cch_tocsy_line = tk.Entry(self.newWindow).grid(row=7, column=1)
        hcch_tocsy_line = tk.Entry(self.newWindow).grid(row=8, column=1)
        save_file_line = tk.Entry(self.newWindow).grid(row=9, column=1)
        self.standard_deviation_line = tk.Entry(self.newWindow)
        self.standard_deviation_line.grid(row=10, column=1)
        self.seq_start_line = tk.Entry(self.newWindow)
        self.seq_start_line.grid(row=11, column=1)
        bmrb_file_line = tk.Entry(self.newWindow).grid(row=12, column=1)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.input_seq)
        self.newWindow.btn.grid(row=0,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.NHSQC)
        self.newWindow.btn.grid(row=1,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.HNCA)
        self.newWindow.btn.grid(row=2,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.HNCACB)
        self.newWindow.btn.grid(row=3,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.HNCO)
        self.newWindow.btn.grid(row=4,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.CHSQC)
        self.newWindow.btn.grid(row=5,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.HBHACONH)
        self.newWindow.btn.grid(row=6,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.CCH_TOCSY)
        self.newWindow.btn.grid(row=7,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.HCCH_TOCSY)
        self.newWindow.btn.grid(row=8,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.save_file)
        self.newWindow.btn.grid(row=9,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Enter',command=self.standard_deviation)
        self.newWindow.btn.grid(row=10,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Enter',command=self.seq_start)
        self.newWindow.btn.grid(row=11,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='browse',command=self.bmrb_file)
        self.newWindow.btn.grid(row=12,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Run',command=self.run_spartytonmrstar)
        self.newWindow.btn.grid(row=14,column=1)
        self.newWindow.btn = tk.Button(self.newWindow,text='Quit',command=self.newWindow.destroy)
        self.newWindow.btn.grid(row=15,column=1)
        self.newWindow.btn = tk.Button(self.newWindow,text='Assignment Completion',command=self.assignment_completion)
        self.newWindow.btn.grid(row=14,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Custom Percent Calculator',command=self.custom_assignment_completion)
        self.newWindow.btn.grid(row=15,column=2)
        self.newWindow.btn = tk.Button(self.newWindow,text='Additional_NMR_Experiments',command=self.nmr_experiments)
        self.newWindow.btn.grid(row=13,column=1)
        tk.Checkbutton(self.newWindow, text="Bruker", variable=Bruker_check).grid(row=13,column=0,stick=W)
        tk.Checkbutton(self.newWindow, text="Keep Varian Files", variable=Keep_file_check).grid(row=13,column=0)



        ttk.Label(self.newWindow,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 15)

        text_area = ReadOnlyText(self.newWindow,height=17,font = ("Times New Roman",12))

        text_area.grid(column = 0,columnspan=5,sticky=W+E)
    def input_seq(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global sequence_file
        global seq_directory
        seq_directory=os.path.dirname(fullpath)
        sequence_file= os.path.basename(fullpath)
        if sequence_file == '' or seq_directory == '':
            sequence_file=()
            seq_directory=()
        label3=Label(self.newWindow,text=fullpath).grid(row=0,column=1)

    def NHSQC(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global NHSQC_file
        global NHSQC_directory
        NHSQC_directory=os.path.dirname(fullpath)
        NHSQC_file= os.path.basename(fullpath)
        if NHSQC_file == '' or NHSQC_directory == '':
            NHSQC_file=()
            NHSQC_directory=()
        label4=Label(self.newWindow,text=fullpath).grid(row=1,column=1)
    def HNCA(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global HNCA_file
        global HNCA_directory
        HNCA_directory=os.path.dirname(fullpath)
        HNCA_file= os.path.basename(fullpath)
        if HNCA_file == '' or HNCA_directory == '':
            HNCA_file=()
            HNCA_directory=()
        label5=Label(self.newWindow,text=fullpath).grid(row=2,column=1)

    def HNCACB(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global HNCACB_file
        global HNCACB_directory
        HNCACB_directory=os.path.dirname(fullpath)
        HNCACB_file= os.path.basename(fullpath)
        if HNCACB_file == '' or HNCACB_directory == '':
            HNCACB_file=()
            HNCACB_file=()
        label6=Label(self.newWindow,text=fullpath).grid(row=3,column=1)

    def HNCO(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global HNCO_file
        global HNCO_directory
        HNCO_directory=os.path.dirname(fullpath)
        HNCO_file= os.path.basename(fullpath)
        if HNCO_file == '' or HNCO_directory == '':
            HNCO_file=()
            HNCO_directory=()
        label7=Label(self.newWindow,text=fullpath).grid(row=4,column=1)
    def CHSQC(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global CHSQC_file
        global CHSQC_directory
        CHSQC_directory=os.path.dirname(fullpath)
        CHSQC_file= os.path.basename(fullpath)
        if CHSQC_directory == '' or CHSQC_file == '':
            CHSQC_file=()
            CHSQC_directory=()
        label7=Label(self.newWindow,text=fullpath).grid(row=5,column=1)
    def HBHACONH(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global HBHACONH_file
        global HBHACONH_directory
        HBHACONH_directory=os.path.dirname(fullpath)
        HBHACONH_file= os.path.basename(fullpath)
        if HBHACONH_file == '' or HBHACONH_directory == '':
            HBHACONH_file=()
            HBHACONH_directory=()
        label7=Label(self.newWindow,text=fullpath).grid(row=6,column=1)
    def CCH_TOCSY(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global CCH_TOCSY_file
        global CCH_TOCSY_directory
        CCH_TOCSY_directory=os.path.dirname(fullpath)
        CCH_TOCSY_file= os.path.basename(fullpath)
        if CCH_TOCSY_file == '' or CCH_TOCSY_directory =='':
            CCH_TOCSY_file=()
            CCH_TOCSY_directory=()
        label7=Label(self.newWindow,text=fullpath).grid(row=7,column=1)
    def HCCH_TOCSY(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global HCCH_TOCSY_file
        global HCCH_TOCSY_directory
        HCCH_TOCSY_directory=os.path.dirname(fullpath)
        HCCH_TOCSY_file= os.path.basename(fullpath)
        if HCCH_TOCSY_file == '' or HCCH_TOCSY_directory == '':
            HCCH_TOCSY_file=()
            HCCH_TOCSY_directory=()
        label7=Label(self.newWindow,text=fullpath).grid(row=8,column=1)
    def save_file(self):
        myFormats = [('Text File','*.txt'),]
        fullpath = tk.filedialog.asksaveasfilename(parent=self.newWindow,filetypes=myFormats ,title="Save the file as...")
        global save_file
        global save_directory
        save_directory=os.path.dirname(fullpath)
        save_file=os.path.basename(fullpath)
        if save_file == '' or save_directory == '':
            save_file=()
            save_directory=()
        label8=Label(self.newWindow,text=fullpath).grid(row=9,column=1)
    def bmrb_file(self):
        fullpath = filedialog.askopenfilename(parent=self.newWindow, title='Choose a file')
        global bmrb_file
        global bmrb_directory
        bmrb_directory=os.path.dirname(fullpath)
        bmrb_file= os.path.basename(fullpath)
        label7=Label(self.newWindow,text=fullpath).grid(row=12,column=1)
    def nmr_experiments(self):
        from additional_nmr_experiments_window import nmr_experiment_window
        experiments_window = nmr_experiment_window(self.newWindow)
        experimentswindow = experiments_window.experimentswindow


    def standard_deviation(self):
        standard_deviation_input=self.standard_deviation_line.get()
        global standard_deviation_value
        standard_deviation_value=float(standard_deviation_input)
        text_area.insert(tk.INSERT,f'Standard Deviation set: {standard_deviation_input} \n')

    def seq_start(self):
        seq_start_input=self.seq_start_line.get()
        global seq_start_value
        seq_start_value=float(seq_start_input)
        text_area.insert(tk.INSERT,f'Sequence starts at: {seq_start_input} \n')

    def run_spartytonmrstar(self):
        text_area.delete(1.0,END)
        if sequence_file == ():
            text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
        if standard_deviation_value == ():
            text_area.insert(tk.INSERT,'please enter a standard devation value (make sure to click enter)\n')
        if seq_start_value == ():
            text_area.insert(tk.INSERT,'please enter a sequence start value (make sure to click enter)\n')
        if save_file == ():
            text_area.insert(tk.INSERT,'please add the save file (make sure to use browse)\n')
        else:
            try:
                terminal_flag=False
                from SPARKYtoNMRSTAR3p1 import main_loop
                from additional_nmr_experiments_window import get_variables
                second_window=self.newWindow
                HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory=get_variables()
                main_loop(sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,text_area,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,bmrb_file,bmrb_directory,terminal_flag,HNCACO_file,HNCACO_directory,HNCOCA_file,HNCOCA_directory,CBCACONH_file,CBCACONH_directory,HCCONH_file,HCCONH_directory,seq_start_value,Bruker_check,Keep_file_check,second_window)
            except:
                text_area.insert(tk.INSERT,'Unknown Error, Program could not run. Restart and try again. If it still fails, Please Contact Support.')
                #print(traceback.print_exc())
    def assignment_completion(self):
        from percent_assigned import calculate_percentage
        calculate_percentage(sequence_file,seq_directory,save_file,save_directory,text_area)
    def custom_assignment_completion(self):
        if sequence_file == ():
            text_area.insert(tk.INSERT,'please upload your seq file (make sure to use browse)\n')
        if save_file == ():
            text_area.insert(tk.INSERT,'please add the save file (make sure to use browse)\n')
        else:
            from sparky_assingment_window import SparkyWindow
            sparky_top = SparkyWindow(self.newWindow,sequence_file,seq_directory,save_file,save_directory)
            newSparkyWindow = sparky_top.sparky_assign_window
