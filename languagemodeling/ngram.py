# coding=utf-8
# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random
from functools import reduce


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.start_symbol = '<s>'
        start_phrase = [self.start_symbol] * (self.n - 1)
        self.counts = counts = defaultdict(int)

        for sent in sents:
            sent = start_phrase + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)])/self.counts[tuple(prev_tokens)]

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        if tokens in self.counts.keys():
            return self.counts[tokens]
        else:
            return 0

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if prev_tokens is None:
            prev_tokens = tuple()
        else:
            prev_tokens = tuple(prev_tokens)
        return float(self.count(prev_tokens + (token,)))/float(self.count(prev_tokens))

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        p = 1
        start_phrase = [self.start_symbol] * (self.n - 1)
        sent = start_phrase + sent + ['</s>']
        for i in range(len(sent) - self.n + 1):
            ngram = tuple(sent[i:i+self.n])
            token = ngram[len(ngram)-1]
            prev_tokens = ngram[:len(ngram)-1]
            p = p * self.cond_prob(token, prev_tokens)
            if p == 0:
                break
        return p

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        try:
            return log(self.sent_prob(sent), 2)
        except ValueError:
            return float('-inf')


def merge_dicts(d, sd):
    '''
    Merges two dicts of dicts if they have the same key.

    Parameters:
        @param d1: a dictionary with another dictionary as value.
        @param d2: same as above.

    Returns:
        A new merged dict.
    '''
    skey = sd.keys()[0]
    for key in d.keys():
        if skey == key:
            value = d[key]
            svalue = sd[skey]
            value.update(svalue)
            d.update({key: value})
            return d
    d.update(sd)
    return d


class NGramGenerator:
    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = model.n
        self.start_symbol = model.start_symbol
        m = model.counts.keys()
        m = [y for y in m if len(y) >= model.n and y != ('<s>',)]
        l = map(lambda x: {x[:len(x)-1]: {x[len(x)-1]: model.cond_prob(x[len(x)-1], x[:len(x)-1])}}, m)
        self.probs = reduce(merge_dicts, l)
        self.sorted_probs = {}
        for d in self.probs:
            aux = []
            for key in self.probs[d]:
                aux.append((key, self.probs[d][key]))
            aux = sorted(aux, key=lambda x: (-x[1], x[0]))
            self.sorted_probs.update({d: aux})

    def generate_sent(self):
        """Randomly generate a sentence."""
        l = [self.start_symbol] * (self.n - 1)
        s = ''
        while s != '</s>':
            prev = tuple(l[len(l)-(self.n-1):])
            s = self.generate_token(prev)
            l.append(s)
        return l[self.n-1:len(l)-1]

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        u = random()
        if prev_tokens is None:
            prev_tokens = ()
        probs = self.sorted_probs[prev_tokens]
        aux = 0
        for prob in probs:
            aux += prob[1]
            if u < aux:
                return prob[0]

