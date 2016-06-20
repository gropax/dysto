from dysto.functional import *
from dysto.vectors import Vectors
from dysto.thesaurus import Thesaurus
import os


class MultitagVectors(object):
    def __init__(self, mt_vectors):
        self.vectors = mt_vectors

    def distributional_thesauri(self, sim='cosine'):
        out = {}
        for t, vx in self.vectors.items():
            out[t] = Vectors(vx).distributional_thesaurus(sim)
        return out

    def dump(self, dir):
        for tag, vx in self.vectors.items():
            filename = os.path.join(dir, "vectors_%s" % tag)
            Vectors(vx).dump(open(filename, 'w'))
