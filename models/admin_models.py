from ast import For
from datetime import datetime
from typing import Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


class CreatePost(BaseModel):
    file: UploadFile = File(...)
    title: str = Form(...)
    category: str = Form(...)
    tags: str = Form(...)
    createdAt: datetime = Form(...)
    modifiedAt: datetime = Form(...)
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "file": "example.md",
                "title": "Example Title",
                "category": "General",
                "tags": ["tag1", "tag2", "tag3"],
                "createdAt": "2024-04-16-13-23",
                "modifiedAt": "2024-04-16-13-23",
            }
        }
    )
    