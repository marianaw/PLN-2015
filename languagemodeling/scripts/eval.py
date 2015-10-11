# coding=utf-8
"""Evaluates an n-gram model using the test set.

Usage:
  train.py -i <i>
  train.py -h | --help

Options:
  -i <file>     Input model file.
  -h --help     Show this screen.
"""
from pickle import load
from docopt import docopt
from corpus_reader import corpus
from nltk.corpus import gutenberg


def eval_model(test, model):
    print('Entropy:')
    print(model.entropy(test))
    print('Perplexity:')
    print(model.perplexity(test))
    
    

if __name__ == '__main__':
    opts = docopt(__doc__)
    f = open(opts['-i'], 'rb')
    #test = corpus(' '.join(open('../../amapola.txt').readlines()))
    #test = gutenberg.sents('shakespeare-caesar.txt')
    test = [['la', 'ñapi', 'mamá']]
    model = load(f)
    eval_model(test, model)
