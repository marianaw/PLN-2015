from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from features import *
from featureforge.vectorizer import Vectorizer
from collections import defaultdict


class WordCluster:
    def __init__(self, num_clusters, sents):
        '''
        Parameters:
            @param num_clusters: number of clusters.
            @param sents: the sentences.
        '''
        #import ipdb; ipdb.set_trace()
        self.num_clusters = num_clusters
        histories = self.sents_histories(sents)
        features = [word_islower, word_istitle, word_isdigit,
                    word_isupper, word_vowels, word_punctuation]
        prevword_features = []
        for feature in features:
            prevword_features.append(PrevWord(feature))
        nextword_features = []
        for feature in features:
            nextword_features.append(NextWord(feature))
        features.extend(nextword_features + prevword_features)
        features_vector = Vectorizer(features)
        cl = KMeans(n_clusters=num_clusters)
        self.pipeline = Pipeline([('vectorizer', features_vector),
                                  ('cluster', cl)])
        self.pipeline.fit_transform(histories)
        self.clusters = self.pipeline.named_steps['cluster']
        words = [word for s in sents for word in s]
        self.words_per_cluster = sorted(list(zip(self.clusters.labels_, words)),
                                        key=lambda x: x[0])
        

    def sents_histories(self, sents):
        """
        Iterator over the histories of a corpus.

        Parameters:
            @param sents: the corpus (as a list of sentences)
        """
        histories = []
        for sent in sents:
            if len(sent) > 0:
                histories.extend(self.sent_histories(sent))
        return histories

    def sent_histories(self, sent):
        """
        Iterator over the histories of a sentence.

        Parameters:
            @param sent: the sentence (a list of words).
        """
        histories = []
        for i in range(len(sent)):
            histories.append(History(sent, i))
        return histories

    def cluster_history(self, h):
        '''
        Clusters a history:
        
        Parameters:
            @param h: the history.
        '''
        return self.pipeline.predict([h])[0]

    def cluster(self, sent):
        """
        Cluster the words of a sentence.

        Parameters:
            @param sent: the sentence.
        """
        clusters = []
        for i in range(len(sent)):
            h = History(sent, i)
            clus = self.cluster_history(h)
            clusters.append(clus)
        return list(zip(clusters, sent))

    #def cluster_words(self, num_terms=10):
        #'''
        #Computes a dictionary with the num_terms most important terms
        #for each cluster.

        #Parameters:
            #@param num_terms: the number of terms per cluster we want
            #to compute.

        #Returns:
            #A dictionary indexed by cluster number with the terms.
        #'''
        #d = defaultdict(list)
        #order_centroids = self.clusters.cluster_centers_.argsort()[:, ::-1]
        #for i in range(self.num_clusters):
            #for ind in order_centroids[i, :num_terms]:
                #d[i].append(self.terms[ind])
        #return d
