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


class CanonChapterGroup(str, Enum):
    beginning = "beginning"
    song1 = "song1"
    song2 = "song2"
    song3 = "song3"
    intermediate1 = "intermediate1"
    song4 = "song4"
    song5 = "song5"
    song6 = "song6"
    intermediate2 = "intermediate2"
    song7 = "song7"
    song8 = "song8"
    song9 = "song9"
    ending = "ending"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)


class CanonChapterType(str, Enum):
    """Types of chapters in a canon."""

    ikos = "ikos"
    kontakion = "kontakion"
    sessional_hymn = "sessional hymn"
    song = "song"
    stichos = "stichos"
    theotokion = "theotokion"
    trinitarian = "trinitarian"
    troparion = "troparion"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)

    @property
    def display_name(self) -> str:
        """Get display name in Ukrainian."""
        return {
            CanonChapterType.ikos: "ікос",
            CanonChapterType.kontakion: "кондак",
            CanonChapterType.sessional_hymn: "сидален",
            CanonChapterType.song: "пісня",
            CanonChapterType.stichos: "стихіра",
            CanonChapterType.theotokion: "Богородичен",
            CanonChapterType.trinitarian: "Троїчен",
            CanonChapterType.troparion: "тропар",
        }[self]


class CanonItemType(str, Enum):
    """Types of items in a canon chapter."""

    ikos = "ikos"
    kontakion = "kontakion"
    sessional_hymn = "sessional hymn"
    song = "song"
    stichos = "stichos"
    theotokion = "theotokion"
    trinitarian = "trinitarian"
    troparion = "troparion"

    # unique for item:
    refrain = "refrain"
    hirmos = "hirmos"

    @classmethod
    def values(cls):
        """Return all values as a comma-separated string for SQL."""
        return ", ".join(f"'{item.value}'" for item in cls)

    @property
    def display_name(self) -> str:
        """Get display name in Ukrainian."""
        return {
            CanonItemType.ikos: "ікос",
            CanonItemType.kontakion: "кондак",
            CanonItemType.sessional_hymn: "сидален",
            CanonItemType.song: "пісня",
            CanonItemType.stichos: "стихіра",
            CanonItemType.theotokion: "Богородичен",
            CanonItemType.trinitarian: "Троїчен",
            CanonItemType.troparion: "тропар",
            #
            CanonItemType.refrain: "приспів",
            CanonItemType.hirmos: "ірмос",
        }[self]


class Canon(BaseModel):
    """Model representing a canon in the Orthodox Church."""

    name = CharField(max_length=255)

    class Meta:
        table_name = "canon"

    def __str__(self):
        return self.name


class CanonChapter(BaseModel):
    """Model representing a chapter within a canon."""

    canon = ForeignKeyField(Canon, backref="chapters", on_delete="CASCADE")
    title = CharField(max_length=255)
    position = IntegerField(default=0)
    group = CharField(
        max_length=32,
        constraints=[Check(f"type IN ({CanonChapterGroup.values()})")],
    )
    type = CharField(
        max_length=32,
        constraints=[Check(f"type IN ({CanonChapterType.values()})")],
    )

    class Meta:
        table_name = "canonchapter"
        indexes = ((("canon", "title"), True),)

    def __str__(self):
        return f"{self.canon.name} - {self.title}"


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
