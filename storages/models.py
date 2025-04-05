from datetime import UTC, datetime

from peewee import (
    CharField,
    Check,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

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


class CanonItem(BaseModel):
    canon = ForeignKeyField(Canon, backref="items", on_delete="CASCADE")
    type = CharField(
        max_length=255,
        constraints=[
            Check(
                """type IN (
                'hirmos', 'ikos', 'song', 'troparion', 'kontakion', 'stichos'
            )"""
            )
        ],
    )
    text = TextField()
    position = IntegerField(default=0)

    class Meta:
        table_name = "canonitem"
