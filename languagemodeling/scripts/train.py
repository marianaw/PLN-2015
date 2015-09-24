"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file> -m <string>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -m <string>   "ngram" for usual NGrams or "addone" for AddOneNGram. Default: NGram.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = gutenberg.sents('austen-emma.txt')

    # train the model
    n = int(opts['-n'])
    
    try:
        m = opts['-m']
    except KeyError:
        m = 'ngram'
        
    if m == 'ngram':
        model = NGram(n, sents)
    if m == 'addone':
        model = AddOneNGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
