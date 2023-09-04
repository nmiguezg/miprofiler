import re
import spacy
import nltk
import pandas as pd
import emoji
from lxml import etree
import os

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
html_tag_re = re.compile(r'</?[\w]*>\b')

def _preprocess_feed(tweet: str):
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
    t = t.replace("\n", "")
    t = re.sub(user_re, "@username", t)
    #t = t.replace("#", " <HASHTAG> ")
    #t = re.sub(mention_re, " <MENTION> ", t)
    t = re.sub(smile_re, " <EMOTICON> ", t)
    # t = re.sub(emoji_re, " <EMOJI> ", t)
    #t = re.sub(time_re, " <TIME> ", t)
    #t = re.sub(numbers_re, " <NUMBER> ", t)
    t = re.sub(html_tag_re, "", t)
    t = re.sub(not_ascii_re, "", t)
    t = re.sub(space_collapse_re, " ", t)
    t = t.strip()
    return t

def parse_xml_corpus(path: str, parser=etree.XMLParser(recover=True)):
    """For a directory given parses its xml files
    and returns a list with each parsed file"""
    data = []
    for file in os.listdir(path):
        if str(file).endswith(".xml"):
            data.append([etree.parse(path + file, parser=parser), file[:(file.find('.'))]])
    return data

def group_authors(df_: pd.DataFrame):
    df = df_.copy()
    df['post'] = df.groupby(['label'])['post'].transform(lambda x: ' '.join(x))
    return df.drop_duplicates(subset='label').reset_index(drop=True)

def load_dataset(input_dir):
    xml_tree = parse_xml_corpus(input_dir)
    data = []
    for i, tree in enumerate(xml_tree):
        root = tree[0].getroot()
        author_id = tree[1]

        for element in root.iter():
            if element.tag == 'document':
                if element.text != None and element.text.find("Tweet / Twitte") == -1:
                    data.append({"label": author_id, "post": _preprocess_feed(element.text)})
    # Labels
    header = ['id', 'gender', 'age']
    labels = pd.read_csv(input_dir + 'truth.txt', sep=":::", names=header, engine='python')
    df = pd.DataFrame(data)
    df = df.set_index('label').join(labels.set_index('id')).reset_index(names='label')
    df = df.dropna(subset = ['gender'])
    df = df.dropna()
    return group_authors(df)
