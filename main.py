import tkinter as tk
from tkinter import filedialog
import random
import re
from settings import *
import fastareader as fasta

class DNA(tk.Frame):
    # realize the cheking on the gui level
    # GUI part
    gcode = 0
    Protein = None
    edna = None

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.menu = tk.Menu(master)
        self.createMenu()
        self.dna_frame = tk.Frame(master)
        self.createDNA()
        self.dna_derivatives_frame = tk.Frame(master)
        self.dseq_var = tk.IntVar()
        self.createDNAderivatives()
        master.config(menu = self.menu)
        self.dna_frame.pack(fill = "x", padx = common_padx)
        self.dna_derivatives_frame.pack(fill = 'x', padx = common_padx)

    def call_code(self):
        def gcode_minus(self):
            self.gcode = 0
            self.code_win.destroy()
        if self.gcode == 0:
            self.code_win = tk.Toplevel(self)
            code_win = self.code_win
            code_win.title('Standard genetic code')
            code_win.resizable(0,0)
            code_label = tk.Label(code_win)
            code_label.image = tk.PhotoImage(file = './dna_code.png')
            code_label['image'] = code_label.image
            self.gcode = 1
            code_label.pack()
            code_win.protocol("WM_DELETE_WINDOW", lambda: gcode_minus(self))
        else:
            gcode_minus(self)


    def createMenu(self):

        top_menubar = self.menu
        file_menu = tk.Menu(master = top_menubar, tearoff=0)
        file_menu.add_command(label = 'Read fasta file', command = lambda: self.browse_fasta())
        file_menu.add_separator()
        file_menu.add_command(label = 'Exit', command = self.master.quit)

        top_menubar.add_cascade(label = 'File', menu = file_menu)
        top_menubar.add_command(label = 'Tools', command = lambda: self.call_code())



    def createDNA(self):
        dna_frame = self.dna_frame
        generator = tk.Frame(dna_frame)
        generator_button, generator_entry, generator_label = [
            tk.Button(generator, text = 'generate', command = lambda: self.dna_treater(generator_entry)),
            tk.Entry(generator,width=10),
            tk.Label(generator, text = 'length of the chain:')
         ]
        generator_entry.insert(0, '100')
        generator_button.pack(side = 'left')
        generator_entry.pack(side = 'right')
        generator_label.pack(side = 'right')
        generator.pack(fill= 'x')

        oseq = tk.Frame(dna_frame)
        oseq_label = tk.Label(oseq,text = 'Original DNA sequence')
        self.oseq_text = tk.Text(oseq, height = text_height)
        self.oseq_text.bind("<Button-1>", lambda e: "break")
        self.oseq_text.bind("<Key>", lambda e: "break")
        oseq_label.pack(side = 'top')
        self.oseq_text.pack(side = 'top', pady = common_pady)
        oseq.pack(fill = 'x')

    def createDNAderivatives(self):
        dna_derivatives_frame = self.dna_derivatives_frame

        dseq_frame = tk.Frame(dna_derivatives_frame)
        dseq_label = tk.Label(dseq_frame,text = 'Sequence DNA:')
        dseq_button_complementary = tk.Checkbutton(dseq_frame,text = 'Complementary', onvalue= 1, variable = self.dseq_var, command= lambda: self.dna_derivatives_treater())
        dseq_button_reverse = tk.Checkbutton(dseq_frame,text = 'Reverse', onvalue= 2, variable=self.dseq_var, command= lambda: self.dna_derivatives_treater())
        self.dseq_text = tk.Text(dna_derivatives_frame, height=text_height)
        self.dseq_text.bind("<Button-1>", lambda e: "break")
        self.dseq_text.bind("<Key>", lambda e: "break")
        dseq_label.pack(side = 'left')
        dseq_button_reverse.pack(side = 'right')
        dseq_button_complementary.pack(side = 'right')
        dseq_frame.pack(fill = 'x')
        self.dseq_text.pack(fill = 'x', pady= common_pady)


    # functional part
    #TODO: adapt code under fasta function
    def dna_treater(self, entry):
        try:
            dna_list = random.choices(dna_dictionary, k = int(entry.get()))  
            self.initial_chain =  ''.join(dna_list)
            self.oseq_text.delete('1.0', tk.END)
            self.oseq_text.insert('1.0', self.initial_chain)
            self.dna_derivatives_treater()
        except:
            self.oseq_text.delete('1.0', tk.END)
            self.oseq_text.insert('1.0', 'Wrong generation number given')

    def dna_derivatives_treater(self):
        if self.dseq_var.get() == 0:
            self.dseq_text.delete('1.0', tk.END)
            self.edna = ''
            self.Protein.getProtein()
        elif self.dseq_var.get() == 1:
            self.generate_complementary_dna(self.dseq_text)
        elif self.dseq_var.get() == 2:
            self.generate_reverse_dna(self.dseq_text)

    def browse_fasta(self):
        types = {    'filetypes': (('fasta', '.fasta'),
                              ('fsta', '.fsta'),
                              ('Text files', '.txt'),
                              ('All files', '.*'),)}
        types['title'] = 'Select a file to open...'
        search_window = filedialog.askopenfilename(**types)
        if len(search_window) > 0 :
            self.initial_chain=fasta.fastaReader(search_window)
            self.oseq_text.delete('1.0', tk.END)
            self.oseq_text.insert('1.0', self.initial_chain)
            self.dna_derivatives_treater()

    def generate_complementary_dna(self, text):
        try:
            dna = self.initial_chain
            cdna = ''  
            for i in dna:
                cdna = cdna + dna_complementarity_dictionary[i]
            self.edna = cdna[::-1]
            text.delete('1.0', tk.END)
            text.insert('1.0', self.edna)
            self.Protein.getProtein()
        except:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Initial chain is absent or wrong')

    def generate_reverse_dna(self, text):
        try:
            dna = self.initial_chain
            self.edna = dna[::-1]
            text.delete('1.0', tk.END)
            text.insert('1.0', self.edna)
            self.Protein.getProtein()
        except:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Initial chain is absent or wrong')

