import argparse
import emoji
import re
import logging
import time
import json

import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from sklearn.svm import LinearSVC
from lazypredict.Supervised import LazyClassifier
from modaresi.preprocessor import Preprocessor

from process_files import load_data
import utils

# Change the level of the loggers of some of the imported modules
logging.getLogger("matplotlib").setLevel(logging.INFO)


text_re = re.compile(r"[^a-zA-Z\s]")
url_re = re.compile(r"http(s)*://([\w]+)\.(\w|/)*(\b|\s|$)")
quoted_url_re = re.compile(r"http(s)*://([\w]+)\.(\w|/)*(\s|$|\”|\")")
user_re = re.compile(r"@\w\b")
hashtag_re = re.compile(r"[\W]#[\w]*[\W]")
mention_re = re.compile(r"(^|[\W\s])@[\w]*[\W\s]")
mention_re = re.compile(r"(\“|\")[^|\”]*(\“|\")")
smile_re = re.compile(r"(:\)|;\)|:-\)|;-\)|:\(|:-\(|:-o|:o|<3)")
emoji_re = re.compile(r"(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])")
not_ascii_re = re.compile(r"([^\x00-\x7FáéíóúÁÉÍÓÚñÑ]+)")
time_re = re.compile(r"(^|\D)[\d]+:[\d]+")
numbers_re = re.compile(r"(^|\D)[\d]+[.'\d]*\D")
space_collapse_re = re.compile(r"[\s]+")
user_re = re.compile(r"@[\w]*\b")

def preprocess_feed(tweet: str):
    """ takes the original tweet text and returns the preprocessed texts.
    Preprocessing includes:
        - lowercasing
        - replacing hyperlinks with <url>, mentions with <user>, time, numbers, emoticons, emojis
        - removing additional non-ascii special characters
        - collapsing spaces
    """
    t = tweet.lower()
    t = emoji.demojize(t, language='es')
    t = re.sub(url_re, " <URL> ", t)
    t = t.replace("\n", " ")
    t = re.sub(user_re, "@username", t)
    t = re.sub(smile_re, " <EMOTICON> ", t)
    t = re.sub(not_ascii_re, "", t)
    t = re.sub(space_collapse_re, " ", t)
    t = t.strip()
    return t

def load_train_and_test_sets(train_path, test_path = None, test = False):
    samples = load_data(train_path)
    #If there is no test set, split the training set into training and test
    if test_path == None:
        X_train, X_test, y_train, y_test = \
            train_test_split(samples[:,1], samples[:,2:4], train_size=0.7,
                             test_size=0.3, stratify=samples[:,2:4], random_state=42)
    else:
        samples_test = load_data(test_path, test)
        X_train = samples[:,1]
        y_train = samples[:,2:4]
        X_test = samples_test[:,1]
        y_test = samples_test[:,2:4]
    logger.info(np.shape(y_train))
    logger.info(np.shape(y_test))
    return X_train, X_test, y_train[:,0], y_train[:,1], y_test[:,0], y_test[:,1]


