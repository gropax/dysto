from collections import defaultdict


def read_conll(stream):
    """Parse a .conll file into a list of sentences"""
    sent = []
    for i, l in enumerate(stream):
        line = l.strip()
        if line:
            fx = line.split('\t')
            word = fx[2], fx[4]
            sent.append(word)
        elif sent:
            yield sent
            sent = []
    if sent: yield sent

def read_stopwords(stream):
    """Parse a stopwords stream and return a set of words"""
    return set(stream.read().strip().split('\n'))

def sanitize_sentence(sent, words=[], tags=[]):
    """Remove all items in `sent` which word is in `words` or tag is in `tags`"""
    return [(w, t) for w, t in sent if not (w in words or t in tags)]

def sanitize_corpus(corpus, words=[], tags=[]):
    for s in corpus:
        yield sanitize_sentence(s, words, tags)

def limit_tokens(corpus, limit, logger=None):
    """Reduce the size of the corpus under a given number tokens."""
    if logger:
        psize = int(limit / 20)
        ptot = psize

    n = 0
    for s in corpus:
        nn = n
        for w, t in s:
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
    """Takes a corpus of sentences and reduce it to smaller corpus whose
    vocabulary size does not exceed the given vocabulary limit."""
    i = 0
    for s in corpus:
        new_vocab = []
        for w, t in s:
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
    triples = []
    for i in range(0, len(sent)):
        w = sent[i]
        neighbours = sent[max(0,i-span):i] + sent[i+1:min(i+span+1,len(sent))]
        triples += [(w, n) for n in neighbours]
    return triples

def bag_of_words_contexts(corpus, span=4):
    for sent in corpus:
        for context in sentence_bag_of_words_contexts(sent, span):
            if backup:
                backup.write(dump_bag_of_words_context(context))

            yield context

def sentence_positional_contexts(sent, span=4):
    triples = []
    for i in range(0, len(sent)):
        w = sent[i]
        before = [(sent[x], x-i) for x in range(max(0,i-span),i)]
        after = [(sent[x], x-i) for x in range(i+1,min(i+span+1,len(sent)))]
        contexts = before + after
        triples += [(w, n) for n in contexts]
    return triples

def positional_contexts(corpus, span=4, backup=None):
    for sent in corpus:
        for context in sentence_positional_contexts(sent, span):
            if backup:
                backup.write(dump_positional_context(context))

            yield context

def filter_by_tag(contexts, allowed):
    for c in contexts:
        if c[0][1] in allowed:
            yield c



def compute_context_vectors(contexts, tags={}, context_min=1):
    """Compute vector representation for lemmas from the given list of contexts.
    Only return vectors for the `lemma_nb` most frequent lemmas if given, and only
    consider contexts which have been observed at least `context_min` times
    (default 1)."""

    # Compute vector representations
    vectors = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    freq = defaultdict(lambda: defaultdict(int))
    keep_tags = tags.keys()

    for (w, t), c in contexts:
        if t in keep_tags:
            vectors[t][w][c] += 1
            freq[t][w] += 1

    out = {}
    for t, n in tags.items():
        # Select the n most frequent lemmas
        freq_lemmas = sorted(freq[t].items(), key=lambda t: t[1], reverse=True)[0:n]
        lemmas = [l for l, f in freq_lemmas]

        # Cut off rare lemmas and contexts that are not significant
        tag_vectors = defaultdict(dict)
        for w, cx in vectors[t].items():
            if w in lemmas:
                #v = {}
                #for c, f in cx.items():
                    #if f >= context_min:
                        #v[c] = f
                v = {c: f for c, f in cx.items() if f >= context_min}
                if v:
                    tag_vectors[w] = v

        out[t] = tag_vectors

    return out


def dump_bag_of_words_context(context):
    (w1, t1), (w2, t2) = context
    return "\t".join([w1, t1, w2, t2]) + "\n"

def dump_positional_context(context):
    (w1, t1), ((w2, t2), p) = context
    return "\t".join([w1, t1, w2, t2, str(p)]) + "\n"

#def cosine_similarity(vectors):
    #simil = {}
    #words = list(vectors.keys())
    #for i in range(1, len(words)):
        #for j in range(0, i):
            #w1, w2 = words[i], words[j]
            #v1, v2 = vectors[w1], vectors[w2]
            #simil[(w1, w2)] = cosine(v1, v2)
    #return simil

#def cosine(v1, v2):
    #return scalar_product(v1, v2) / norm(v1) / norm(v2)

#def norm(v):
    #return sum(x**2 for x in v.values()) ** 0.5

#def scalar_product(v1, v2):
    #return sum(v1[k] * v2[k] for k in v1 if k in v2)

#def dump_thesaurus(stream, simil):
    #simil = sorted(simil.items(), key=lambda t: t[1], reverse=True)
    #for pair, score in simil:
        #if score > 0:
            #stream.write("\t".join("_".join(s for s in i) for i in pair) + "\t%f\n" % score)

#def lemmatize_contexts(contexts, lemmatizer, tagmap={}):
    #for (w, t), (w2, t2) in contexts:
        #l = lemmatizer.lemmatize(w, tagmap.get(t, t))
        #if l:
            #l2 = lemmatizer.lemmatize(w2, tagmap.get(t2, t2))
            #if l2:
                #yield ((l, t), (l2, t2))

#def lemmatize_corpus(corpus, lemmatizer):
    #for s in corpus:
        #news = lemmatize_sentence(s, lemmatizer)
        #if news:
            #yield news

#def lemmatize_sentence(sentence, lemmatizer):
    #news = []
    #for w, t in sentence:
        #l = lemmatizer.lemmatize(w, t)
        #if l:
            #news.append((l, t))
        #else:
            #return None
    #return news

def tf_idf(vectors):
    pass

def tf(vectors):
    pass

def idf(vectors):
    pass




def bag_of_word_contexts(sents):
    pass

def neighbours_contexts(sents):
    pass

def dependency_contexts(trees):
    pass
