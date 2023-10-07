from model.exceptions import InputValidationException
from pydantic import BaseModel, ValidationError
from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional, Tuple


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

class Users_filters_dto(BaseModel):
    age: Optional[Literal['18-24', '25-34', '35-49', '50-XX']] = None
    gender: Optional[Literal['MALE', 'FEMALE']] = None


def validate_filters(filters) -> Users_filters_dto:
    try:
        return Users_filters_dto(**filters).model_dump(exclude_unset=True)
    except ValidationError as e:
        raise FieldsInputValidationException(e.errors())
