"""Generate sentences.

Usage:
  generate.py -n <n> -i <file>
  generate.py -h | --help

Options:
  -n <n>        Order of the model.
  -i <file>     Input model file.
  -h --help     Show this screen.
"""
from docopt import docopt
from pickle import load

#sys.path.append('~/Documents/Materias_de_posgrado/2015/PLN/PLN-2015/languagemodeling/')
from languagemodeling.ngram import *


def generate_sentences(model, n):
    ngen = NGramGenerator(model)
    for i in range(0,n):
        yield(ngen.generate_sent())



if __name__ == '__main__':
    opts = docopt(__doc__)
    
    n = int(opts['-n'])
    with open(opts['-i'], 'rb') as f:
        f.seek(0)
        model = load(f)
    
        sentences = generate_sentences(model, n)
        for sentence in sentences:
            print(' '.join(sentence))
            print('----------*----------')
    