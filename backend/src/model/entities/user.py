from typing import Any, Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    id: int = Field(validation_alias=AliasChoices("user", "id"))
    posts: list[str] = []
    gender: Literal['MALE', 'FEMALE', 'M', 'F']
    age: Literal['18-24', '25-34', '35-49', '50-XX']
    collection_id: Optional[str | UUID] = None

    def model_post_init(self, __context: Any) -> None:
        self.gender = "MALE" if self.gender[0] == 'M' else "FEMALE"
