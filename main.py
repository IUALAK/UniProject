from itertools import chain
from Bio import SeqIO
import tkinter as tk
import random
import re

dna_dictionary = ['A', 'T', 'G', 'C']
dna_complementarity_dictionary = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
dna_to_protein_dictionary = {
    'TTT' : ('Phe', 'F'), 'TTC' : ('Phe', 'F'), 'TTA' : ('Leu', 'L'), 'TTG': ('Leu', 'L'),
    'TCT' : ('Ser', 'S'), 'TCC' : ('Ser', 'S'), 'TCA' : ('Ser', 'S'), 'TCG': ('Ser', 'S'),
    'TAT' : ('Tyr', 'Y'), 'TAC' : ('Tyr', 'Y'), 'TAA' : ('***', '*'), 'TAG': ('***', '*'),
    'TGT' : ('Cys', 'C'), 'TGC' : ('Cys', 'C'), 'TGA' : ('***', '*'), 'TGG': ('Trp', 'W'),
    'CTT' : ('Leu', 'L'), 'CTC' : ('Leu', 'L'), 'CTA' : ('Leu', 'L'), 'CTG': ('Leu', 'L'),
    'CCT' : ('Pro', 'P'), 'CCC' : ('Pro', 'P'), 'CCA' : ('Pro', 'P'), 'CCG': ('Pro', 'P'),
    'CAT' : ('His', 'H'), 'CAC' : ('His', 'H'), 'CAA' : ('Gln', 'Q'), 'CAG': ('Gln', 'Q'),
    'CGT' : ('Arg', 'R'), 'CGC' : ('Arg', 'R'), 'CGA' : ('Arg', 'R'), 'CGG': ('Arg', 'R'),
    'ATT' : ('Ile', 'I'), 'ATC' : ('Ile', 'I'), 'ATA' : ('Ile', 'I'), 'ATG': ('Met', 'M'),
    'ACT' : ('Thr', 'T'), 'ACC' : ('Thr', 'T'), 'ACA' : ('Thr', 'T'), 'ACG': ('Thr', 'T'),
    'AAT' : ('Asn', 'N'), 'AAC' : ('Asn', 'N'), 'AAA' : ('Lys', 'K'), 'AAG': ('Lys', 'K'),
    'AGT' : ('Ser', 'S'), 'AGC' : ('Ser', 'S'), 'AGA' : ('Arg', 'R'), 'AGG': ('Arg', 'R'),
    'GTT' : ('Val', 'V'), 'GTC' : ('Val', 'V'), 'GTA' : ('Val', 'V'), 'GTG': ('Val', 'V'),
    'GCT' : ('Ala', 'A'), 'GCC' : ('Ala', 'A'), 'GCA' : ('Ala', 'A'), 'GCG': ('Ala', 'A'),
    'GAT' : ('Asp', 'D'), 'GAC' : ('Asp', 'D'), 'GAA' : ('Glu', 'E'), 'GAG': ('Glu', 'E'),
    'GGT' : ('Gly', 'G'), 'GGC' : ('Gly', 'G'), 'GGA' : ('Gly', 'G'), 'GGG': ('Gly', 'G'),
}

# Idea: Could I realize the combination of graphical and back fnc? So I'll obtain functional modules

