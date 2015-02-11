#!/usr/bin/env python

from psychopy import visual, core, event

import nltk
import nltk.data
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.corpus import brown
from nltk.probability import LidstoneProbDist
from nltk.model.ngram import NgramModel


reader = PlaintextCorpusReader("./nltk_data/corpora/tao/",['tao_te_ching.yaml'])
tao = reader.words()
est = lambda fdist, bins: LidstoneProbDist
lm = NgramModel(3, brown.words(), estimator=est)
lm.generate(10);