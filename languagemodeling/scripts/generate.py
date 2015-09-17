from optparse import OptionParser
import sys

sys.path.append('~/Documents/Materias_de_posgrado/2015/PLN/PLN-2015/languagemodeling/')
from languagemodeling.ngram import *


def read_model(f):
    with open(f, 'r') as fl:
        sents = []
        for line in fl:
            sents.append(line.strip('\n').split())
        n = int(sents[0][0])
        sents = sents[1:]
        ng = NGram(n, sents)
        fl.close()
    return ng



def generate_sentences(model, n):
    ngen = NGramGenerator(model)
    for i in range(0,n):
        yield(ngen.generate_sent())



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", dest="filename", help="File containing language model.")
    parser.add_option("-n", dest="sentsnum", help="The number of sentences to be generated.")
    opt, args = parser.parse_args()
    
    n = int(opt.sentsnum)
    f = opt.filename
    model = read_model(f)
    
    sentences = generate_sentences(model, n)
    for sentence in sentences:
        print(sentence)
    