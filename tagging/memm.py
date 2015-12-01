from featureforge.vectorizer import Vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from tagging.features import *


class MEMM:
 
    def __init__(self, n, tagged_sents): #Acá tengo que crear el pipeline (¡mirar la documentación!). Básicamente: pipeline = [(vector de features, clasificador)]
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        #import ipdb; ipdb.set_trace()
        self.n = n
        w = []
        for tagged_sent in tagged_sents:
            words, tags = zip(*tagged_sent)
            w.extend(list(words))
        self.words = w
        histories = self.sents_histories(tagged_sents)
        #TODO: aplicar cada función feature en las histories que tenemos. v = Vectorizer([some_feature, some_other_feature])
        #feature_vector = Vectorizer([word_lower, word_istitle, word_isdigit, \
                                     #word_isupper, prev_tags, NPrevTags, PrevWord])
        features = [word_lower, word_istitle, word_isdigit, word_isupper, prev_tags]
        prevtags_features = []
        prevword_features = []
        for i in range(n - 1):
            prevtags_features.append(NPrevTags(i+1))
        for feature in features:
            prevword_features.append(PrevWord(feature))
        features.extend(prevtags_features + prevword_features)
        features_vector = Vectorizer(features)
        mnb = MultinomialNB()
        self.pipeline = Pipeline([('vectorizer', features_vector),
                                  ('classifier', mnb)])
        self.pipeline.fit(self.sents_histories(tagged_sents),
                          self.sents_tags(tagged_sents))
 
    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        histories = []
        for tagged_sent in tagged_sents:
            histories.extend(self.sent_histories(tagged_sent))
        return histories

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        bow, tags = zip(*tagged_sent)
        tags = ('<s>',) * (self.n - 1) + tags + ('</s>',)
        histories = []
        for i in range(len(tags) - self.n):
            ngram = tags[i: i + self.n - 1]
            histories.append(History(list(bow), ngram, i))
        return histories
 
    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.
 
        tagged_sents -- the corpus (a list of sentences)
        """
        tags = []
        for tagged_sent in tagged_sents:
            tags.extend(self.sent_tags(tagged_sent))
        return tags

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
 
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        _, tags = zip(*tagged_sent)
        return list(tags)
 
    def tag(self, sent):
        """Tag a sentence.
 
        sent -- the sentence.
        """
        result = []
        tags = ('<s>',) * (self.n - 1)
        for i in range(len(sent)):
            h = History(sent, tags, i)
            new_tag = self.tag_history(h)[0]
            result.append(new_tag)
            tags = tags[1:] + (new_tag,)
        return result
 
    def tag_history(self, h):
        """Tag a history.
 
        h -- the history.
        """
        #tag = self.pipeline.predict(h)   #¡Toma un iterable!
        return self.pipeline.predict([h])
 
    def unknown(self, w):
        """Check if a word is unknown for the model.
 
        w -- the word.
        """
        return w not in self.words

#if __name__ == '__main__':
    #tagged_sents = [
            #list(zip('el gato come pescado .'.split(),
                 #'D N V N P'.split())),
            #list(zip('la gata come salmón .'.split(),
                 #'D N V N P'.split())),
        #]
    #me = MEMM(1, tagged_sents)