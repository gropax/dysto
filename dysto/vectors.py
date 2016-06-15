from dysto.functional import *
from dysto.thesaurus import Thesaurus


class Vectors(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.words = list(vectors.keys())
        self._norms = {}

    def distributional_thesaurus(self, sim='cosine'):
        simil, score = {}, self.score_proc(sim)
        for i in range(1, len(self.words)):
            for j in range(0, i):
                w1, w2 = self.words[i], self.words[j]
                simil[(w1, w2)] = score(w1, w2)
        return Thesaurus(simil)

    def score_proc(self, string):
        if string == 'cosine':
            return self.cosine

    def cosine(self, w1, w2):
        return self.scalar_product(w1, w2) / self.norm(w1) / self.norm(w2)

    def norm(self, w):
        if not w in self._norms:
            self._norms[w] = sum(x**2 for x in self.vectors[w].values()) ** 0.5
        return self._norms[w]

    def scalar_product(self, w1, w2):
        v1, v2 = self.vectors[w1], self.vectors[w2]
        return sum(v1[k] * v2[k] for k in v1 if k in v2)
