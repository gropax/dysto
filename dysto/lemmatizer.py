LEFFF_TAGS = ['v', 'adj', 'nc', 'prep']

class Lemmatizer(object):
    @classmethod
    def parse_lefff(self, stream):
        data = {}

        for line in stream:
            word, cat, lemma = line.strip().split('\t')[0:3]
            if cat in LEFFF_TAGS:
                k = (word, cat)
                if not k in data:
                    data[k] = set()
                data[k].add(lemma)

        return Lemmatizer(data)

    def __init__(self, data):
        self.data = data
        self.report = {'errors': []}

    def lemmatize(self, word, tag):
        key = (word, tag)
        if key in self.data:
            lemmas = list(set(self.data[key]))
            if len(lemmas) == 1:
                return lemmas[0]
            else:
                self.report['errors'].append("Multiple results for `%s_%s`" % (word, tag))
        else:
            self.report['errors'].append("No result for `%s_%s`" % (word, tag))
