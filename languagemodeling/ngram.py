# coding=utf-8
# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random
from functools import reduce
from sklearn.cross_validation import train_test_split


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
        vocab = set()
        for sent in sents:
            sent = start_phrase + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
            vocab = vocab.union(set(sent))
        self.voc_size = len(vocab) - 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return (float(self.counts[tuple(tokens)])/
                self.counts[tuple(prev_tokens)])

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
        p = 0
        start_phrase = [self.start_symbol] * (self.n - 1)
        sent = start_phrase + sent + ['</s>']
        try:
            for i in range(len(sent) - self.n + 1):
                ngram = tuple(sent[i:i+self.n])
                token = ngram[len(ngram)-1]
                prev_tokens = ngram[:len(ngram)-1]
                p += log(self.cond_prob(token, prev_tokens), 2)
        except ValueError:
            return float('-inf')
        return p
    
    def log_prob(self, text):
        p = 0
        m = 0
        for sent in text:
            p += self.sent_log_prob(sent)
            m += len(sent)
        return p/float(m + len(text))
        
    def entropy(self, sents):
        """
        Computes entropy of the sentences.

        sent -- the sentence which entropy is to be calculated.
        """
        p = self.log_prob(sents)
        return -p

    def perplexity(self, sents):
        """
        Computes perplexity of a text.

        sents -- the text which perplexity is to be calculated.
        """
        return pow(2.0, self.entropy(sents))


def merge_dicts(d, sd):
    '''
    Merges two dicts of dicts if they have the same key.

    Parameters:
        @param d1: a dictionary with another dictionary as value.
        @param d2: same as above.

    Returns:
        A new merged dict.
    '''
    skey = list(sd.keys())[0]
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
        #import ipdb; ipdb.set_trace()
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


class AddOneNGram(NGram):

    def V(self):
        return self.voc_size

    def cond_prob(self, token, prev_tokens=None):
        if prev_tokens is None:
            prev_tokens = tuple()
        else:
            prev_tokens = tuple(prev_tokens)
        #import ipdb; ipdb.set_trace()
        num = float(self.count(prev_tokens + (token,))+1)
        den = float(self.count(prev_tokens)) + self.V()
        return num/den


class InterpolatedNGram(NGram):
 
    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        if gamma is None:
            train, ho = train_test_split(sents, train_size=0.9) #NOTE: al usar train_test_split a veces pasa el test held_out, ¡¡¡y a veces no!!!
            self.gamma = self.compute_gamma(ho)
        else:
            train = sents
            self.gamma = gamma
        self.start_symbol = '<s>'
        start_phrase = [self.start_symbol] * (self.n - 1)
        self.counts = counts = defaultdict(int)
        self.addone = addone
        vocab = set()
        #import ipdb; ipdb.set_trace()
        for sent in train:
            sent = start_phrase + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                for j in range(n+1):
                    counts[ngram[0:j]] += 1
            vocab = vocab.union(set(sent))
        self.voc_size = len(vocab) - 1
        counts[('</s>',)] = len(train)
                    
    #def V(self):
        #vocabulary = set()
        #for key in self.counts.keys():
            #vocabulary = vocabulary.union(set(key))
        #return len(vocabulary.difference({self.start_symbol}))
    
    def l(self, i, ngram, current_sum):
        if i == self.n:
            return 1-current_sum
        else:
            return (1 - current_sum) * self.count(ngram)/(self.count(ngram) + self.gamma)
    
    def compute_gamma(self, ho):
        gammas = [1.0, 5.0, 10.0, 50.0, 100.0]
        candidates = []
        train, test = train_test_split(ho, train_size=0.9)
        if len(train) == 0 or len(test) == 0:
            return gammas[0] #FIXME: ¡Consultar esto!
        for g in gammas:
            ng = InterpolatedNGram(self.n, train, g, False)
            candidates.append(ng.perplexity(test))
        return max(candidates)
    
    def cond_prob(self, token, prev_tokens=None): #FIXME: usar addone para evitar las divisiones por cero, ¿está bien esto?
        p = 0
        #import ipdb;ipdb.set_trace()
        current_sum = 0
        if prev_tokens is None:
            prev_tokens = tuple()
        prev_tokens = tuple(prev_tokens)
        for i in range(self.n):
            lambda_i = self.l(i+1, prev_tokens[i:], current_sum)
            current_sum += lambda_i
            #import ipdb; ipdb.set_trace()
            numerator = self.count(prev_tokens[i:]+(token,))
            denominator = self.count(prev_tokens[i:])
            if self.addone and len(prev_tokens[i:]) == 0:
                numerator = numerator + 1.0
                denominator += self.voc_size
            
            if lambda_i != 0:
                p += lambda_i * (numerator/denominator)
        return p
    