class DNA(tk.Frame):
    # realize the cheking on the gui level
    # GUI part
    gcode = 0
    text_height = 5
    padx = 3

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
        self.dna_frame.pack(fill = "x", padx = self.padx)
        self.dna_derivatives_frame.pack(fill = 'x', padx = self.padx)

    def call_code(self):
        def gcode_minus(self):
            self.gcode = 0
            self.code_win.destroy()
        if self.gcode == 0:
            self.code_win = tk.Toplevel(self.master)
            code_win = self.code_win
            code_win.title('Standard genetic code')
            code_win.resizable(0,0)
            code_label = tk.Label(code_win)
            code_label.image = tk.PhotoImage(file = './dna_code.png')
            code_label['image'] = code_label.image
            code_label.pack()
            self.gcode = 1
            code_win.protocol("WM_DELETE_WINDOW", lambda: gcode_minus(self))

    def createMenu(self):

        top_menubar = self.menu
        file_menu = tk.Menu(master = top_menubar, tearoff=0)
        file_menu.add_command(label = 'Read fasta file')
        file_menu.add_separator()
        file_menu.add_command(label = 'Exit', command = self.master.quit)

        top_menubar.add_cascade(label = 'File', menu = file_menu)
        top_menubar.add_command(label = 'Tools', command = lambda: self.call_code())

    def createDNA(self):
        dna_frame = self.dna_frame
        generator = tk.Frame(dna_frame)
        generator_button, generator_entry = [tk.Button(master = generator, text = 'generate', command = lambda: self.dna_treater(generator_entry, oseq_text)),
         tk.Entry(master = generator,width=10)
         ]
        generator_entry.insert(0, '100')
        generator_button.pack(side = 'left')
        generator_entry.pack(side = 'right')
        generator.pack(fill= 'x')

        oseq = tk.Frame(dna_frame)
        oseq_label = tk.Label(oseq,text = 'Original DNA sequence')
        oseq_text = tk.Text(oseq, height = self.text_height)
        oseq_label.pack(side = 'top')
        oseq_text.pack(side = 'top')
        oseq.pack(fill = 'x')

    def createDNAderivatives(self):
        dna_derivatives_frame = self.dna_derivatives_frame

        dseq_frame = tk.Frame(dna_derivatives_frame)
        dseq_label = tk.Label(dseq_frame,text = 'Sequence DNA:')
        dseq_button_complementary = tk.Checkbutton(dseq_frame,text = 'Complementary', onvalue= 1, variable = self.dseq_var, command= lambda: self.dna_derivatives_treater(dseq_text))
        dseq_button_reverse = tk.Checkbutton(dseq_frame,text = 'Reverse', onvalue= 2, variable=self.dseq_var, command= lambda: self.dna_derivatives_treater(dseq_text))
        dseq_text = tk.Text(dna_derivatives_frame, height=self.text_height)
        dseq_label.pack(side = 'left')
        dseq_button_reverse.pack(side = 'right')
        dseq_button_complementary.pack(side = 'right')
        dseq_frame.pack(fill = 'x')
        dseq_text.pack(fill = 'x')


    # functional part
    #TODO: adapt code under fasta function
    def dna_treater(self,  entry, text):
        dna_list = random.choices(dna_dictionary, k = int(entry.get()))  
        self.initial_chain =  ''.join(dna_list)
        # TODO: think about this part of the code, may be it's better to call them then needed?
        text.delete('1.0', tk.END)
        text.insert('1.0', self.initial_chain)

    def dna_derivatives_treater(self, text):
        if self.dseq_var.get() == 0:
            text.delete('1.0', tk.END)
        elif self.dseq_var.get() == 1:
            self.generate_complementary_dna(text)
        elif self.dseq_var.get() == 2:
            self.generate_reverse_dna(text)


    def generate_complementary_dna(self, text):
        try:
            dna = self.initial_chain
            cdna = ''  
            for i in dna:
                cdna = cdna + dna_complementarity_dictionary[i]
            text.delete('1.0', tk.END)
            text.insert('1.0',cdna[::-1])
        except:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Initial chain is absent or wrong')

    def generate_reverse_dna(self, text):
        try:
            dna = self.initial_chain
            rdna = dna[::-1]
            text.delete('1.0', tk.END)
            text.insert('1.0', rdna)
        except:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Initial chain is absent or wrong')

class Protein(tk.Frame):
    padx = 3

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.protein_frame = tk.Frame(master)
        self.rf_var = tk.IntVar(value = 1)
        self.cs_var = tk.IntVar(value = 1)
        self.createProtein()
        self.protein_frame.pack(fill = 'x', padx = self.padx)


    def createProtein(self):
        protein_frame = self.protein_frame
        pset_frame = tk.Frame(protein_frame)
        pseq_label = tk.Label(pset_frame,text = 'Protein\nsequence')
        frames_height, frames_width  = [55, 100]
        pseq_frame1, pseq_frame2 = [
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief='groove'),
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief ='groove')
        ]
        pseq_text = tk.Text(protein_frame,height= 5, width=65)
        pseq_label.pack(side = 'left')
        pseq_frame1.pack(side = 'right')
        pseq_frame2.pack(side = 'right')
        rf_label = tk.Label(master = pseq_frame1, text = 'Reading\nframe')
        cs_label = tk.Label(master = pseq_frame2, text = 'AA Code\nLength ')
        rf_label.pack(side = 'left')
        cs_label.pack(side = 'left')
        pset_frame.pack(fill = 'x')
        pseq_text.pack(fill = 'x')

        # protein, buttons
        pseq_rf1 = tk.Radiobutton(master = pseq_frame1,text = '1', variable= self.rf_var, value = 1)
        pseq_rf2 = tk.Radiobutton(master = pseq_frame1,text = '2', variable= self.rf_var, value = 2)
        pseq_rf3 = tk.Radiobutton(master = pseq_frame1,text = '3', variable= self.rf_var, value = 3)
        pseq_rf1.pack()
        pseq_rf2.pack()
        pseq_rf3.pack()
        pseq_cs1 = tk.Radiobutton(master = pseq_frame2, text = '1', variable = self.cs_var, value= 1)
        pseq_cs3 = tk.Radiobutton(master = pseq_frame2, text = '3', variable = self.cs_var, value= 3)
        pseq_cs1.pack()
        pseq_cs3.pack()
        pseq_frame1.pack_propagate(0)
        pseq_frame2.pack_propagate(0)


    def getProtein(self, dna, frame = 0, code = 3):
        if code == 1:
            code = 0
        else:
            code = 1
        dna = dna[frame:]
        protein  = []
        dna = re.findall('...', dna)
        for codon in dna:
            if dna_to_protein_dictionary[codon][0] == '***':
                break
            protein.append(dna_to_protein_dictionary[codon][code])
        self.protein_chain = ''.join(protein)


# tests
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x297')
    root.resizable(0,0)
    root.title('Genetic code treater')
    DNA_frame = DNA(root)
    Protein_frame = Protein(root)
    DNA_frame.pack()
    Protein_frame.pack()
    
    # to check the geometry
    # root.update()
    # print(root.winfo_height())
    # print(root.winfo_width())

    # root.bind_all("<<NewDNA>>", affiche)

    root.mainloop()