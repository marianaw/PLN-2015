from math import log

log2 = lambda x: log(x, 2)

class HMM:
 
    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.tagset = tagset
        self.trans = trans
        self.out = out
        self.n = n
        
 
    def tagset(self):
        """Returns the set of tags.
        """
        return self.tagset
 
    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
 
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if self.n == 1:
            prev_tags = tuple()
        else:
            prev_tags = tuple(prev_tags)
        tags = self.trans[prev_tags]
        if tag in tags.keys():
            return tags[tag]
        return 0.0

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
 
        word -- the word.
        tag -- the tag.
        """
        words_dict = self.out[tag]
        if word in words_dict.keys():
            return words_dict[word]
        return 0.0

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
 
        y -- tagging.
        """
        p = 1.0
        y = ['<s>'] * (self.n-1) + y + ['</s>']
        for i in range(len(y) - self.n + 1):
            ngram = tuple(y[i:i+self.n])
            tag = ngram[len(ngram)-1]
            prev_tags = ngram[:len(ngram)-1]
            p *= self.trans_prob(tag, prev_tags)
            if p == 0:
                return 0
        return p

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
 
        x -- sentence.
        y -- tagging.
        """
        p = 1.0
        for i, word in enumerate(x):
            p *= self.out_prob(word, y[i])
            if p == 0:
                return 0
        return p * self.tag_prob(y)

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
 
        y -- tagging.
        """
        p = 0
        y = ['<s>'] * (self.n-1) + y + ['</s>']
        try:
            for i in range(len(y) - self.n + 1):
                ngram = tuple(y[i:i+self.n])
                tag = ngram[len(ngram)-1]
                prev_tags = ngram[:len(ngram)-1]
                p += log2(self.trans_prob(tag, prev_tags))
        except ValueError:
            p = float('-inf')
        return p

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.
 
        x -- sentence.
        y -- tagging.
        """
        p = 0.0
        try:
            for i, word in enumerate(x):
                p += log2(self.out_prob(word, y[i]))
        except ValueError:
            return float('-inf')
        return p * self.tag_prob(y)

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
 
        sent -- the sentence.
        """
 
 
class ViterbiTagger:
 
    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
 
    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
 
        sent -- the sentence.
        """