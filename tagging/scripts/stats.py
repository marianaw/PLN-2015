"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt

from corpus.ancora import SimpleAncoraCorpusReader
from collections import Counter, defaultdict


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('../../../ancora/ancora-2.0/')
    
    sents = list(corpus.tagged_sents())
    tagged = [item for sublist in sents for item in sublist]
    # compute the statistics
    words = []
    tags = []
    num_sent = 0
    for tagged_sent in sents:
        num_sent += len(tagged_sent)
        if len(tagged_sent) > 0:
            w, t = zip(*tagged_sent)
            words.extend(list(w))
            tags.extend(list(t))
    vocabulary = set(words)
    voc_size = len(vocabulary)
    tag_vocabulary = set(tags)
    tag_voc_size = len(tags)
    word_counts = Counter(words)
    tag_counts = Counter(tags)
    
    basics = {'Cantidad de oraciones: ': num_sent,
              'Cantidad de ocurrencias de palabras: ': len(words),
              'Cantidad de palabras: ': voc_size,
              'Cantidad de tags: ': len(tag_vocabulary)}
    
    print('Estadísticas básicas:')
    print('----------------------\n')
    for key, value in basics.items():
        print(key, value)
    
    #Etiquetas más frecuentes:
    print('\nEtiquetas más frecuentes:\n\n')
    tags_frecuentes = tag_counts.most_common(10)
    print('|Tag\t|Frecuencia\t|Porcentaje|')
    print('|-----:------------:----------|')
    for k,v in tags_frecuentes:
        print('|', k, '| ', v, '\t|', float(v/tag_voc_size) * 100, '|')

    #Palabras más frecuentes para cada etiqueta frencuente:
    print('\nPalabras más frecuentes:\n\n')
    print('|Tag\t|(Palabra, cantidad)|')
    print('|-----:-------------------|')
    #import ipdb; ipdb.set_trace()
    for tag in tags_frecuentes:
        aux = Counter([x[0] for x in tagged if x[1] == tag[0]])
        print('|', tag[0], '| ', aux.most_common(5), '|')
    
    #Ambigüedad:
    num_words = defaultdict(int)
    tag_words = defaultdict(list)
    counts = Counter(tagged)
    for k, v in counts.items():
        tag_words[k[0]].append(k[1])
        num_words[k[0]] += v
    
    w_tag_num = []
    for k in tag_words.keys():
        w_tag_num.append((k, tag_words[k], num_words[k]))
    w_tag_num = sorted(w_tag_num, key=lambda x: (len(x[1]), x[2]), reverse=True)
    
    print('\nAmbigüedad:\n\n')
    print('-------------------')
    print('|Palabra\t| Nivel de ambigüedad\t| Frecuencia|')
    print('|---------:----------------------:-----------|')
    level = 10
    for word, tags, f in w_tag_num:
        curr_level = len(tags)
        if curr_level != level:
            print('|', word, '\t|', curr_level, '\t\t|', f, '|')
        level = curr_level
    
    print('\n\n')
    print('|Nivel de ambigüedad\t|Cantidad de palabras\t|Porcentaje del corpus|')
    print('|---------------------:----------------------:---------------------|')
    for i in range(1, 10):
        cantidad_palabras = len([tup for tup in w_tag_num if len(tup[1]) == i])
        porcentaje = float(cantidad_palabras/voc_size)*100
        print('|', i, '\t\t|', cantidad_palabras, '\t\t|', porcentaje, '|')
    
    #Palabras más frecuentes para cada etiqueta frencuente:
    
    #print('sents: {}'.format(len(sents)))
