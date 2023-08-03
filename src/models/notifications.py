import uuid

from models.base import BaseOrjsonModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID


class NewSeriesModel(BaseOrjsonModel):
    movie_id: str
    movie_name: str
    series_number: int
    user_id: str
    user_name: str
    user_email: str


class Series(NewSeriesModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)


class NewSeriesModelRead(NewSeriesModel):
    id: uuid.UUID


class VerifyUserModel(BaseOrjsonModel):
    user_id: str
    user_email: str
    user_name: str


class LikeModel(BaseOrjsonModel):
    user_id: str
    user_name: str
    user_email: str
    like_subject: str
    subject_id: str



