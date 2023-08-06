import pickle
import pandas as pd
from magic.profilers.cross_genre_profiler import CrossGenrePerofiler

class Modaresi_profiler():
    def __init__(self):
        with open('pickle/processed-data.pickle', 'rb') as f:
            X_train, y_train_gender, y_train_age = pickle.load(f)
        with open('pickle/gender-model.pickle', 'rb') as f:
            self.clf_gender = pickle.load(f).set_params(n_jobs=1)
        with open('pickle/age-model.pickle', 'rb') as f:
            self.clf_age = pickle.load(f).set_params(n_jobs=1)
        with open('pickle/gender-pipeline.pickle', 'rb') as f:
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

    def process_csv(self, coll_csv):
        df = pd.read_csv(coll_csv, encoding='utf-8')
        df['post'] = df['post'].transform(lambda x: str(x))
        df.groupby(['label'])['post'].apply('\n'.join).reset_index()
        df.drop_duplicates(subset='label').reset_index(drop=True)
        return df['label'], df['post']