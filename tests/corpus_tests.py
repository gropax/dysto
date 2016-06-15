from nose.tools import *
from io import StringIO
from dysto import Corpus


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
corpus_stream = StringIO(corpus)

def test_corpus():
    corpus = Corpus.from_stream(corpus_stream)
