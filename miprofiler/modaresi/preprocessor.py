from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.utils import compute_class_weight
from modaresi.pipelines import avg_spelling_error, char_ngrams, punctuation_features, word_bigrams, word_unigrams
import numpy as np

class Preprocessor(object):
    def __init__(self, y_train, trait = 'gender') -> None:
        if (trait == 'gender'):
            fs = [word_unigrams(),
                  word_bigrams(),
                  avg_spelling_error(),
                  char_ngrams()
                  ]
        else:
            fs = [word_unigrams(),
                word_bigrams(),
                avg_spelling_error(),
                punctuation_features(),
                char_ngrams()
                ]
        fu = FeatureUnion(fs)
        self.pipeline = make_pipeline(fu, 
                                      Normalizer(),
                                      LogisticRegression(C=1e3,
                                                         tol=0.01,
                                                         multi_class='ovr',
                                                         solver='liblinear',
                                                         n_jobs=1,
                                                         random_state=123,
                                                         class_weight = 'balanced'
                                                        #  compute_class_weight(
                                                        #      'balanced',
                                                        #      classes= np.unique(y_train),
                                                        #      y=y_train)
                                                         )
                                      )
    
    def fit_transform(self, x):
        return self.pipeline.fit_transform(x)
    def transform(self, x):
        return self.pipeline.transform(x)
    
    def fit(self, X_train, Y_train):
        self.model = self.pipeline.fit(X_train, Y_train)
    def predict(self, X):
        return self.model.predict(X)