def extract_features(posts, docs_test, PARAMS):
    """Extract features

    This function builds a transformer (vectorizer) pipeline,
    fits the transformer to the training set (learns vocabulary and idf),
    transforms the training set and the test set to their TF-IDF matrix representation,
    and builds a classifier.
    """
   # Build a vectorizer that splits strings into sequences of i to j words
    word_vectorizer = TfidfVectorizer(preprocessor=preprocess_feed,
                                      analyzer='word', ngram_range=PARAMS['word_ngram_range'],
                                      min_df=2, use_idf=True, sublinear_tf=True)
    # Build a vectorizer that splits strings into sequences of 3 to 5 characters
    char_vectorizer = TfidfVectorizer(preprocessor=preprocess_feed,
                                     analyzer='char', ngram_range=PARAMS['char_ngram_range'],
                                     min_df=2, use_idf=True, sublinear_tf=True)
    ngrams_vectorizer = Pipeline([('feats', FeatureUnion([('word_ngram', word_vectorizer),
                                                         ('char_ngram', char_vectorizer),
                                                         ])),
                                 # ('clff', LinearSVC(random_state=42))
                                 ])

      # Fit (learn vocabulary and IDF) and transform (transform documents to the TF-IDF matrix) the training set
    X_train_ngrams_tfidf = ngrams_vectorizer.fit_transform(posts)
    '''
    ↳ Check the following attributes of each of the transformers (analyzers)—*word_vectorizer* and *char_vectorizer*:
    vocabulary_ : dict. A mapping of terms to feature indices.
    stop_words_ : set. Terms that were ignored
    '''
    logger.info("@ %.2f seconds: Finished fit_transforming the training dataset", time.process_time())
    logger.info("Training set word & character ngrams .shape = %s", X_train_ngrams_tfidf.shape)

    feature_names_ngrams = [word_vectorizer.vocabulary_, char_vectorizer.vocabulary_]

    # # TEMP: For debugging purposes
    # ProcessDataFiles.write_iterable_to_csv(list(feature_names_ngrams[0].items()), "word_vectorizer.vocabulary_",
    #                                     logger.handlers[1].baseFilename)
    # ProcessDataFiles.write_iterable_to_csv(list(feature_names_ngrams[1].items()), "char_vectorizer.vocabulary_",
    #                                     logger.handlers[1].baseFilename)

    '''
    Extract the features of the test set (transform test documents to the TF-IDF matrix)
    Only transform is called on the transformer (vectorizer), because it has already been fit to the training set.
    '''
    X_test_ngrams_tfidf = ngrams_vectorizer.transform(docs_test)
    logger.info("@ %.2f seconds: Finished transforming the test dataset", time.process_time())
    logger.info("Test set word & character ngrams .shape = %s", X_test_ngrams_tfidf.shape)

    # • Dimensionality reduction using truncated SVD (aka LSA)
    if PARAMS['perform_dimensionality_reduction']:
        # Build a truncated SVD (LSA) transformer object
        svd = TruncatedSVD(n_components=300, random_state=43)
        # Fit the LSI model and perform dimensionality reduction
        X_train_ngrams_tfidf_reduced = svd.fit_transform(X_train_ngrams_tfidf)
        logger.info("@ %.2f seconds: Finished dimensionality reduction (LSA) on the training dataset", time.process_time())
        X_test_ngrams_tfidf_reduced = svd.transform(X_test_ngrams_tfidf)
        logger.info("@ %.2f seconds: Finished dimensionality reduction (LSA) on the test dataset", time.process_time())

        X_train = X_train_ngrams_tfidf_reduced
        X_test = X_test_ngrams_tfidf_reduced
    else:
        X_train = X_train_ngrams_tfidf
        X_test = X_test_ngrams_tfidf

    return X_train, X_test, feature_names_ngrams

def cross_validate_model(gender_clf, age_clf, X_train, y_train_gender, y_train_age):
    """Evaluates the classification model by k-fold cross-validation.

    The model is trained and tested k times, and all the scores are reported.
    """

    # Build a stratified k-fold cross-validator object
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    '''
    Evaluate the score by cross-validation
    This fits the classification model on the training data, according to the cross-validator
    and reports the scores.
    Alternative: sklearn.model_selection.cross_validate
    '''
    scores_gender = cross_val_score(gender_clf.pipeline, X_train, y_train_gender, scoring='accuracy', cv=skf)
    scores_age = cross_val_score(age_clf.pipeline, X_train, y_train_age, scoring='accuracy', cv=skf)

    logger.info("@ %.2f seconds: Cross-validation finished", time.process_time())

    # Log the cross-validation scores, the mean score and the 95% confidence interval, according to:
    # http://scikit-learn.org/stable/modules/cross_validation.html#computing-cross-validated-metrics
    # https://en.wikipedia.org/wiki/Standard_error#Assumptions_and_usage
    logger.info("Gender Scores = %s", scores_gender)
    logger.info("%%Gender Accuracy: %0.2f (±%0.2f)" % (scores_gender.mean()*100, scores_gender.std()*100))
    logger.info("Age Scores = %s", scores_age)
    logger.info("%%Age Accuracy: %0.2f (±%0.2f)" % (scores_age.mean()*100, scores_age.std()*100))
    # ↳ https://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html


