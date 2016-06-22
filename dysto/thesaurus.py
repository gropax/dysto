from dysto.functional import *


class Thesaurus(object):
    @classmethod
    def from_stream(self, stream):
        return self(read_thesaurus(stream))

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

    def score(self, w1, w2):
        """Retourne le score de similarité des deux mots données. Retourne 0 si
        l'un des mots n'est pas présent dans le thésaurus"""
        if (w1, w2) in self._similarity:
            return self._similarity[(w1, w2)]
        elif (w2, w1) in self._similarity:
            return self._similarity[(w2, w1)]
        else:
            return 0
