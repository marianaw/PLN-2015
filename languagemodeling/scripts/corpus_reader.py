import re


def sents(text):
    sents = text.split('.')
    for sent in sents:
        yield(re.findall(r'\w+|[^\w\s]', sent))



def corpus(text):
    sents = text.split('.')
    return [re.findall(r'\w+|[^\w\s]', sent) for sent in sents]