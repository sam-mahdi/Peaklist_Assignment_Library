import tkinter as tk
from tkinter import filedialog
import os
import tkinter.scrolledtext as st
from tkinter import ttk
import functools
from tkinter import *
import webbrowser

root = tk.Tk()
root.title('SAG')

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


ttk.Label(root,text = "Program Output",font = ("Times New Roman", 15),background = 'green',foreground = "white").grid(column = 0, row = 14)

text_area = ReadOnlyText(root,width = 40,height = 10,font = ("Times New Roman",12))

text_area.grid(column = 0,columnspan=2,sticky=W+E,pady = 10, padx = 10)


tk.Label(root, text="Amide Nitrogen Chemical Shift (if no value, leave blank)").grid(row=0)
tk.Label(root, text="Carbonyl Carbon Chemical Shift (if no value, leave blank)").grid(row=1)
tk.Label(root, text="Alpha Carbon Chemical Shift (if no value, leave blank)").grid(row=2)
tk.Label(root, text="Beta Carbon Chemical Shift (if no value, leave blank)").grid(row=3)
tk.Label(root, text="Amide Hydrogen Chemical Shift (if no value, leave blank)").grid(row=4)
tk.Label(root, text="Save file name (use browse)").grid(row=5)


e1 = tk.Entry(root)
e2 = tk.Entry(root)
e3 = tk.Entry(root)
e4 = tk.Entry(root)
e5 = tk.Entry(root)
e6 = tk.Entry(root)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)

save_file_peaklist=()
save_directory=()

list_of_shifts=[]
i=0

def generate_files():
  nitrogen=e1.get()
  carbon=e2.get()
  alpha_carbon=e3.get()
  beta_carbon=e4.get()
  hydrogen=e5.get()
  text_area.insert(tk.INSERT,f'added amide nitrogen: {nitrogen}\n')
  text_area.insert(tk.INSERT,f'added carbonyl carbon: {carbon}\n')
  text_area.insert(tk.INSERT,f'added alpha carbon: {alpha_carbon}\n')
  text_area.insert(tk.INSERT,f'added beta carbon: {beta_carbon}\n')
  text_area.insert(tk.INSERT,f'added amide hydrogen: {hydrogen}\n')
  global list_of_shifts
  global i
  i+=1
  if nitrogen != '':
      list_of_shifts.append(f'X{i}N-HN {float(nitrogen)}\n')
  else:
      list_of_shifts.append(f'X{i}N-HN 1000\n')
  list_of_shifts.append(f'X{i}N-HA 1000\n')
  if carbon != '':
      if float(alpha_carbon)<50:
          list_of_shifts.append(f'X{i}HA2-HA 1000\n')
          list_of_shifts.append(f'X{i}C {float(carbon)}\n')
      else:
          list_of_shifts.append(f'X{i}C {float(carbon)}\n')
  else:
    list_of_shifts.append(f'X{i}C 1000\n')
  if alpha_carbon != '':
    list_of_shifts.append(f'X{i}CA-HN {float(alpha_carbon)}\n')
  else:
    list_of_shifts.append(f'X{i}CA-HN 1000\n')
  if beta_carbon != '':
    list_of_shifts.append(f'X{i}CB-HN {float(beta_carbon)}\n')
  else:
      if float(alpha_carbon)<50:
          pass
      else:
          list_of_shifts.append(f'X{i}CB-HN 1000\n')
  if hydrogen != '':
    list_of_shifts.append(f'X{i}N-HN {float(hydrogen)}\n')
  else:
    list_of_shifts.append(f'X{i}N-HN 1000\n')

def save_file2():
    myFormats = [('Text File','*.txt'),]
    fullpath = tk.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save the image as...")
    global save_file_peaklist
    global save_directory
    save_directory=os.path.dirname(fullpath)
    save_file_peaklist=os.path.basename(fullpath)
    label8=Label(root,text=fullpath).grid(row=5,column=1)

def help():
    webbrowser.open('https://github.com/sam-mahdi/SPARKY-Assignment-Tools/blob/master/SAG/HELP/SAG%20Manual.md')


def write_file():
    if save_file_peaklist == ():
        text_area.insert(tk.INSERT,'please indicate your save file (make sure to use browse)\n')
    else:
        os.chdir(save_directory)
        joined=''.join(list_of_shifts)
        with open(save_file_peaklist,'w') as file:
            for values in joined:
                file.write(values)
        text_area.insert(tk.INSERT,'File written\n')

tk.Button(root,text='enter values',command=generate_files).grid(row=6,column=0)
tk.Button(root,text='save/write file',command=write_file).grid(row=6,column=1)
tk.Button(root,text='browse',command=save_file2).grid(row=5,column=2)
tk.Button(root,text='quit',command=root.quit).grid(row=6,column=2)
tk.Button(root,text='help',command=help).grid(row=4,column=0)




root.mainloop()

