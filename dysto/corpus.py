from dysto.functional import *
from dysto.contexts import Contexts


class Corpus(object):
    @classmethod
    def from_stream(self, stream):
        return self(read_conll(stream))

    def __init__(self, gen, vocab=None):
        self._generator = gen
        self._vocabulary = vocab

    def __iter__(self):
        return self._generator

    def sanitize(self, words=[], tags=[]):
        gen = sanitize_corpus(self._generator, words, tags)
        return Corpus(gen)

    def limit_tokens(self, limit, logger=False):
        gen = limit_tokens(self._generator, limit=limit, logger=logger)
        return Corpus(gen)

    def limit_vocabulary(self, limit):
        vocab = {}
        gen = compute_vocabulary(self._generator, vocab, vocab_limit=limit)
        return Corpus(gen, vocab=vocab)

    def bag_of_words_contexts(self, span=2, backup=None):
        gen = bag_of_words_contexts(self, span, backup=backup)
        return Contexts(gen)

    def positional_contexts(self, span=2, backup=None):
        gen = positional_contexts(self, span, backup=backup)
        return Contexts(gen)

    def vocabulary(self):
        return self._vocabulary
