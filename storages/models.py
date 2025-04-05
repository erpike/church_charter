from datetime import UTC, datetime
from enum import Enum

from flask_login import UserMixin
from peewee import (
    CharField,
    Check,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .database import db


class BaseModel(Model):
    """Base model with common fields for all models."""

    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    def save(self, *args, **kwargs):
        if not self.get_id():
            self.created_at = datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert string timestamps to datetime objects if needed
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(
                self.created_at.replace("Z", "+00:00")
            )
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(
                self.updated_at.replace("Z", "+00:00")
            )

    class Meta:
        database = db


class User(BaseModel, UserMixin):
    """Model representing an admin user."""

    username = CharField(max_length=80, unique=True)
    password_hash = CharField(max_length=128)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    class Meta:
        table_name = "user"


class Canon(BaseModel):
    """Model representing a canon in the Orthodox Church."""

    name = CharField(max_length=255)

    class Meta:
        table_name = "canon"

    def __str__(self):
        return self.name


class CanonChapterType(str, Enum):
    """Types of chapters in a canon."""

    song = "song"
    troparion = "troparion"
    kontakion = "kontakion"
    stichos = "stichos"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)

    @property
    def display_name(self) -> str:
        """Get display name in Ukrainian."""
        return {
            CanonChapterType.song: "пісня",
            CanonChapterType.troparion: "тропар",
            CanonChapterType.kontakion: "кондак",
            CanonChapterType.stichos: "стихіра",
        }[self]


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


class CanonItemType(str, Enum):
    """Types of items in a canon chapter."""

    refrain = "refrain"
    hirmos = "hirmos"
    ikos = "ikos"
    song = "song"
    troparion = "troparion"
    kontakion = "kontakion"
    stichos = "stichos"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)

    @property
    def display_name(self) -> str:
        """Get display name in Ukrainian."""
        return {
            CanonItemType.refrain: "приспів",
            CanonItemType.hirmos: "ірмос",
            CanonItemType.ikos: "ікос",
            CanonItemType.song: "пісня",
            CanonItemType.troparion: "тропар",
            CanonItemType.kontakion: "кондак",
            CanonItemType.stichos: "стихіра",
        }[self]


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
