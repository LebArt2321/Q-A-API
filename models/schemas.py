from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Any

class QuestionBase(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()

    model_config = ConfigDict(from_attributes=True)

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnswerBase(BaseModel):
    text: str
    user_id: str

    @field_validator("text", "user_id")
    @classmethod
    def validate_fields(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    model_config = ConfigDict(from_attributes=True)

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)