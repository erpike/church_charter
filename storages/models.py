from peewee import (
    Model,
    DateTimeField,
    CharField,
)
from datetime import datetime, UTC
from .database import db


class BaseModel(Model):
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    class Meta:
        database = db


class Canon(BaseModel):
    name = CharField(max_length=255)

    class Meta:
        table_name = "canon"
