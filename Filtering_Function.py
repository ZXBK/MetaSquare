from skbio import DNA
import re
import string
import argparse
from argparse import RawTextHelpFormatter

def parse_seqs(fasta_ifh, fasta_ofh, convg=False, desc=False):
    str1 = 'U'
    str2 = 'T'
    if convg: #convert "U"->"T" and additionally convert ","->"-" ; remove whitespace
        str1 = str1 + '.'
        str2 = str2 + '-'
    trans_rules= str.maketrans(str1, str2, string.whitespace)
    if desc:
        for seq in fasta_ifh:
            seq_str = str(seq)
            seq_str = seq_str.translate(trans_rules)
            new_str = '>' + seq.metadata['id'] + ' ' + \
                      seq.metadata['description'] + '\n' + seq_str + '\n'
            fasta_ofh.write(new_str)
    else:
        for seq in fasta_ifh:
            seq_str = str(seq)
            seq_str = seq_str.translate(trans_rules)
            new_str = '>' + seq.metadata['id'] + '\n' + seq_str + '\n'
            fasta_ofh.write(new_str)

def check_ambigous(seq, n_ambiguous_bases):
    try:
        input_dna = DNA(str(seq)) 
        ambig_in_seq = sum(input_dna.degenerates()) #return number of words other than atcg(DNA)
        if ambig_in_seq >= n_ambiguous_bases:
            return True
        else:
            return False
    except ValueError:
        print('Notice: Input Sequence including wrong characters:\n',seq.metadata['id']+':\n',str(seq))

def check_homopolymer(seq, n_homopolymer_length):
    nhl = n_homopolymer_length - 1 # due to how regex is written
    if nhl < 1:
        raise ValueError("Homopolymer length must be >= 2!")
    else:
        regex_str = "([ACGTURYSWKMBDHVN])\\1{%s,}" % nhl  #[]: one of element; \\1 the one capture in ([]) ;%s: 	Match any whitespace character
        for p in re.finditer(regex_str, str(seq)): #finditer will return an element that can be loop
            if len(p.group()) >= n_homopolymer_length:
                print("Notice: Input include homopolymer greater than {}:\n".format(n_homopolymer_length),
                      seq.metadata['id']+':\n',seq)   
                return True
            else:
                continue
        return False

def filter_seqs(fasta_ifh, fasta_ofh,
                n_homopolymer_length=8,
                n_ambiguous_bases=5):
    for seq in fasta_ifh:
        seq_str = str(seq)
        ambig = check_ambigous(seq, n_ambiguous_bases)
        if ambig == False:
            poly = check_homopolymer(seq, n_homopolymer_length)
            if poly == False: # if we make it here, write seq to file
                seq_str = '>' + seq.metadata['id'] + ' ' + seq.metadata['description'] + '\n' + seq_str + '\n'
                fasta_ofh.write(seq_str)
            else:
               continue
        else:
           continue

