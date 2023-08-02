#!/usr/bin/env python
from random import seed
from magic.profilers.cross_genre_profiler import CrossGenrePerofiler
from magic.benchmarks.sklearn_benchmark import SklearnBenchmark
from magic.configuration import Configuration
from magic.datasets.pan import load
import argparse
import logging


def configure(conf):

    @conf.profiler('english-gender-profiler', lang='en', method='logistic_regression', dimension='gender')
    def build_en_gender_profiler(**args):
        features = ['unigram', 'bigram', 'spelling', 'char']
        return CrossGenrePerofiler(lang='en', method='logistic_regression', features=features)

    @conf.profiler('english-age-profiler', lang='en', method='logistic_regression', dimension='age')
    def build_en_age_profiler(**args):
        features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
        return CrossGenrePerofiler(lang='en', method='logistic_regression', features=features)

    @conf.profiler('spanish-gender-profiler', lang='es', method='logistic_regression', dimension='gender')
    def build_es_gender_profiler(**args):
        features = ['unigram', 'bigram', 'char']
        return CrossGenrePerofiler(lang='es', method='logistic_regression', features=features)

    @conf.profiler('spanish-age-profiler', lang='es', method='logistic_regression', dimension='age')
    def build_es_age_profiler(**args):
        features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
        return CrossGenrePerofiler(lang='es', method='logistic_regression', features=features)

    @conf.profiler('dutch-gender-profiler', lang='nl', method='logistic_regression', dimension='gender')
    def build_nl_gender_profiler(**args):
        features = ['unigram', 'bigram', 'spelling', 'char']
        return CrossGenrePerofiler(lang='en', method='logistic_regression', features=features)

    @conf.dataset('pan2014/english/blogs/gender', label='gender', type='blogs', language='english', year='2014')
    @conf.dataset('pan2014/english/blogs/age', label='age_group', type='blogs', language='english', year='2014')
    @conf.dataset('pan2014/english/socialmedia/gender', label='gender', type='socialmedia', language='english', year='2014')
    @conf.dataset('pan2014/english/socialmedia/age', label='age_group', type='socialmedia', language='english', year='2014')
    @conf.dataset('pan2014/english/review/gender', label='gender', type='review', language='english', year='2014')
    @conf.dataset('pan2014/english/review/age', label='age_group', type='review', language='english', year='2014')
    @conf.dataset('pan2014/spanish/blogs/gender', label='gender', type='blogs', language='spanish', year='2014')
    @conf.dataset('pan2014/spanish/blogs/age', label='age_group', type='blogs', language='spanish', year='2014')
    @conf.dataset('pan2014/spanish/socialmedia/gender', label='gender', type='socialmedia', language='spanish', year='2014')
    @conf.dataset('pan2014/spanish/socialmedia/age', label='age_group', type='socialmedia', language='spanish', year='2014')
    def build_dataset_pan14(label=None, type=None, language=None, year=None):
        X, y = load(label=label, type=type, language=language, year=year)
        X = [x['text'] for x in X]
        y = [yy[label]for yy in y]
        return X, y

    @conf.dataset('pan2015/spanish/twitter/gender', label='gender', type='twitter', language='spanish', year='2015')
    @conf.dataset('pan2015/spanish/test/gender', label='gender', type='test', language='spanish', year='2015')
    @conf.dataset('pan2015/spanish/test/age', label='age', type='test', language='spanish', year='2015')
    @conf.dataset('pan2015/spanish/junto/gender', label='gender', type='junto', language='spanish', year='2015')
    @conf.dataset('pan2015/spanish/junto/age', label='age', type='junto', language='spanish', year='2015')
    @conf.dataset('all/spanish/twitter/age', label='age', type='twitter', language='spanish', year='2017')
    @conf.dataset('all/spanish/twitter/gender', label='gender', type='twitter', language='spanish', year='2017')

    @conf.dataset('pan2015/spanish/twitter/age', label='age', type='twitter', language='spanish', year='2015')
    @conf.dataset('pan2016/english/twitter/gender', label='gender', type='twitter', language='english', year='2016')
    @conf.dataset('pan2016/spanish/twitter/gender', label='gender', type='twitter', language='spanish', year='2016')
    @conf.dataset('pan2016/spanish/blogs/gender', label='gender', type='blogs', language='spanish', year='2016')
    @conf.dataset('pan2016/dutch/twitter/gender', label='gender', type='twitter', language='dutch', year='2016')
    @conf.dataset('pan2016/english/twitter/age', label='age', type='twitter', language='english', year='2016')
    @conf.dataset('pan2016/spanish/twitter/age', label='age', type='twitter', language='spanish', year='2016')
    @conf.dataset('pan2016/spanish/blogs/age', label='age', type='blogs', language='spanish', year='2016')

    def build_dataset_pan16(label=None, type=None, language=None, year=None):
        X, y = load(label=label, type=type, language=language, year=year)
        X = [x['text'] for x in X]
        y = [yy[label] for yy in y]
        return X, y


def pretty_list(items):
    return ', '.join([x for x in items])


if __name__ == '__main__':
    conf = Configuration()
    argparser = argparse.ArgumentParser(description='Author Profiling Evaluation')
    argparser.add_argument('-l', '--log-level', dest='log_level', type=str, default='INFO',
                           help='Set log level (DEBUG, INFO, ERROR)')

    argparser.add_argument('-c', '--train_corpus', dest='training_corpus', type=str, required=True,
                           help='Set name of the training corpus used for the evaluation: ' + pretty_list(
                               conf.get_dataset_names()))

    argparser.add_argument('-t', '--test_corpus', dest='test_corpus', type=str, required=False,
                           help='Set name of the test corpus used for the evaluation: ' + pretty_list(
                               conf.get_dataset_names()))

    argparser.add_argument('-p', '--profiler', dest='profiler_name', type=str, required=True,
                           help='Name of the invoked profiler: ' + pretty_list(conf.get_profiler_names()))

    args = argparser.parse_args()
    LOGFMT = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(level=getattr(logging, args.log_level), format=LOGFMT)

    configure(conf)
    X_train, y_train = conf.get_dataset(
        args.training_corpus)
    if args.test_corpus:
        X_test, y_test = conf.get_dataset(args.test_corpus)
    else:
        X_test, y_test = None
    profiler_instance = conf.get_profiler(args.profiler_name)
    seed(21)
    benchmark = SklearnBenchmark()
    benchmark.run(X_train=X_train, y_train=y_train,
                  X_test=X_test, y_test=y_test,
                  profiler=profiler_instance)
