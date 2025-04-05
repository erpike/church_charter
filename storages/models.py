from datetime import UTC, datetime
from enum import Enum

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
    """Base model with common fields for all models."""

    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    class Meta:
        database = db


class Canon(BaseModel):
    """Model representing a canon in the Orthodox Church."""

    name = CharField(max_length=255)

    class Meta:
        table_name = "canon"

    def __str__(self):
        return self.name


class CanonChapterType(Enum):
    """Enum for the types of chapters in a canon."""

    SONG = "song"
    TROPARION = "troparion"
    KONTAKION = "kontakion"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)


class CanonChapter(BaseModel):
    """Model representing a chapter within a canon."""

    canon = ForeignKeyField(Canon, backref="chapters", on_delete="CASCADE")
    title = CharField(max_length=255)
    position = IntegerField(default=0)
    type = CharField(
        max_length=32,
        constraints=[Check(f"type IN ({CanonChapterType.values()})")],
    )

    class Meta:
        table_name = "canonchapter"
        indexes = ((("canon", "title"), True),)

    def __str__(self):
        return f"{self.canon.name} - {self.title}"


class CanonItemType(Enum):
    """Enum for the types of items in a canon."""

    REFRAIN = "refrain"
    HIRMOS = "hirmos"
    IKOS = "ikos"
    SONG = "song"
    TROPARION = "troparion"
    KONTAKION = "kontakion"
    STICHOS = "stichos"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)


class CanonItem(BaseModel):
    """Model representing an item (text) within a canon chapter."""

    chapter = ForeignKeyField(CanonChapter, backref="items", on_delete="CASCADE")
    type = CharField(
        max_length=32,
        constraints=[Check(f"type IN ({CanonItemType.values()})")],
    )
    text = TextField()
    position = IntegerField(default=0)

    class Meta:
        table_name = "canonitem"

    def __str__(self):
        return f"{self.canonchapter.title} - {self.type}"
