from nose.tools import *
from io import StringIO
from dysto import *  # read_conll, read_stopwords, sanitize_sentence, compute_vocabulary, sentence_bag_of_words_contexts, norm, scalar_product


corpus = """1	Aviator	_	NOUN	PNOUN	_	0	ROOT	_	_
2	,	_	.	.	_	1	p	_	_
3	un	_	DET	DET	_	4	det	_	_
4	film	_	NOUN	NOUN	_	1	appos	_	_
5	sur	_	ADP	ADP	_	4	adpmod	_	_
6	la	_	DET	DET	_	7	det	_	_
7	vie	_	NOUN	NOUN	_	5	adpobj	_	_
8	de	_	ADP	ADP	_	7	adpmod	_	_
9	Hughes	_	NOUN	PNOUN	_	8	adpobj	_	_
10	.	_	.	.	_	1	p	_	_

1	Les	_	DET	DET	_	2	det	_	_
2	études	_	NOUN	NOUN	_	3	nsubj	_	_
3	durent	_	VERB	VERB	_	0	ROOT	_	_
4	six	_	NUM	NUM	_	5	num	_	_
5	ans	_	NOUN	NOUN	_	3	dobj	_	_
6	mais	_	CONJ	CONJ	_	3	cc	_	_
7	leur	_	DET	DET	_	8	poss	_	_
8	contenu	_	NOUN	NOUN	_	9	nsubj	_	_
9	diffère	_	VERB	VERB	_	3	conj	_	_
10	donc	_	ADV	ADV	_	9	advmod	_	_
11	selon	_	ADP	ADP	_	9	adpmod	_	_
12	les	_	DET	DET	_	13	det	_	_
13	Facultés	_	NOUN	PNOUN	_	11	adpobj	_	_
14	.	_	.	.	_	3	p	_	_
"""

expected_corpus = [
    [
        ('Aviator', 'PNOUN'),
        (',', '.'),
        ('un', 'DET'),
        ('film', 'NOUN'),
        ('sur', 'ADP'),
        ('la', 'DET'),
        ('vie', 'NOUN'),
        ('de', 'ADP'),
        ('Hughes', 'PNOUN'),
        ('.', '.'),
    ],
    [
        ('Les', 'DET'),
        ('études', 'NOUN'),
        ('durent', 'VERB'),
        ('six', 'NUM'),
        ('ans', 'NOUN'),
        ('mais', 'CONJ'),
        ('leur', 'DET'),
        ('contenu', 'NOUN'),
        ('diffère', 'VERB'),
        ('donc', 'ADV'),
        ('selon', 'ADP'),
        ('les', 'DET'),
        ('Facultés', 'PNOUN'),
        ('.', '.'),
    ]
]
corpus_stream = StringIO(corpus)

def test_read_conll():
    corpus = read_conll(corpus_stream)
    assert_equal(expected_corpus, list(corpus))


stopwords = """allô
allons
après
assez
"""
stop_stream = StringIO(stopwords)

def test_read_stopwords():
    stop = read_stopwords(stop_stream)
    expected = set(['allô', 'allons', 'après', 'assez'])
    assert_equal(expected, stop)


def test_sanitize_sentence():
    sent = [
        ('Aviator', 'PNOUN'),
        (',', '.'),
        ('un', 'DET'),
        ('film', 'NOUN'),
        ('sur', 'ADP'),
        ('la', 'DET'),
        ('vie', 'NOUN'),
        ('de', 'ADP'),
        ('Hughes', 'PNOUN'),
        ('.', '.'),
    ]
    expected = [
        ('Aviator', 'PNOUN'),
        (',', '.'),
        ('sur', 'ADP'),
        ('de', 'ADP'),
        ('Hughes', 'PNOUN'),
        ('.', '.'),
    ]
    res = sanitize_sentence(sent, ['film', 'vie'], ['DET'])
    assert_equal(expected, res)


def test_compute_vocabulary():
    original_corpus = [
        [
            ('Le', 'DET'),
            ('chat', 'NOUN'),
            ('mange', 'VERB'),
        ],
        [
            ('La', 'DET'),
            ('souris', 'NOUN'),
            ('dort', 'VERB'),
        ],
        [
            ('Le', 'DET'),
            ('chien', 'NOUN'),
            ('court', 'VERB'),
        ],
    ]
    expected_corpus = [
        [
            ('Le', 'DET'),
            ('chat', 'NOUN'),
            ('mange', 'VERB'),
        ],
        [
            ('La', 'DET'),
            ('souris', 'NOUN'),
            ('dort', 'VERB'),
        ],
    ]
    expected_vocab = {
        'Le': 1,
        'chat': 2,
        'mange': 3,
        'La': 4,
        'souris': 5,
        'dort': 6,
    }
    vocab = {}
    corpus = compute_vocabulary(original_corpus, vocab, vocab_limit=7)
    assert_equal(expected_corpus, list(corpus))
    assert_equal(expected_vocab, vocab)


def test_sentence_bag_of_words_contexts():
    sent = [('1', 0), ('2', 0), ('3', 0), ('4', 0), ('5', 0), ('6', 0)]
    expected = [(('1', 0), ('2', 0)), (('1', 0), ('3', 0)),
                (('2', 0), ('1', 0)), (('2', 0), ('3', 0)), (('2', 0), ('4', 0)),
                (('3', 0), ('1', 0)), (('3', 0), ('2', 0)), (('3', 0), ('4', 0)), (('3', 0), ('5', 0)),
                (('4', 0), ('2', 0)), (('4', 0), ('3', 0)), (('4', 0), ('5', 0)), (('4', 0), ('6', 0)),
                (('5', 0), ('3', 0)), (('5', 0), ('4', 0)), (('5', 0), ('6', 0)),
                (('6', 0), ('4', 0)), (('6', 0), ('5', 0))]
    contexts = sentence_bag_of_words_contexts(sent, span=2)
    assert_equal(expected, contexts)


#def test_norm():
    #v = {'a': 3, 'c': 4}
    #assert_equal(5, norm(v))


#def test_scalar_product():
    #v1 = {'a': 3, 'c': 4, 'd': 6}
    #v2 = {'a': 2, 'b': 3, 'd': 2}
    #assert_equal(18, scalar_product(v1, v2))
