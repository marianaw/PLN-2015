#from functools import reduce
from collections import Counter, defaultdict


#def merge(d, sd):
    #skey= list(sd.keys())[0]
    #dk = d.keys()
    #for key in dk:
        #if key == skey:
            #d1 = d[key]
            #d2 = sd[skey]
            #d2_key = list(d2.keys())[0]
            #d1k = d1.keys()
            #for d1_key in d1k:
                #if d2_key == d1_key:
                    #d1.update({d1_key: d1[d1_key] + d2[d2_key]})
                    #d.update({key: d1})
                    #return d
            #d1.update(d2)
            #d.update({key:d1})
            #return d
    #d.update(sd)
    #return d

        #tagged = []
        #for t in tagged_sents:
            #tagged += t
        #l = list(map(lambda x: {x[0]: { x[1]: 1}}, tagged))
        #self.tag_counts = reduce(merge, l)
        #aux = list(self.tag_counts.values())
        #counts = {}
        #for item in aux:
            #for key in item:
                #if key in counts.keys():
                    #vale = counts[key]
                    #counts.update({key: vale + item[key]})
                #else:
                    #counts.update(item)
        #li = sorted(counts.items(), key=lambda x:x[1], reverse=True)
        #self.default_tag = li[0][0]

class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        tagged = []
        for sent in tagged_sents:
            tagged.extend(sent)
        words, tags = zip(*tagged)
        c = Counter(tags)
        self.default_tag = c.most_common(1)[0][0]
        words = set(words)
        self.words = words
        
        counts = Counter(tagged)
        nested_dict = lambda: defaultdict(int)
        word_tags_count = defaultdict(nested_dict)
        for wt, freq in counts.items():
            word_tags_count[wt[0]][wt[1]] = freq
        word_tags = {}
        for word in word_tags_count:
            m = max(word_tags_count[word].items(), key=lambda x: x[1])[0]
            word_tags[word] = m
                
        #for w in words:
            #aux = [x for x in counts.items() if x[0][0] == w]
            #aux = sorted(aux, key=lambda x: x[1], reverse=True)
            #tag = aux[0][0][1]
            #word_tags[w] = tag
        self.word_tags = word_tags

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
            return self.word_tags[w]
        else:
            return self.default_tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return not w in self.words

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