from abc import ABC, abstractmethod
import pickle
import random
import numpy as np

import pandas as pd
from sklearn import preprocessing
import tensorflow as tf
from tokenizers import Tokenizer
import transformers

class Generic_profiler(ABC):
    
    @abstractmethod
    def predict(self, df):
        pass
    def process_csv(self, coll_csv, sep=' '):
        df = pd.read_csv(coll_csv)
        df['post'] = df['post'].transform(lambda x: str(x))
        df = df.groupby(['label'])['post'].apply(sep.join).reset_index()
        df = df.drop_duplicates(subset='label').reset_index(drop=True)
        return df['label'], df['post']

class LosCalis_profiler(Generic_profiler):
    def __init__(self) -> None:
        with open('model/encoders.pickle', 'rb') as handle:
            self.enc_gender, self.enc_age = pickle.load(handle)
        with open('model/tokenizer.pickle', 'rb') as handle:
            tokenizer_bert, tokenizer_maria = pickle.load(handle)
        self.tokenizers = tokenizer_bert, tokenizer_maria
        # Cargar el archivo JSON que contiene la arquitectura
        with open('model/modelo.json', 'r', encoding='utf-8') as json_file:
            loaded_model_json = json_file.read()
        self.model = tf.keras.models.model_from_json(loaded_model_json,
                                                     custom_objects={
                                                         "TFBertModel": transformers.TFBertModel,
                                                         "TFRobertaModel" : transformers.TFRobertaModel
                                                         }
                                                     )
        self.model.load_weights('model/modelo.h5')
        
    def process_csv(self, coll_csv, sep=' '):
        df = pd.read_csv(coll_csv)
        df = df.dropna()
        df = pd.DataFrame(self._group_posts(df))
        return df
    
    def predict(self, df):    
        samples = df.values
        x_bert = self._create_inputs_targets(samples, self.tokenizers[0])
        x_maria = self._create_inputs_targets(samples, self.tokenizers[1])

        encoders = {'gender': self.enc_gender, 'age': self.enc_age}
        df['index'] = [i for i in range(0, len(df))]
        posts_per_user = df.groupby('label')['index'].apply(list).to_dict()

        y_pred = self.model.predict([x_bert[0], x_bert[1], x_bert[2], x_maria[0], x_maria[1], x_maria[2]])
        eval_data = list()
        for user in posts_per_user.keys():
            row = dict()
            row['label'] = user
            for i,label in enumerate(['gender', 'age']):
                if label == 'age':
                    y_label = np.argmax(np.mean(y_pred[i][posts_per_user[user]], axis = 0))
                else:
                    y_label = round(np.mean(y_pred[i][posts_per_user[user]]))


                row[label] = y_label
            eval_data.append(row)

        evaluation_df = pd.DataFrame(eval_data)
        for column in evaluation_df.columns[1:]:
            evaluation_df[column] = encoders[column].inverse_transform(evaluation_df[column])

        return evaluation_df.values
    
    def _group_posts(self, df: pd.DataFrame, max_tokens=510):
        new_data = []
        users = list(df['label'].unique())
        for user in users:
            user_posts = df[df['label'].isin([user])]
            posts = user_posts['post'].values
            random.shuffle(posts)
            num_tokens = 0
            samples = []
            for post in posts:
                max_tokens_post = max([len(tokenizer.encode(post))
                                    for tokenizer in self.tokenizers])
                if (num_tokens + max_tokens_post > max_tokens):
                    post_sample = ' '.join(samples)
                    new_data.append({'label': user, 'post': post_sample})
                    num_tokens = max_tokens_post
                    samples = [post]
                else:
                    num_tokens = num_tokens + max_tokens_post
                    samples.append(post)

            if num_tokens > 0:
                post_sample = ' '.join(samples)
                new_data.append({'label': user, 'post': post_sample})
        return new_data
    


    def _create_inputs_targets(self, samples, tokenizer:Tokenizer):
        dataset_dict = {
            "input_ids": [],
            "token_type_ids": [],
            "attention_mask": []
        }

        sentences = samples[:, -1]
        for sentence in sentences:
            input_ids = []
            input_ids = tokenizer.encode(sentence, add_special_tokens=True)

            # Keep the tokens of each sentence to improve evaluation
            # Pad truncate
            input_ids = input_ids[:512-2]

            input_ids = [4] + input_ids + [5]
            token_type_ids = [0] * len(input_ids)
            attention_mask = [1] * len(input_ids)
            padding_len = 512 - len(input_ids)

            input_ids = input_ids + ([0] * padding_len)
            attention_mask = attention_mask + ([0] * padding_len)
            token_type_ids = token_type_ids + ([0] * padding_len)

            dataset_dict["input_ids"].append(input_ids)
            dataset_dict["token_type_ids"].append(token_type_ids)
            dataset_dict["attention_mask"].append(attention_mask)

        for key in dataset_dict:
            dataset_dict[key] = np.array(dataset_dict[key])

        x = [
            dataset_dict["input_ids"],
            dataset_dict["token_type_ids"],
            dataset_dict["attention_mask"],
        ]
        return x