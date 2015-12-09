from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()



def word_istitle(h):
    '''
    Feature: word begins with capital letter.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return sent[i][0].isupper() and sent[i][1:].islower()



def word_isdigit(h):
    '''
    Feature: word begins with capital letter.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return sent[i].isdigit()



def word_isupper(h):
    '''
    Feature: word is capital.

    Parameters:
        @param h: the history (namedtuple).
    '''
    sent, i = h.sent, h.i
    return sent[i].isupper()



def prev_tags(h):
    '''
    Feature: the previous tags.
    
    Parameters:
        @param h: the history (namedtuple).
        
    Returns:
        The previous tags.
    '''
    return h.prev_tags



class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.
 
        n -- number of previous tags to consider.
        """
        self.n = n
 
    def _evaluate(self, h):
        """n previous tags tuple.
 
        h -- a history.
        """
        tags = h.prev_tags
        #assert self.n <= len(tags)
        return tags[len(tags) - self.n:]



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
        sent, tags, i = h.sent, h.prev_tags, h.i
        if i == 0:
            return 'BOS'
        prev_h = History(sent, tags, i-1) #FIXME: acá los tags "previos" son los mismos que los de la actual, ¿ta bien esto? Rta.: si (¡revisar definición!)
        return str(self.f(prev_h))
