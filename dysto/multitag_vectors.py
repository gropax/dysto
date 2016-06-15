from dysto.functional import *
from dysto.vectors import Vectors
from dysto.thesaurus import Thesaurus


class MultitagVectors(object):
    def __init__(self, mt_vectors):
        self.vectors = mt_vectors

    def distributional_thesauri(self, sim='cosine'):
        out = {}
        for t, vx in self.vectors.items():
            out[t] = Vectors(vx).distributional_thesaurus(sim)
        return out
