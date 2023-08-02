from magic.datasets.pan_utils import load_xml_dataset
import os


base_2014_path = 'magic/corpora/2014/Training'
es14_blogs_path = os.path.join(base_2014_path, 'pan14-author-profiling-training-corpus-spanish-blogs-2014-04-16')
es14_socialmedia_path = os.path.join(base_2014_path, 'pan14-author-profiling-training-corpus-spanish-socialmedia-2014-04-16')
es14_twitter_path = os.path.join(base_2014_path, 'pan14-author-profiling-training-corpus-spanish-twitter-2014-04-16')

base_2015_path = 'magic/corpora/2015/'
base_2016_path = 'magic/corpora/2016/'
base_all_path = 'magic/corpora/all/'

#es16_twitter_path =     X, y = load_xml_dataset(mapping[language + year[2:4]][type])
os.path.join(base_2016_path, 'pan16-author-profiling-training-corpus-spanish-2016-02-29')


mapping = {'spanish14': {'blogs': es14_blogs_path,
                         'socialmedia': es14_socialmedia_path,
                         'twitter': es14_twitter_path},
           'spanish15': {'twitter': base_2015_path + 'Training',
                         'test' : base_2015_path + 'Test',
                         'junto' : base_2015_path + 'junto'},
           'spanish16': {'twitter': base_2016_path + 'Training',
                         'blogs' : base_2016_path + 'Test' },
           'spanish17': {'twitter' : base_all_path}
           }


def load(label='gender', type='socialmedia', language='spanish', year='2014'):
    X, y = load_xml_dataset(mapping[language + year[2:4]][type])
    return X, y
