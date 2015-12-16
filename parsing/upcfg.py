from nltk.tree import Tree
from nltk.grammar import Nonterminal as N, ProbabilisticProduction, Production, PCFG
from collections import Counter
from parsing.cky_parser import CKYParser
from parsing.util import lexicalize

class UPCFG:
    """Unlexicalized PCFG.
    """
 
    def __init__(self, parsed_sents, start='sentence', horzMarkov=None):
        """
        parsed_sents -- list of training trees.
        """
        counts_prods = []
        counts_lefts = []
        start_symbol = parsed_sents[0].label()
        self.start_symbol = start_symbol
        for sent in parsed_sents:
            copy_sent = sent
            #if horzMarkov is not None:
            copy_sent.chomsky_normal_form(horzMarkov=horzMarkov)
            prods = copy_sent.productions()
            for prod in prods:
                r = prod.rhs()
                if len(r) == 1:
                    counts_prods.append(Production(prod.lhs(),
                                                   [prod.lhs().symbol()]))
                else:
                    counts_prods.append(prod)
                counts_lefts.append(prod.lhs().symbol())

        counts_lefts = Counter(counts_lefts)
        counts_prods = Counter(counts_prods)
        
        prods = []
        for prod, count in counts_prods.items():
            left = prod.lhs().symbol()
            right = prod.rhs()
            p = float(counts_prods[prod])/counts_lefts[left]
            if len(right) == 2:
                rl = right[0].symbol()
                rr = right[1].symbol()
                prods.append(ProbabilisticProduction(N(left),
                                                     [N(rl), N(rr)],
                                                     prob=p))
            else:
                prods.append(ProbabilisticProduction(N(left),
                                                     [left],
                                                     prob=p))
        self.prods = prods
        pcfg = PCFG(N(start_symbol), prods)
        self.parser = CKYParser(pcfg)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        w, t = zip(*tagged_sent)
        #import ipdb; ipdb.set_trace()
        _, tree = self.parser.parse(list(t))
        if len(tree) == 0:
            return Tree(self.start_symbol, [Tree(tag, [word]) for word, tag in tagged_sent])#FIXME: dejar tag como string.
        else:
            return lexicalize(tree, w)
