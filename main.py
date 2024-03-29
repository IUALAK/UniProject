import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext as st
import random
import re
from src.settings import *
import src.fastareader as fasta

class DNA(tk.Frame):
    '''
    Class includes all methods and attributes responsible for visualization and treatment of DNA and its derivatives. Also it responses menu elements
    '''
    # Attributes

    gcode = 0
    Protein = None
    edna = None
    initial_chain = None
    # GUI part

    def __init__(self, master = None):
        '''
        Gets master, creates GUI elements and call functions responsible for their setting
        '''
        tk.Frame.__init__(self, master)
        self.master = master
        self.menu = tk.Menu(master)
        self.createMenu()
        self.dna_frame = tk.Frame(master)
        self.createDNA()
        self.dna_derivatives_frame = tk.Frame(master)
        self.cseq_var = tk.IntVar()
        self.rseq_var = tk.IntVar()
        self.createDNAderivatives()
        master.config(menu = self.menu)
        self.dna_frame.pack(fill = "x", padx = common_padx)
        self.dna_derivatives_frame.pack(fill = 'x', padx = common_padx)

    def call_code(self):
        '''
        Creates and controls window containing table of codons
        '''
        def gcode_minus(self):
            self.gcode = 0
            self.code_win.destroy()
        if self.gcode == 0:
            self.code_win = tk.Toplevel(self)
            code_win = self.code_win
            code_win.title('Standard genetic code')
            code_win.resizable(0,0)
            code_label = tk.Label(code_win)
            code_label.image = tk.PhotoImage(file = './src/dna_code.png')
            code_label['image'] = code_label.image
            self.gcode = 1
            code_label.pack()
            code_win.protocol("WM_DELETE_WINDOW", lambda: gcode_minus(self))
        else:
            gcode_minus(self)


    def createMenu(self):
        '''
        Sets up the GUI elements of top menu
        '''
        top_menubar = self.menu
        file_menu = tk.Menu(master = top_menubar, tearoff=0)
        file_menu.add_command(label = 'Read fasta file', command = lambda: self.browse_fasta())
        file_menu.add_separator()
        file_menu.add_command(label = 'Exit', command = self.master.quit)

        top_menubar.add_cascade(label = 'File', menu = file_menu)
        top_menubar.add_command(label = 'Tools', command = lambda: self.call_code())



    def createDNA(self):
        '''
        Creates and controls GUI elements for initial DNA chain
        '''
        dna_frame = self.dna_frame
        generator = tk.Frame(dna_frame)
        oseq_counter = tk.Frame(generator)
        generator_button, generator_entry, generator_label = [
            tk.Button(generator, text = 'generate', command = lambda: self.dna_treater(generator_entry)),
            tk.Entry(generator,width=10),
            tk.Label(generator, text = 'length of the chain:')
         ]

        generator_entry.insert(0, '100')
        generator_button.pack(side = 'left')
        generator_label.pack(side = 'left')
        generator_entry.pack(side = 'left')
        oseq_counter.pack(side = 'right')
        generator.pack(fill= 'x')
        self.nuc_counter = tk.Label(oseq_counter, text = 'A: 0     T: 0     \n\nC: 0     G: 0     ')
        self.nuc_counter.pack()
 
        # creating counter


        oseq = tk.Frame(dna_frame)
        oseq_label = tk.Label(oseq,text = 'Original DNA sequence')
        self.oseq_text = st.ScrolledText(oseq, height = text_height)
        self.oseq_text.bind("<Button-1>", lambda e: "break")
        self.oseq_text.bind("<Key>", lambda e: "break")
        oseq_label.pack(side = 'top')
        self.oseq_text.pack(side = 'top', pady = common_pady)
        oseq.pack(fill = 'x')


    def countNucleotides(self):
        '''
        Counts the quantity of each nucleotide in initial DNA chain
        '''
        pass
        nuc_table = []
        for i in ('A', 'T', 'C', 'G'):
            text = str(self.oseq_text.get("0.0",tk.END).count(i)) + '   '
            if len(text) > 6:
                text = text[:3] + '...'
            else:
                text = text + ' '*(6-len(text))
            nuc_table.append(text)

        self.nuc_counter.config(text = f'A: {nuc_table[0]} T: {nuc_table[1]}\n\nC: {nuc_table[2]} G: {nuc_table[3]}')
        



    def createDNAderivatives(self):
        '''
        Creates and controls GUI elements for initial chain's derivatives
        '''
        dna_derivatives_frame = self.dna_derivatives_frame

        dseq_frame = tk.Frame(dna_derivatives_frame)
        dseq_label = tk.Label(dseq_frame,text = 'Sequence DNA:')
        dseq_button_complementary = tk.Checkbutton(dseq_frame,text = 'Complementary', onvalue = 1, variable = self.cseq_var, command= lambda: self.dna_derivatives_treater())
        dseq_button_reverse = tk.Checkbutton(dseq_frame,text = 'Reverse', onvalue = 1, variable=self.rseq_var, command= lambda: self.dna_derivatives_treater())
        self.dseq_text = st.ScrolledText(dna_derivatives_frame, height=text_height)
        self.dseq_text.bind("<Button-1>", lambda e: "break")
        self.dseq_text.bind("<Key>", lambda e: "break")
        dseq_label.pack(side = 'left')
        dseq_button_reverse.pack(side = 'right')
        dseq_button_complementary.pack(side = 'right')
        dseq_frame.pack(fill = 'x')
        self.dseq_text.pack(fill = 'x', pady= common_pady)


    # functional part

    def dna_treater(self, entry):
        '''
        Generates DNA initial chain and calls function responsible for generation of derivatives
        '''
        try:
            dna_list = random.choices(dna_dictionary, k = int(entry.get()))  
            self.initial_chain =  ''.join(dna_list)
            self.oseq_text.delete('1.0', tk.END)
            self.oseq_text.insert('1.0', self.initial_chain)
            self.countNucleotides()
            self.dna_derivatives_treater()
        except:
            self.initial_chain = ''
            self.oseq_text.delete('1.0', tk.END)
            self.oseq_text.insert('1.0', 'Wrong generation number given')
            self.countNucleotides()
            self.dna_derivatives_treater()

    def dna_derivatives_treater(self):
        '''
        Controls which derivative will be generated and shown
        '''
        if self.cseq_var.get() == 1:
            self.generate_complementary_dna()
        elif self.rseq_var.get() == 1:
            self.generate_reverse_dna()
        else:
            self.dseq_text.delete('1.0', tk.END)
            self.edna = ''
            self.Protein.getProtein()

    def browse_fasta(self):
        '''
        Permits to browse files in order to find a fasta file
        '''
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
            self.countNucleotides()
            self.dna_derivatives_treater()

    def generate_complementary_dna(self):
        '''
        Generates and shows complementary derivative of initial DNA chain
        '''
        try:
            if self.rseq_var.get() == 0:
                dna = self.initial_chain
            else:
                dna = self.initial_chain[::-1]
            cdna = ''  
            for i in dna:
                cdna = cdna + dna_complementarity_dictionary[i]
            self.edna = cdna
            self.dseq_text.delete('1.0', tk.END)
            self.dseq_text.insert('1.0', self.edna)
            self.Protein.getProtein()
        except:
            self.dseq_text.delete('1.0', tk.END)
            self.dseq_text.insert('1.0', 'Initial chain is absent or wrong')
            self.Protein.getProtein()

    def generate_reverse_dna(self):
        '''
        Generates and shows reverse derivative of initial DNA chain
        '''
        try:
            dna = self.initial_chain
            self.edna = dna[::-1]
            self.dseq_text.delete('1.0', tk.END)
            self.dseq_text.insert('1.0', self.edna)
            self.Protein.getProtein()
        except:
            self.dseq_text.delete('1.0', tk.END)
            self.dseq_text.insert('1.0', 'Initial chain is absent or wrong')
            self.Protein.getProtein()