class BackOffNGram(NGram):
 
    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.
 
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.addone = addone
        self.denominator = {}
        if beta is None:
            train, ho = train_test_split(sents, train_size=0.9)
            self.beta = self.compute_beta(ho)
        else:
            train = sents
            self.beta = beta
        self.start_symbol = '<s>'
        start_phrase = [self.start_symbol] * (self.n - 1)
        self.counts = counts = defaultdict(int)
        vocab = set()
        for sent in train:
            sent = start_phrase + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                for j in range(n+1):
                    counts[ngram[0:j]] += 1
            vocab = vocab.union(set(sent))
        self.voc_size = len(vocab) - 1
        counts[('</s>',)] = len(train)    
        self.lala = {}
        self.jisd = {}
 
    """
       Todos los métodos de NGram.
    """
    
    def compute_beta(self, ho):
        #import ipdb; ipdb.set_trace()
        betas = [0.1, 0.2, 0.4, 0.5]
        candidates = []
        train, test = train_test_split(ho, train_size=0.9)
        if len(train) == 0 or len(test) == 0:
            return betas[0] #FIXME: ¡Consultar esto!
        for beta in betas:
            ng = BackOffNGram(self.n, train, beta, self.addone)
            candidates.append(ng.perplexity(test))
        return max(candidates)

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        if tokens in self.lala.keys():
            return self.lala[tokens]
        else:
            s = set()
            m = len(tokens)
            for item in self.counts.keys():
                if len(item) == m + 1:
                    if item[0:m] == tokens:
                        s = s.union({item[m]})
            self.lala[tokens] = s
            return s
 
    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        if tokens in self.jisd.keys():
            return self.jisd[tokens]
        else:
            s = sum([self.count(tokens + (item,)) - self.beta for item in self.A(tokens)])
            if s == 0:
                return 1
            result = 1 - s/float(self.count(tokens))
            self.jisd[tokens] = result
            return result

    #def V(self):
        #vocabulary = set()
        #for key in self.counts.keys():
            #vocabulary = vocabulary.union(set(key))
        #return len(vocabulary.difference({self.start_symbol}))

    def cond_prob(self, token, prev_tokens=None):
        if prev_tokens is None:
            prev_tokens = tuple()
        prev_tokens = tuple(prev_tokens)
        gram = prev_tokens + (token,)
        numerator = self.count(gram)
        denominator = self.count(prev_tokens)
        if len(gram) == 1:
            if self.addone:
                numerator += 1
                denominator += self.voc_size
            return numerator/denominator
        if token in self.A(prev_tokens):
            return float(numerator - self.beta)/denominator
        else:
            alpha = self.alpha(prev_tokens)
            if alpha == 0:
                return 0
            else:
                d = self.denom(prev_tokens)
                if len(prev_tokens) > 0 and d > 0:
                    prob = alpha * (self.cond_prob(token, prev_tokens[1:])/d)
                    return prob

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        
        s = 1
        #import ipdb; ipdb.set_trace()
        if tokens in self.denominator.keys():
            return self.denominator[tokens]
        else:
            for w in self.A(tokens):
                s -= self.cond_prob(w, tokens[1:])
            self.denominator[tokens] = s
            return s
    
#if __name__ == '__main__':
    #from sklearn.cross_validation import train_test_split
    #sents = ['la gata come pescado .'.split(), 'el gato come salmón .'.split(), 'el canario come semillas .'.split()]
    #train, test = train_test_split(sents, train_size=0.9)
    #ng = BackOffNGram(3, train, beta=0.4)
    #c = ng.cond_prob('lala')
    #print(c)