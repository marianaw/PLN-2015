'''
Evaluates a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
'''
from pickle import load
from docopt import docopt

#NOTE: las parsed_sents serán de tipo Tree, y t.pos() devuelve la tagged_sent. 
#NOTE: t.pretty_print() imprime el arbolito.


if __name__ == '__main__':
    