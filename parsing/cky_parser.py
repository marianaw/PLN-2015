from collections import defaultdict
from nltk.tree import Tree


class CKYParser:
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        nested_dict = lambda: defaultdict(dict)
        parent_prob = defaultdict(nested_dict)

        for prod in grammar.productions():
            key = tuple(str(t) for t in prod.rhs())
            parent_prob[key][prod.lhs().symbol()] = prod.logprob()
        self.parent_prob = parent_prob
        self._pi = defaultdict(nested_dict)
        self._bp = defaultdict(nested_dict)
        self.start = grammar.start().symbol()

    def parse(self, sent):
        """Parse a sequence of terminals.
 
        sent -- the sequence of terminals.
        """
        n = len(sent)
        pp = self.parent_prob
        pi = self._pi
        bp = self._bp

        for i in range(1, n + 1):
            w = sent[i-1]
            parents = pp[(w,)]
            if len(parents) > 0:
                max_parent = max(parents.items(), key=lambda x: x[1])
                s = max_parent[0]
                pi[(i, i)][s] = max_parent[1]
                bp[(i, i)][s] = Tree(s, [w])

        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i + l
                if pi[(i,j)]:
                    pass
                if bp[(i,j)]:
                    pass
                for s in range(i, j):
                    left_pi = pi[(i, s)]
                    right_pi = pi[(s + 1, j)]
                    for parent_left, left_prob in left_pi.items():
                        for parent_right, right_prob in right_pi.items():
                            prob = left_prob + right_prob
                            rule = (parent_left, parent_right)
                            p_dict = pp[rule]
                            for grand_parent, grand_prob in p_dict.items():
                                prob = prob + grand_prob
                                if len(pi[(i,j)]) == 0:
                                    pi[(i,j)][grand_parent] = float('-inf') #Para la primera vez.
                                if prob > pi[(i,j)][grand_parent]: #FIXME: ¡Para la primera vez dará un type error!
                                    pi[(i,j)][grand_parent] = prob
                                    bp[(i,j)][grand_parent] = Tree(grand_parent,
                                                                    [bp[(i, s)][parent_left],
                                                                    bp[s+1, j][parent_right]])
        self._pi = pi
        self._bp = bp
        try:
            return pi[(1, n)][self.start], bp[(1, n)][self.start]
        except KeyError:
            return float('-inf'), Tree(' ', [])
