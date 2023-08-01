from logging import logger
import utils
from process_files import load_data

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-i', '--input', help='Path to the training set')
    parser.add_argument('-t', '--test', help='Path to the test set')
    # parser.add_argument('-o', '--output', default='models', help='Path to the test set')
    args = parser.parse()
    samples = load_data(args.t, True)
    labels = samples[:,0]
    posts = samples[:,1]
    
    ngrams_vec = utils.get_vectorizer()
    X_test_ngrams_tfidf = ngrams_vec.fit_transform(posts)
    
    gender_clf = utils.get_trained_model('gender')
    age_clf = utils.get_trained_model('age')

    
if __name__ == "__main__":
    logger = utils.configure_root_logger()
    main()