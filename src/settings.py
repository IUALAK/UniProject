# GUI Settings
common_padx = 3
text_height = 5
common_pady = 3

# Internal dictionaries
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
