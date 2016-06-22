from dysto.functional import *
from dysto.thesaurus import Thesaurus
import math


class Vectors(object):
    def __init__(self, vectors):
        self.vectors = vectors
        self.words = list(vectors.keys())
        self._norms = {}

    def ppmi(self):
        wp, cp, t = {}, {}, 0
        for w, cx in self.vectors.items():
            if not w in wp:
                wp[w] = 0
            for c, s in cx.items():
                if not c in cp:
                    cp[c] = 0
                wp[w] += s
                cp[c] += s
                t += s

        wp = {w: s / t for w, s in wp.items()}
        cp = {c: s / t for c, s in cp.items()}

        newvx = {}
        for w, cx in self.vectors.items():
            v = {}
            for c, s in cx.items():
                v[c] = max(math.log(s / (wp[w] * cp[c])), 0)
            newvx[w] = v

        return Vectors(newvx)


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

    #def cosine(self, w1, w2):
        #p = self.scalar_product(w1, w2) / self.norm(w1) / self.norm(w2)
        #if p == 1:
            #print("v1 : %s | %s" % (w1, self.vectors[w1]))
            #print("v2 : %s | %s" % (w2, self.vectors[w2]))
            #raise
        #return p

    def norm(self, w):
        if not w in self._norms:
            self._norms[w] = sum(x**2 for x in self.vectors[w].values()) ** 0.5
        return self._norms[w]

    def scalar_product(self, w1, w2):
        v1, v2 = self.vectors[w1], self.vectors[w2]
        return sum(v1[k] * v2[k] for k in v1 if k in v2)

    #def dump(self, stream):
        #for w, v in self.vectors.items():
            #a = [x for w, s in v.items() for x in ["_".join(w), s]]
            #s = w + "\t" + "\t".join([x for y in v.items() for x in y])
            #stream.write(s)
