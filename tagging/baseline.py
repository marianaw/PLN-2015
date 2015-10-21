from functools import reduce
from collections import OrderedDict


def merge(d, sd):
    skey= list(sd.keys())[0]
    for key in d.keys():
        if key == skey:
            d1 = d[key]
            d2 = sd[skey]
            d2_key = list(d2.keys())[0]
            for d1_key in d1.keys():
                if d2_key == d1_key:
                    d1.update({d1_key: d1[d1_key] + d2[d2_key]})
                    d.update({key: d1})
                    return d
            d1.update(d2)
            d.update({key:d1})
            return d
    d.update(sd)
    return d



class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        tagged = []
        for t in tagged_sents:
            tagged += t
        l = list(map(lambda x: {x[0]: { x[1]: 1}}, tagged))
        self.tag_counts = reduce(merge, l)
        aux = list(self.tag_counts.values())
        counts = {}
        for item in aux:
            for key in item:
                if key in counts.keys():
                    vale = counts[key]
                    counts.update({key: vale + item[key]})
                else:
                    counts.update(item)
        li = sorted(counts.items(), key=lambda x:x[1], reverse=True)
        self.default_tag = li[0][0]

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        if not self.unknown(w):
            tags = self.tag_counts[w]
            ordered_tags = OrderedDict(tags)
            return max(ordered_tags)
        else:
            return self.default_tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return not w in self.tag_counts.keys()

#if __name__ == '__main__':
    #from functools import reduce
    #t = [('el', ('D', 1)),
    #('gato', ('N', 1)),
    #('come', ('V', 1)),
    #('pescado', ('N', 1)),
    #('.', ('P', 1)),
    #('el', ('V', 1)),
    #('la', ('V', 1)),
    #('el', ('V', 1)),
    #('el', ('V', 1))]

    #d = {}
    #reduce(merge(d), t)
    #print(d)