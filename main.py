import argparse
from argparse import RawTextHelpFormatter
import Filtering_Function as FilterF
from skbio.io import read

def main():
    parser = argparse.ArgumentParser(
             description= 'This script will re-write FASTA files without the description.\n' 
             'And also convert all Us to Ts and '
             'optionally convert "." to "-".',
             formatter_class=RawTextHelpFormatter)
    req = parser.add_argument_group('REQUIRED')
    req.add_argument('-i', '--input_fasta', required=True, action='store',
                     help='Input fasta file.')
    req.add_argument('-o1', '--output_DNA', required=True, action='store',
                     help='Output DNA fasta.')
    req.add_argument('-o2', '--output_removed_DNA', required=True, action='store',
                    help='Output removed DNA fasta.')
    
    optp = parser.add_argument_group('OPTIONAL')
    optp.add_argument('-d', '--include_description', action='store_true',
                      help='Boolean. Keep the additional FASTA header '
                      'description text. \n[Default: False]')
    optp.add_argument('-g', '--convert_to_gap', action='store_true',
                      help='Boolean. Convert "." to "-". \n[Default: False]')

    optp.add_argument('-p', '--n_homopolymer_length', action='store',
                      type=int, default=8,
                      help='Remove sequences that contain homopolymers of '
                      'greater than or equal to length n. \n'
                      "[Default %(default)s)]")
    optp.add_argument('-a', '--n_ambiguous_bases', action='store',
                      type=int,default=5,
                      help='Remove sequences that contain ambiguous bases greater than or equal '
                      "to length n. \n[Default %(default)s)]")

    p = parser.parse_args()

    input_fasta = read(p.input_fasta, format='fasta')
    output_DNA_fasta = open(p.output_DNA, 'w')
    convert_to_gap = p.convert_to_gap
    include_description = p.include_description
    FilterF.parse_seqs(input_fasta, output_DNA_fasta, convg=convert_to_gap,
                     desc=include_description)
    input_fasta.close()
    output_DNA_fasta.close()


    input_DNA_fasta = read(p.output_DNA, format='fasta')
    output_removed_fasta = open(p.output_removed_DNA, 'w')
    n_homopolymer_length = p.n_homopolymer_length
    n_ambiguous_bases = p.n_ambiguous_bases
    FilterF.filter_seqs(input_DNA_fasta, output_removed_fasta,
                      n_homopolymer_length=n_homopolymer_length,
                      n_ambiguous_bases=n_ambiguous_bases)
    input_DNA_fasta.close()
    output_removed_fasta.close()

if __name__ == "__main__":
    main()
