from typing import Any, Literal
from pydantic import BaseModel


class User_dto(BaseModel):
    id: int
    posts: list[str]
    gender: Literal['MALE', 'FEMALE']
    age: Literal['18-24', '25-34', '35-49', '50-XX']
