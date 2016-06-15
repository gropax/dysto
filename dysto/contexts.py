from dysto.functional import *
from dysto.multitag_vectors import MultitagVectors


class Contexts(object):
    def __init__(self, gen):
        self._generator = gen

    def __iter__(self):
        return self._generator

    def lemmatize(self, lemmatizer, tagmap={}):
        gen = lemmatize_contexts(self._generator, lemmatizer, tagmap)
        return Contexts(gen)

    def context_vectors(self, tags, context_min=5):
        mt_vectors = compute_context_vectors(self._generator, tags, context_min)
        return MultitagVectors(mt_vectors)
