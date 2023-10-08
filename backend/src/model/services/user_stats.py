from typing import Annotated
from pydantic import BaseModel, validator
from annotated_types import Ge
from typing_extensions import Dict


class User_stats(BaseModel):
    age: Dict[str, Annotated[int, Ge(0)]] = {}
    gender: Dict[str, Annotated[int, Ge(0)]] = {}
    total_users: Annotated[int, Ge(0)] = 0

    @validator("age")
    def validate_age(cls, age):
        for clave in age.keys():
            if clave not in ['18-24','25-34','35-49','50-XX']:
                raise ValueError(f"Clave '{clave}' no permitida")
        return age
    @validator("gender")
    def validate_gender(cls, gender):
        for clave in gender.keys():
            if clave not in ['MALE','FEMALE']:
                raise ValueError(f"Clave '{clave}' no permitida")
        return gender