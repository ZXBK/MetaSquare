#! /usr/bin/env python

from skbio.io import read #scikit-bio==0.5.7 , scikit-learn==1.1.2, scipy==1.8.1
import string
import argparse
from argparse import RawTextHelpFormatter


def make_trans_table(convg=False):
    """Convert U to T and optionally, . to - and remove whitespace."""
    str1 = 'U'
    str2 = 'T'
    if convg:
        str1 = str1 + '.'
        str2 = str2 + '-'
    tt = str.maketrans(str1, str2, string.whitespace) #set rules 
    return tt

def parse_seqs(fasta_ifh, fasta_ofh, convg=False, desc=False):
    tt = make_trans_table(convg=convg) #if convg is true, then set rules
    if desc:
        for seq in fasta_ifh:  #seq is an object from skbio.io  Ex: >seq1 Turkey metadata[id]=seq1 [description]=Turkey
            seq_str = str(seq)
            seq_str = seq_str.translate(tt) #apply rules
            new_str = '>' + seq.metadata['id'] + ' ' + \
                      seq.metadata['description'] + '\n' + seq_str + '\n'
            fasta_ofh.write(new_str)
    else:
        for seq in fasta_ifh:
            seq_str = str(seq)
            seq_str = seq_str.translate(tt)
            new_str = '>' + seq.metadata['id'] + '\n' + seq_str + '\n'
            fasta_ofh.write(new_str)


def main():
    parser = argparse.ArgumentParser(
             description= 'This script will simply re-write FASTA files '
             'without the description. \nWill also convert all Us to Ts and '
             'optionally convert "." to "-".'
             'That is, this: \n'
             '\t>seq1 H. Sapiens\n'
             '\tACCGGUUGGCCGUUCAGGGUACAGGUUGGCCGUUCAGGGUAA\n'
             'will be output as:\n'
             '\t>seq1\n'
             '\tACCGGTTGGCCGTTCAGGGTACAGGTTGGCCGTTCAGGGTAA\n'
             'Expected to be used with SILVA FASTA files.',
             formatter_class=RawTextHelpFormatter)
    req = parser.add_argument_group('REQUIRED')
    req.add_argument('-i', '--input_fasta', required=True, action='store',
                     help='Input fasta file.')
    req.add_argument('-o', '--output_fasta', required=True, action='store',
                     help='Output fasta file.')
    optp = parser.add_argument_group('OPTIONAL')
    optp.add_argument('-d', '--include_description', action='store_true',
                      help='Boolean. Keep the additional FASTA header '
                      'description text.[Default: False]')
    optp.add_argument('-g', '--convert_to_gap', action='store_true',
                      help='Boolean. Convert "." to "-". [Default: False]')

    p = parser.parse_args()

    input_fasta = read(p.input_fasta, format='fasta')
    output_fasta = open(p.output_fasta, 'w')
    convert_to_gap = p.convert_to_gap
    include_description = p.include_description

    parse_seqs(input_fasta, output_fasta, convg=convert_to_gap,
               desc=include_description)

    input_fasta.close()
    output_fasta.close()

if __name__ == '__main__':
    main()
