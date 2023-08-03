import pickle
from random import seed

from magic.profilers.cross_genre_profiler import CrossGenrePerofiler
from magic.benchmarks.sklearn_benchmark import SklearnBenchmark
from magic.datasets.pan_utils import load_xml_dataset
from magic.utils.utils import get_classifier

def train_models():
    X, y = load_xml_dataset('magic/corpora/all')
    X_train = [x['text'] for x in X]
    y_train_gender = [yy['gender'] for yy in y]
    y_train_age = [yy['age'] for yy in y]
    
    with open('pickle/processed-data.pickle', 'wb') as f:
        pickle.dump((X_train, y_train_gender, y_train_age), f)
        
    clf_gender = get_classifier()
    clf_age = get_classifier()
    
    gender_features = ['unigram', 'bigram', 'char']
    gender_profiler = CrossGenrePerofiler(lang='es', method='logistic_regression', features=gender_features)
    gender_profiler.train(X_train, y_train_gender)
    with open('pickle/gender-pipeline.pickle', 'wb') as f:
        pickle.dump(gender_profiler, f)
        
    clf_gender.fit(gender_profiler.transform(X_train), y_train_gender)
    clf_age.fit(age_profiler.transform(X_train), y_train_age)
    with open('pickle/gender-model.pickle', 'wb') as f:
        pickle.dump(clf_gender, f)
    with open('pickle/age-model.pickle', 'wb') as f:
        pickle.dump(clf_age, f)

def test():
    clf_gender = None
    clf_age = None

    X, y = load_xml_dataset('magic/corpora/2016/Test')
    X_test = [x['text'] for x in X]
    y_test_gender = [yy['gender'] for yy in y]
    y_test_age = [yy['age'] for yy in y]
        
    with open('pickle/processed-data.pickle', 'rb') as f:
        X_train, y_train_gender, y_train_age = pickle.load(f)
    with open('pickle/gender-model.pickle', 'rb') as f:
        clf_gender = pickle.load(f)
    with open('pickle/age-model.pickle', 'rb') as f:
        clf_age = pickle.load(f)
    with open('pickle/gender-pipeline.pickle', 'rb') as f:
        gender_profiler = pickle.load(f)
                   
    age_features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
    age_profiler = CrossGenrePerofiler(lang='es', method='logistic_regression', features=age_features)
    age_profiler.train(X_train, y_train_age)
        
    X_test_gender = gender_profiler.transform(X_test)
    X_test_age = age_profiler.transform(X_test)
    benchmark = SklearnBenchmark()
    seed(21)
    benchmark.run(None, y_train_gender, X_test_gender, y_test_gender, clf_gender)
    benchmark.run(None, y_train_age, X_test_age, y_test_age, clf_age)