import pickle
from sklearn.externals import joblib
from magic.profilers.cross_genre_profiler import CrossGenrePerofiler
from abc import ABCMeta, abstractmethod

class Generic_profiler():
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def predict(self, X_test):
        pass
    def join_posts(self, users_posts, sep=' '):
        return [sep.join(posts) for posts in users_posts]
    
class Modaresi_profiler(Generic_profiler):
    def __init__(self):
        with open('pickle/modaresi/processed-data.pickle', 'rb') as f:
            X_train, y_train_gender, y_train_age = pickle.load(f)
        with open('pickle/modaresi/gender-model.pickle', 'rb') as f:
            self.clf_gender = pickle.load(f).set_params(n_jobs=1)
        with open('pickle/modaresi/age-model.pickle', 'rb') as f:
            self.clf_age = pickle.load(f).set_params(n_jobs=1)
        with open('pickle/modaresi/gender-pipeline.pickle', 'rb') as f:
            self.gender_profiler = pickle.load(f)
        self.gender_profiler.pipeline.named_steps['features'].set_params(n_jobs=1)
                    
        age_features = ['unigram', 'bigram', 'spelling', 'punctuation', 'char']
        self.age_profiler = CrossGenrePerofiler(lang='es', method='logistic_regression', features=age_features)
        self.age_profiler.train(X_train, y_train_age)
    
    def predict(self, X_test):
        X_test_gender = self.gender_profiler.transform(X_test)
        X_test_age = self.age_profiler.transform(X_test)
        y_pred_gender = self.clf_gender.predict(X_test_gender)
        y_pred_age = self.clf_age.predict(X_test_age)
        return y_pred_gender, y_pred_age
    def join_posts(self, coll_csv, sep="\n"):
        return super(Modaresi_profiler, self).join_posts(coll_csv, sep)
    
class Grivas_profiler(Generic_profiler):
    def __init__(self):
        with open('pickle/grivas/age.joblib', 'rb') as f:
            self.age_model = joblib.load(f)
        with open('pickle/grivas/gender.joblib', 'rb') as f:
            self.gender_model = joblib.load(f)
    def predict(self, X_test):
        y_pred_gender = self.gender_model.predict(X_test)
        y_pred_age = self.age_model.predict(X_test)
        return y_pred_gender, y_pred_age