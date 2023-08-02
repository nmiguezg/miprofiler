#!/usr/bin/env python

from random import seed
from magic.profilers.cross_genre_profiler import CrossGenrePerofiler
from magic.benchmarks.sklearn_benchmark import SklearnBenchmark
from magic.datasets.pan_utils import load_xml_dataset
from process_files import load_data

# from process_files import load_data

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# @app.route('/profile', methods=['POST'])
# def profile():
    
#     data = flask.request.data
    
#     return 

if __name__ == '__main__':
    train_path = "magic/corpora/2016/Training"
    test_path = "magic/corpora/2015/junto"

    samples = load_data(train_path)
    samples_test = load_data(test_path)
    X_train = samples[:,1]
    y_train_gender = samples[:,2]
    y_train_age = samples[:,3]
    X_test = samples_test[:,1]
    y_test_gender = samples_test[:,2]
    y_test_age = samples_test[:,3]
    # X, y = load_xml_dataset('magic/corpora/2016/Training')
    # X_train = [x['text'] for x in X]
    # y_train_gender = [yy['gender'] for yy in y]
    # y_train_age = [yy['age'] for yy in y]
    
    # X, y = load_xml_dataset('magic/corpora/2016/Test')
    # X_test = [x['text'] for x in X]
    # y_test_gender = [yy['gender'] for yy in y]
    # y_test_age = [yy['age'] for yy in y]
    
    # features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
    features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
    profiler_instance = CrossGenrePerofiler(lang='es', method='logistic_regression', features=features)
    seed(21)
    benchmark = SklearnBenchmark()
    benchmark.run(X_train=X_train, y_train=y_train_age,
                  X_test=X_test, y_test=y_test_age,
                  profiler=profiler_instance)