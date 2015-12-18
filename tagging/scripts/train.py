"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM


models = {
    'base': BaselineTagger,
    'mlhmm': MLHMM,
    'memm': MEMM
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('../../../ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # train the model
    mod_name = opts['-m']
    if mod_name != 'base':
        if not opts['-n']:
            n = 1
        else:
            n = int(opts['-n'])
            model = models[mod_name](n, sents)
    else:
        model = BaselineTagger(sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
