import os
from lxml import etree
import pandas as pd
import logging

def load_xml_files(path:str):
    """Load author data
    
    This function loads the dataset from the given path, parses the xml files
    and concatenates the posts of each author in a single string object returning a list
    containing for each author his/her id and merged posts
    
    Args:
        path: the path to de folder where xml files are located
    Returns:
        data: a list of dicts containing the id and merged posts for each author
    """
    data = []
    parser = etree.XMLParser(recover=True)
    
    for file in os.listdir(path):
        if file.endswith(".xml"):
            tree = etree.parse(os.path.join(path, file), parser=parser)
            label = file[:file.find('.')]
            tweets = []
            for element in tree.getroot().iter():
                if element.tag == 'document' and element.text not in {"", None}:
                    tweets.append(element.text)
            data.append({"label": label, "posts" : '<EOP>'.join(tweets) + '<EOP>'})
        
    return data

def load_data(path:str, test = False):
    """Load author data
    
    This function loads the dataset from the given path, parses the xml files
    and concatenates the posts of each author in a single string object returning a list
    containing for each author his/her id and merged posts
    
    Args:
        path: the path to de folder where xml files are located
    Returns:
        data: a list of dicts containing the id and merged posts for each author
    """
    data = load_xml_files(path)
    df = pd.DataFrame(data)
    
    path_truth_file = os.path.join(path,"truth.txt")
    if not test:
        if not os.path.exists(path_truth_file):
            raise FileNotFoundError(path_truth_file)
        
        #header = ['id', 'gender', 'age']
        truth = pd.read_csv(path_truth_file, sep=":::", header=None, engine='python')# names=header, engine='python')
        df = df.set_index('label').join(truth.set_index(0)).reset_index(names='label')
        df = df.dropna()
        #df.to_csv(path + "data.csv")
    return df.values

logger = logging.getLogger(__name__)
