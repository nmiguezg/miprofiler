from __future__ import unicode_literals
from sklearn import preprocessing
from sklearn.base import BaseEstimator
import numpy as np
import hunspell
from string import printable


def tokenize(x):
    x = str(filter(lambda x: x in printable, x))
    return x.split()

class SpellingError(BaseEstimator):

    def __init__(self):
        self.hunspell = hunspell.HunSpell(
                'modaresi/hunspell/es_ES.dic', 'modaresi/hunspell/es_ES.aff')

    def get_feature_names(self):
        return np.array(['avg_error_count'])

    def fit(self, documents, y=None):
        return self

    def avg_error(self, tokens):
        if len(tokens) == 0:
            return 0.0
        trueSum = 0
        for token in tokens:
            if self.is_correct(token):
                trueSum += 1
        return 1.0 * trueSum / len(tokens)

    def is_correct(self, text):
        return self.hunspell.spell(text)
    
    def transform(self, documents):
        tokens_list = [tokenize(doc) for doc in documents]
        avg_errors = [self.avg_error(tokens) for tokens in tokens_list]
        X = np.array([avg_errors]).T
        if not hasattr(self, 'scalar'):
            self.scalar = preprocessing.StandardScaler().fit(X)
        return self.scalar.transform(X)
