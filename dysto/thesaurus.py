from dysto.functional import *


class Thesaurus(object):
    def __init__(self, sim):
        self._similarity = sim
        self._words = self.compute_words(sim)

    def compute_words(self, sim):
        wx = set()
        for t in sim.keys():
            wx.update(t)
        return list(wx)

    def size(self):
        return len(self._words)

    def words(self):
        return self._words

    def dump(self, stream):
        simil = sorted(self._similarity.items(), key=lambda t: t[1], reverse=True)
        for pair, score in simil:
            if score > 0:
                stream.write("\t".join(i for i in pair) + "\t%f\n" % score)
