"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
from collections import defaultdict
import pandas as pd

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()



if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('../../../ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total = 0, 0
    unk_hits, total_unk = 0, 0
    n = len(sents)
    nested_dict = lambda: defaultdict(int)
    confusion = defaultdict(nested_dict)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))
        
        #Unknown and known words accuracy:
        words_mod_gold = zip(word_sent, gold_tag_sent, model_tag_sent)
        unk_words = set(word_sent).difference((model.words))
        unk_hits_sent = [g == m for w, g, m in words_mod_gold if w in unk_words]
        unk_hits += sum(unk_hits_sent)
        total_unk += len(unk_words)
        unk_acc = float(unk_hits)/total_unk
        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, unk_acc * 100))
        
        #Confusion matrix as a dictionary:
        mod_gold = zip(gold_tag_sent, model_tag_sent)
        for gt, mt in mod_gold:
            if gt != mt:
                confusion[gt][mt] += 1

    acc = float(hits) / total
    unk_acc = float(unk_hits)/total_unk
    kno_acc = float(hits - unk_hits)/(total - total_unk)
    confusion = pd.DataFrame.from_dict(confusion)
    confusion = confusion.fillna(0)
    
    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy unknown words: {:2.2f}%'.format(unk_acc * 100))
    print('Accuracy known words: {:2.2f}%'.format(kno_acc * 100))
    print('Confusion matrix:')
    print(confusion.ix[:10, :10])