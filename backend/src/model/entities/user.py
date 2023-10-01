from typing import Literal
from uuid import UUID
from pydantic import BaseModel

class User(BaseModel):
    id: str
    posts: list[str]
    gender: Literal['MALE','FEMALE','M','F']
    age: Literal['18-24','25-34','35-49','50-XX']
    collection_id: str | UUID
