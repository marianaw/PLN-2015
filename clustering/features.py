from featureforge.feature import Feature
from collections import namedtuple
from string import punctuation

# sent -- the whole sentence.
# i -- the position to be clustered.
History = namedtuple('History', 'sent i')


def word_islower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return int(sent[i].islower())



def word_istitle(h):
    '''
    Feature: word begins with capital letter.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return int(sent[i][0].isupper() and sent[i][1:].islower())



def word_isdigit(h):
    '''
    Feature: word begins with capital letter.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return int(sent[i].isdigit())



def word_isupper(h):
    '''
    Feature: word is capital.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return int(sent[i].isupper())



def word_vowels(h):
    '''
    Feature: number of vowels on the word.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    num_vowels = sum(sent[i].count(c) for c in list('aeiou'))
    return num_vowels



def word_punctuation(h):
    '''
    Feature: number of vowels on the word.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    num_punc = sum(sent[i].count(c) for c in list(punctuation))
    return num_punc



class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.
 
        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.
 
        h -- the history.
        """
        sent, i = h.sent, h.i
        if i == 0:
            return 0
        prev_h = History(sent, i-1)
        return int(self.f(prev_h))



class NextWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the next word.
 
        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """Apply the feature to the next word in the history.
 
        h -- the history.
        """
        sent, i = h.sent, h.i
        if i >= len(sent) - 1:
            return 0
        prev_h = History(sent, i+1)
        return int(self.f(prev_h))
