from tkinter import *
from tkinter import ttk
import tkinter as tk
# from main import *

window = tk.Tk()
window.resizable(0,0)
window.title('Genetic code treater')
for i in range(2):
    window.columnconfigure(i, weight= 1)
for i in range(2):
    window.rowconfigure(i, weight = 1)
for i in range(2,5,2):
    window.rowconfigure(i, weight = 1)
    window.rowconfigure(i+1, weight = 1)
window.rowconfigure(6, weight = 1, minsize = 60)

standard_padx = 5

# top

def call_code():
    code_win = tk.Toplevel(window)
    code_win.title('Standard genetic code')
    code_win.resizable(0,0)
    code_label = tk.Label(code_win)
    code_label.image = tk.PhotoImage(file = './dna_code.png')
    code_label['image'] = code_label.image
    code_label.pack()

top_menubar = tk.Menu(master = window)
file_menu = tk.Menu(master = top_menubar, tearoff=0)
file_menu.add_command(label = 'Read fasta file')
file_menu.add_separator()
file_menu.add_command(label = 'Exit', command = window.quit)

top_menubar.add_cascade(label = 'File', menu = file_menu)
top_menubar.add_command(label = 'Tools', command = call_code)
window.config(menu = top_menubar)


# generator
generation_button, generation_entry = [tk.Button(master = window, text = 'generate'), tk.Entry(master = window,width=10)]
generation_button.grid(column = 0, row = 1, sticky = 'W', padx= standard_padx)
generation_entry.grid(column = 1, row = 1, sticky = 'E', padx= standard_padx)
generation_entry.insert(0, '100')

# original sequence
oseq_label = tk.Label(text='Original DNA sequence')
oseq_text = tk.Text(height= 5, width=65)
oseq_label.grid(row = 2, sticky= 'W', padx= standard_padx)
oseq_text.grid(row = 3, columnspan=2, padx= standard_padx, pady = 3)

# derived sequence
dseq_label = tk.Label(text = 'Sequence DNA:')
dseq_var = tk.IntVar()
dseq_button_reverse = tk.Checkbutton(text = 'Reverse', onvalue= 1, variable=dseq_var)
dseq_button_complementary = tk.Checkbutton(text = 'Complementary', onvalue= 2, variable = dseq_var)
dseq_text = tk.Text(height=5, width = 65)
dseq_label.grid(row=4, column = 0, sticky='W' ,padx = standard_padx)
dseq_button_reverse.grid(row=4, column = 1, sticky='E', padx= standard_padx)
dseq_button_complementary.grid(row=4, column = 1, sticky='W', padx= standard_padx)
dseq_text.grid(row = 5, columnspan=2, padx= standard_padx, pady = 3)

# protein, main space
pseq_label = tk.Label(text = 'Protein\nsequence')
frames_height, frames_width  = [55, 100]
pseq_frame1, pseq_frame2 = [
    tk.Frame(master = window, height = frames_height, width = frames_width, bd = 2, relief='groove'),
    tk.Frame(master = window, height = frames_height, width = frames_width, bd = 2, relief ='groove')
 ]
pseq_text = tk.Text(height= 5, width=65)
pseq_label.grid(row = 6, column= 0, sticky= 'W', padx= standard_padx)
pseq_frame1.grid(row=6, column = 1, sticky='W', padx= standard_padx)
pseq_frame2.grid(row=6, column = 1, sticky='E', padx= standard_padx)
pseq_text.grid(row = 7, columnspan = 2,padx= standard_padx, pady = 3)
rf_label = tk.Label(master = pseq_frame1, text = 'Reading\nframe')
cs_label = tk.Label(master = pseq_frame2, text = 'AA Code\nLength ')
rf_label.pack(anchor="w", side = 'left')
cs_label.pack(side = 'left')

# protein, buttons
rf_var = tk.IntVar(value=2)
pseq_rf1 = tk.Radiobutton(master = pseq_frame1,text = '1', variable= rf_var, value = 1)
pseq_rf2 = tk.Radiobutton(master = pseq_frame1,text = '2', variable= rf_var, value = 2)
pseq_rf3 = tk.Radiobutton(master = pseq_frame1,text = '3', variable= rf_var, value = 3)
pseq_rf1.pack()
pseq_rf2.pack()
pseq_rf3.pack()
cs_var = IntVar(value = 1)
pseq_cs1 = tk.Radiobutton(master = pseq_frame2, text = '1', variable = cs_var, value= 1)
pseq_cs3 = tk.Radiobutton(master = pseq_frame2, text = '3', variable = cs_var, value= 3)
pseq_cs1.pack()
pseq_cs3.pack()
pseq_frame1.pack_propagate(0)
pseq_frame2.pack_propagate(0)



window.mainloop()

