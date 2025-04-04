from peewee import (
    Model,
    DateTimeField,
    CharField,
    TextField,
    SqliteDatabase, 
)
from datetime import datetime, UTC


db = SqliteDatabase("cc.sqlite3")


class BaseModel(Model):
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    class Meta:
        database = db


class Canon(BaseModel):
    name = CharField(max_length=255)

    class Meta:
        table_name = "canon"
