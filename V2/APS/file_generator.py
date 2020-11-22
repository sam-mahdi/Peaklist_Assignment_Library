list_of_shifts=[]

def generate_files():
  global list_of_shifts
  text_area.insert(tk.INSERT,f'added amide nitrogen: {nitrogen}\n')
  text_area.insert(tk.INSERT,f'added alpha hydrogen: {alpha_hydrogen}\n')
  text_area.insert(tk.INSERT,f'added alpha hydrogen2: {alpha_hydrogen}\n')
  text_area.insert(tk.INSERT,f'added carbonyl carbon: {carbon}\n')
  text_area.insert(tk.INSERT,f'added alpha carbon: {alpha_carbon}\n')
  text_area.insert(tk.INSERT,f'added beta carbon: {beta_carbon}\n')
  text_area.insert(tk.INSERT,f'added amide hydrogen: {hydrogen}\n')
  if nitrogen != '':
      list_of_shifts.append(nitrogen)
  else:
      list_of_shifts.append('1000.00')
  if alpha_hydrogen != '':
      list_of_shifts.append(alpha_hydrogen)
  else:
      list_of_shifts.append('1000.00')
  if alpha_hydrogen2 != '' and beta_carbon == '':
      list_of_shifts.append(alph_hydrogen)
  if carbon != '':
      list_of_shifts.append(carbon)
  else:
    list_of_shifts.append('1000.00')
  if alpha_carbon != '':
    list_of_shifts.append(alpha_carbon)
  else:
    list_of_shifts.append('1000.00')
  if beta_carbon != '' and alpha_hydrogen2 == '':
    list_of_shifts.append(beta_carbon)
  else:
      list_of_shifts.append('1000.00')
  if hydrogen != '':
    list_of_shifts.append(hydrogen)
  else:
    list_of_shifts.append('1000.00')
