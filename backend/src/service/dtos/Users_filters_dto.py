from model.exceptions import InputValidationException
from pydantic import BaseModel, ValidationError
from enum import Enum
from typing import Annotated, Dict, List, Literal, Tuple
from annotated_types import Gt

class FieldsInputValidationException(InputValidationException):
    def __init__(self, field_errors):
        self.errors = field_errors
        super().__init__("")
    def json(self):
        return {
            "error": {
                "errorType": self.__class__.__name__.removesuffix("Exception"),
                "fieldsErrors": self.errors
            }
        }


class Age_dto(Enum):
    YOUNG = "18-24"
    YOUNG_ADULT = "25-34"
    SENIOR_ADULT = "34-49"
    SENIOR = "50-XX"


class Gender_dto(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class Users_filters_dto(BaseModel):
    age: Age_dto | None = None
    gender: Gender_dto | None = None

def validate_filters(filters) -> Users_filters_dto:
    try:
        return Users_filters_dto(**filters).model_dump(exclude_unset=True)
    except ValidationError as e:
        raise FieldsInputValidationException(e.errors())

