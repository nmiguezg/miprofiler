#!/usr/bin/env python

import pickle
from random import seed

from magic.profilers.cross_genre_profiler import CrossGenrePerofiler
from magic.benchmarks.sklearn_benchmark import SklearnBenchmark
from magic.datasets.pan_utils import load_xml_dataset
from magic.utils.utils import get_classifier

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# @app.route('/profile', methods=['POST'])
# def profile():
    
#     data = flask.request.data
    
#     return 

if __name__ == '__main__':
    
    clf_gender = None
    clf_age = None
    TRAINING = False
    
    if TRAINING:
        X, y = load_xml_dataset('magic/corpora/2016/Training')
        X_train = [x['text'] for x in X]
        y_train_gender = [yy['gender'] for yy in y]
        y_train_age = [yy['age'] for yy in y]
        
        X, y = load_xml_dataset('magic/corpora/2016/Test')
        X_test = [x['text'] for x in X]
        y_test_gender = [yy['gender'] for yy in y]
        y_test_age = [yy['age'] for yy in y]
        
        with open('pickle/processed-data.pickle', 'wb') as f:
            pickle.dump((X_train, y_train_gender, y_train_age), f)
            
        clf_gender = get_classifier()
        clf_age = get_classifier()
    else:
        with open('pickle/processed-data.pickle', 'rb') as f:
            X_train, y_train_gender, y_train_age = pickle.load(f)
        with open('pickle/gender-model.pickle', 'rb') as f:
            clf_gender = pickle.load(f)
        with open('pickle/age-model.pickle', 'rb') as f:
            clf_age = pickle.load(f)
                
    gender_features = ['unigram', 'bigram', 'char']
    age_features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
    gender_profiler = CrossGenrePerofiler(lang='es', method='logistic_regression', features=gender_features)
    age_profiler = CrossGenrePerofiler(lang='es', method='logistic_regression', features=age_features)


    
    X_train_gender = gender_profiler.fit_transform(X_train, y_train_gender)
    X_train_age = age_profiler.fit_transform(X_train, y_train_age)
    X_test_gender = gender_profiler.transform(X_test)
    X_test_age = age_profiler.transform(X_test)

    
    seed(21)
    
    benchmark = SklearnBenchmark()
    benchmark.run(X_train=X_train_age, y_train=y_train_age,
                  X_test=X_test_age, y_test=y_test_age,
                  profiler=clf_age)