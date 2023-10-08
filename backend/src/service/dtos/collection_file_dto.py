import csv
from io import StringIO
from typing import Any, Literal
from model.exceptions import InvalidFileException
from pydantic import BaseModel as PydanticBaseModel
import pandas as pd


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class Collection_file_dto(BaseModel):
    filename: str
    filetype: Literal['csv']
    content: StringIO

    def model_post_init(self, __context: Any) -> None:
        self.__validate_file()

    def __validate_file(self):
        try:
            lector_csv = csv.reader(self.content)
            next(lector_csv)
            columns = next(lector_csv)

            # Verificar que las columnas "id" y "posts" estén presentes
            if not {"label", "post"} <= set(columns):
                raise InvalidFileException(
                    "El archivo debe contener al menos las siguientes columnas {label, posts}: " + str(columns))

            self.content.seek(0)
        except Exception as e:
            raise RuntimeError(e.args)

    def get_users_posts(self):
        self.content.seek(0)
        df = pd.read_csv(self.content, encoding='utf-8')
        df['post'] = df['post'].transform(lambda x: str(x))
        df = df.groupby(['label'])['post'].apply(list).reset_index()
        df = df.drop_duplicates(subset='label').reset_index(drop=True)
        df.rename(columns={'post': 'posts'}, inplace=True)
        return df.set_index('label')['posts'].to_dict()
