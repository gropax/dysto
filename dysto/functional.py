import time
from collections import defaultdict


def read_conll(stream):
    """Parser un fichier .conll et yield les phrases une par une"""
    sent = []
    for i, l in enumerate(stream):
        line = l.strip()
        if line:
            fx = line.split('\t')
            word = fx[2], fx[4], int(fx[6]), fx[7]
            sent.append(word)
        elif sent:
            yield sent
            sent = []
    if sent: yield sent

def read_stopwords(stream):
    """Parse une liste de mots et en retourne la liste"""
    return set(stream.read().strip().split('\n'))

def read_relations(stream):
    """Parse un fichier contenant les relation syntaxiques en dépendance à
    considérer pour construire les contextes syntaxiques."""
    return [tuple(s.strip().split('\t')) for s in stream]

def read_thesaurus(stream):
    """Parse un thésaurus sérializé et retourne un objet `Thesaurus`"""
    sim = {}
    for l in stream:
        w1, w2, s = l.strip().split('\t')
        sim[(w1, w2)] = float(s)
    return sim

def sanitize_sentence(sent, words=[], tags=[]):
    """Retire les éléments de la phrase dont le lemme ou le tag fait parties des
    listes d'exclusion données"""
    return [(w, t, h, r) for w, t, h, r in sent if not (w in words or t in tags)]

def sanitize_corpus(corpus, words=[], tags=[]):
    """Nettoye les phrases d'un corpus une à une"""
    for s in corpus:
        yield sanitize_sentence(s, words, tags)

def limit_tokens(corpus, limit, logger=None):
    """Cesse le parsing et le process des phrases une fois le nombre de tokens
    désiré est atteint"""
    if logger:
        psize = int(limit / 20)
        ptot = psize

    n = 0
    for s in corpus:
        nn = n
        for w, t, *_ in s:
            nn += 1

        if logger and n > ptot:
            ptot += psize
            p = 5 * (ptot / psize - 1)
            logger.log("Read Corpus:  %i %%" % p)

        if nn > limit:
            break
        else:
            n = nn
            yield s

    logger.log("Reading finished :  %i tokens" % n)


def compute_vocabulary(corpus, vocab={}, vocab_limit=float('inf')):
    """Cesse le parsing et le process des phrases une fois que le vocabulaire a
    atteint la taille souhaitée"""
    i = 0
    for s in corpus:
        new_vocab = []
        for w, t, *_ in s:
            if not w in vocab:
                i += 1
                new_vocab.append([w, i])
        if i > vocab_limit:
            break
        else:
            for w, i in new_vocab:
                vocab[w] = i
            yield s

def sentence_bag_of_words_contexts(sent, span=4):
    """Retourne la liste des contextes de type bag of words présents dans la
    phrase donnée"""
    triples = []
    for i in range(0, len(sent)):
        w, t, *_ = sent[i]
        neighbours = sent[max(0,i-span):i] + sent[i+1:min(i+span+1,len(sent))]
        triples += [((w, t), (w2, t2)) for w2, t2, *_ in neighbours]
    return triples

def bag_of_words_contexts(corpus, span=4, backup=None):
    """Génère les contextes de types bag of word du corpus un par un"""
    for sent in corpus:
        for context in sentence_bag_of_words_contexts(sent, span):
            if backup:
                backup.write(dump_bag_of_words_context(context))

            yield context

def sentence_positional_contexts(sent, span=4):
    """Retourne la liste des contextes de type linéaire présents dans la
    phrase donnée"""
    triples = []
    for i in range(0, len(sent)):
        w1, t1, *_ = sent[i]
        before = [(sent[x], x-i) for x in range(max(0,i-span),i)]
        after = [(sent[x], x-i) for x in range(i+1,min(i+span+1,len(sent)))]
        contexts = before + after
        triples += [((w1, t1), ((w2, t2), p)) for (w2, t2, *_), p in contexts]
    return triples

def positional_contexts(corpus, span=4, backup=None):
    """Génère les contextes de types linéaire du corpus un par un"""
    for sent in corpus:
        for context in sentence_positional_contexts(sent, span):
            #if backup:
                #backup.write(dump_qualified_context(context))

            yield context

# Retourne la liste les contextes en dépendance de la phrase donnée,
# dont la relation est décrite par le dictionnaire `rels`, au format suivant:
#
#     rels = [
#         ('V', 'obj', 'NC'),
#         ('V', 'obj', 'P', 'obj', 'NC'),
#     ]
#
def sentence_dependency_contexts(sent, rels=[]):
    """Retourne la liste des contextes en dépendance présents dans la phrase
    donnée"""
    triples = []
    for w, t, h, r in sent:
        if h > 0:
            hw, ht, hh, hr = sent[h-1]

            if rels:
                if hh > 0:
                    hhw, hht, *_ = sent[hh-1]
                    if (hht, hr, ht, r, t) in rels:
                        triples.append(((hhw, hht), ((w, t), hw + '_obj')))
                        triples.append(((w, t), ((hhw, hht), hw + '_obj_of')))
                        continue

                if (ht, r, t) in rels:
                    triples.append(((hw, ht), ((w, t), r)))
                    triples.append(((w, t), ((hw, ht), r + '_of')))
            else:
                triples.append(((hw, ht), ((w, t), r)))
                triples.append(((w, t), ((hw, ht), r + '_of')))

    return triples

def dependency_contexts(corpus, relations=[], backup=None):
    """Génère les contextes en dépendance du corpus un par un"""
    for sent in corpus:
        for context in sentence_dependency_contexts(sent, relations):
            if backup:
                backup.write(dump_qualified_context(context))

            yield context


def compute_context_vectors(contexts, tags={}, context_min=1, logger=None):
    """Compute vector representation for lemmas from the given list of contexts.
    Only return vectors for the `lemma_nb` most frequent lemmas if given, and only
    consider contexts which have been observed at least `context_min` times
    (default 1)."""

    # Compute vector representations
    vectors = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    freq = defaultdict(lambda: defaultdict(int))
    keep_tags = tags.keys()

    start = time.clock()

    for (w, t), c in contexts:
        if t in keep_tags:
            vectors[t][w][c] += 1
            freq[t][w] += 1

    end = time.clock()

    if logger:
        logger.log("\tElapsed time : %0.3f s" % (end - start))
        logger.log("Computing vectors...")

    start = time.clock()

    out = {}
    for t, n in tags.items():
        # Select the n most frequent lemmas
        freq_lemmas = sorted(freq[t].items(), key=lambda t: t[1], reverse=True)[0:n]
        lemmas = [l for l, f in freq_lemmas]

        # Cut off rare lemmas and contexts that are not significant
        tag_vectors = defaultdict(dict)
        for w, cx in vectors[t].items():
            if w in lemmas:
                v = {c: f for c, f in cx.items() if f >= context_min}
                if v:
                    tag_vectors[w] = v

        out[t] = tag_vectors

    end = time.clock()

    if logger:
        logger.log("\tElapsed time : %0.3f s" % (end - start))

    return out

def dump_bag_of_words_context(context):
    (w1, t1), (w2, t2) = context
    return "\t".join([w1, t1, w2, t2]) + "\n"

def dump_qualified_context(context):
    (w1, t1), ((w2, t2), p) = context
    return "\t".join([w1, t1, w2, t2, str(p)]) + "\n"