class Protein(tk.Frame):
    '''
    Class includes all methods and arguments needed to visualize and treat protein sequence within an application
    '''
    DNA = None

    # GUI part

    def __init__(self, master):
        '''
        Gets master, creates GUI elements and call functions responsible for their setting
        '''        
        tk.Frame.__init__(self, master)
        self.master = master
        self.protein_frame = tk.Frame(master)
        self.rf_var = tk.IntVar(value = 1)
        self.cs_var = tk.IntVar(value = 1)
        self.createProtein()
        self.protein_frame.pack(fill = 'x', padx = common_padx)


    def createProtein(self):
        '''
        Generates GUI elements for protein
        '''
        protein_frame = self.protein_frame
        pset_frame = tk.Frame(protein_frame)
        pseq_label = tk.Label(pset_frame,text = 'Protein\nsequence')
        frames_height, frames_width, frames_padx  = [55, 100, 2]
        pseq_frame1, pseq_frame2 = [
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief='groove'),
            tk.Frame(master = pset_frame, height = frames_height, width = frames_width, bd = 2, relief ='groove')
        ]
        self.pseq_text = st.ScrolledText(protein_frame,height= text_height)
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

        # Buttons
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

    # functional part

    def getProtein(self):
        '''
        Generates a sequence of amino acids respecting the derivative DNA chain of given DNA class instance
        '''
        frame, code, text = [self.rf_var.get(), self.cs_var.get(), self.pseq_text]
        if self.DNA.initial_chain == None:
            text.delete('1.0', tk.END)
            text.insert('1.0', 'Error')
            return 
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


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('585x327')
    root.resizable(0,0)
    root.title('Genetic code treater')
    DNA_frame = DNA(root)
    Protein_frame = Protein(root)
    Protein_frame.DNA = DNA_frame
    DNA_frame.Protein = Protein_frame
    DNA_frame.pack()
    Protein_frame.pack()
    
    # to check the geometry if needed
    # root.update()
    # print(root.winfo_height())
    # print(root.winfo_width())

    root.mainloop()