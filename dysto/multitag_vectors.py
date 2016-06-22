from dysto.functional import *
from dysto.vectors import Vectors
from dysto.thesaurus import Thesaurus
import os


class MultitagVectors(object):
    def __init__(self, mt_vectors):
        self.vectors = mt_vectors

    def ppmi(self):
        return MultitagVectors({t: Vectors(vx).ppmi() for t, vx in self.vectors.items()})

    def distributional_thesauri(self, sim='cosine', logger=None):
        out = {}
        for t, vx in self.vectors.items():
            logger and logger.log("Computing thesaurus for %s..." % t)
            start = time.clock()

            thes = vx.distributional_thesaurus(sim)

            end = time.clock()
            logger and logger.log("\tElapsed time :  %0.3f s\n\tItem number :  %i" % (end - start, thes.size()))

            out[t] = thes
        return out

    def dump(self, dir):
        for tag, vx in self.vectors.items():
            filename = os.path.join(dir, "vectors_%s" % tag)
            Vectors(vx).dump(open(filename, 'w'))
