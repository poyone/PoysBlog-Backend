from ast import For
from datetime import datetime
from typing import Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]
class Post(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    slug: str
    content: str
    tags: list[str]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,

    )
    
    