class Protein(tk.Frame):
    DNA = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.protein_frame = tk.Frame(master)
        self.rf_var = tk.IntVar(value = 1)
        self.cs_var = tk.IntVar(value = 1)
        self.createProtein()
        self.protein_frame.pack(fill = 'x', padx = common_padx)


    def createProtein(self):
        protein_frame = self.protein_frame
        pset_frame = tk.Frame(protein_frame)
        pseq_label = tk.Label(pset_frame,text = 'Protein\nsequence')
        frames_height, frames_width, frames_padx  = [55, 100, 2]
        pseq_frame1, pseq_frame2 = [
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief='groove'),
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief ='groove')
        ]
        self.pseq_text = tk.Text(protein_frame,height= text_height)
        self.pseq_text.bind("<Button-1>", lambda e: "break")
        self.pseq_text.bind("<Key>", lambda e: "break")
        pseq_label.pack(side = 'left')
        pseq_frame2.pack(side = 'right', padx= frames_padx)
        pseq_frame1.pack(side = 'right', padx= frames_padx)
        rf_label = tk.Label(master = pseq_frame1, text = 'Reading\nframe')
        cs_label = tk.Label(master = pseq_frame2, text = 'AA Code\nLength ')
        rf_label.pack(side = 'left')
        cs_label.pack(side = 'left')
        pset_frame.pack(fill = 'x')
        self.pseq_text.pack(fill = 'x', pady= common_pady)

        # protein, buttons
        pseq_rf2 = tk.Radiobutton(pseq_frame1,text = '2', variable= self.rf_var, value = 2, command = lambda: self.getProtein())
        pseq_rf3 = tk.Radiobutton(pseq_frame1,text = '3', variable= self.rf_var, value = 3, command = lambda: self.getProtein())
        pseq_rf1 = tk.Radiobutton(pseq_frame1,text = '1', variable= self.rf_var, value = 1, command = lambda: self.getProtein())
        pseq_rf1.pack()
        pseq_rf2.pack()
        pseq_rf3.pack()
        pseq_cs1 = tk.Radiobutton(pseq_frame2, text = '1', variable = self.cs_var, value= 1, command = lambda: self.getProtein())
        pseq_cs3 = tk.Radiobutton(pseq_frame2, text = '3', variable = self.cs_var, value= 3, command = lambda: self.getProtein())
        pseq_cs1.pack(pady = 5)
        pseq_cs3.pack(pady = 5)
        pseq_frame1.pack_propagate(0)
        pseq_frame2.pack_propagate(0)


    def getProtein(self):
        frame, code, text = [self.rf_var.get(), self.cs_var.get(), self.pseq_text]
        try:   
            if code == 1:
                code = 1
            else:
                code = 0
            dna = self.DNA.edna[frame-1:]
            protein  = []
            dna = re.findall('...', dna)
            for codon in dna:
                if dna_to_protein_dictionary[codon][0] == '***':
                    break
                protein.append(dna_to_protein_dictionary[codon][code])
            self.protein_chain = ''.join(protein)
            text.delete('1.0', tk.END)
            text.insert('1.0', self.protein_chain)
        except:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Error')

# tests
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('502x315')
    root.resizable(0,0)
    root.title('Genetic code treater')
    DNA_frame = DNA(root)
    Protein_frame = Protein(root)
    Protein_frame.DNA = DNA_frame
    DNA_frame.Protein = Protein_frame
    DNA_frame.pack()
    Protein_frame.pack()
    
    # to check the geometry
    # root.update()
    # print(root.winfo_height())
    # print(root.winfo_width())

    # root.bind_all("<<NewDNA>>", affiche)

    root.mainloop()