def train_and_test_model(clf, X_train, y_train, X_test, y_test, output= "Gender"):
    """Train the classifier and test it.

    This function trains the classifier on the training set,
    predicts the classes on the test set using the trained model,
    and evaluates the accuracy of the model by comparing it to the truth of the test set.
    """
    logger.info("%s classifier", output)
    
    clf.fit(X_train, y_train)
    y_predicted = clf.predict(X_test)

    logger.info("@ %.2f seconds: Finished training the model and predicting class labels for the test set",
                time.process_time())
    # Simple evaluation using numpy.mean
    logger.info("np.mean %%Accuracy: %f", np.mean(y_predicted == y_test) * 100)

    # Log the classification report
    logger.info("Classification report:\n%s", metrics.classification_report(y_test, y_predicted))

    # Log the confusion matrix
    confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)
    logger.info("Confusion matrix:\n%s", confusion_matrix)

    # # Plot the confusion matrix
    # plt.matshow(confusion_matrix)
    # plt.set_cmap('jet')
    # plt.show()
def find_best_model(X_train, y_train_gender, y_train_age):
    pass
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Path to the training set')
    parser.add_argument('-t', '--test', help='Path to the test set')
    parser.add_argument('-o', '--output', default='models', help='Path to the test set')

    
    TRAINING_PATH = "../../modaresi16/magic/corpora/2016/Training"
    TEST_PATH = "../../modaresi16/magic/corpora/2015/junto"
    PARAMS = {
        'word_ngram_range' : (1,3),
        'char_ngram_range' : (3,5),
        'perform_dimensionality_reduction' : True
    }
    logger.info("Training on: %s", TRAINING_PATH)
    logger.info("Testing on %s", TEST_PATH if TEST_PATH!=None else TRAINING_PATH)
    logger.info("Params used: %s", json.dumps(PARAMS))

    docs_train, docs_test, y_train_gender, y_train_age, y_test_gender, y_test_age = load_train_and_test_sets(TRAINING_PATH, TEST_PATH)
    # X_train, X_test, feature_names_ngrams = extract_features(docs_train, docs_test, PARAMS)
    # g_preprocess = Preprocessor('age')
    # X_train = g_preprocess.fit_transform(docs_train)
    # X_test = g_preprocess.transform(docs_test)

    # gender_clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
    # age_clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
    
    # models_gender, _ = gender_clf.fit(X_train, X_test, y_train_gender, y_test_gender)
    # models_age, _ = age_clf.fit(X_train, X_test, y_train_age, y_test_age)
    # logger.info(models_gender)
    # logger.info(models_age)
    
    # gender_clf = LogisticRegression(C=1e3,
    #                               tol=0.01,
    #                               multi_class='ovr',
    #                               solver='liblinear',
    #                               n_jobs=1,
    #                               random_state=123)
    # age_clf = LogisticRegression(C=1e3,
    #                               tol=0.01,
    #                               multi_class='ovr',
    #                               solver='liblinear',
    #                               n_jobs=1,
    #                               random_state=123)
    gender_pipe = Preprocessor(y_train_gender, 'gender')
    age_pipe = Preprocessor(y_train_age, 'age')

    cross_validate_model(gender_pipe, age_pipe, docs_train, y_train_gender, y_train_age)
    train_and_test_model(gender_pipe.pipeline, docs_train, y_train_gender, docs_test, y_test_gender, "Gender")
    train_and_test_model(age_pipe.pipeline, docs_train, y_train_age, docs_test, y_test_age, "Age")
    
if __name__ == "__main__":
    logger = utils.configure_root_logger()
    main()