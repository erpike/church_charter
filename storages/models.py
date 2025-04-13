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

    @property
    def display_name(self) -> str:
        """Get display name in Ukrainian."""
        return {
            CanonChapterGroup.beginning: "Початок",
            CanonChapterGroup.song1: "Пісня 1",
            CanonChapterGroup.song2: "Пісня 2",
            CanonChapterGroup.song3: "Пісня 3",
            CanonChapterGroup.intermediate1: "Після пісні 3",
            CanonChapterGroup.song4: "Пісня 4",
            CanonChapterGroup.song5: "Пісня 5",
            CanonChapterGroup.song6: "Пісня 6",
            CanonChapterGroup.intermediate2: "Після пісні 6",
            CanonChapterGroup.song7: "Пісня 7",
            CanonChapterGroup.song8: "Пісня 8",
            CanonChapterGroup.song9: "Пісня 9",
            CanonChapterGroup.ending: "Кінець",
        }[self]


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

    def get_data(self):
        """
        Get canon content grouped by group and ordered by position.

        Returns a dictionary where keys are group names and values are lists of
        chapters with their sorted items.
        """
        # Get all chapters ordered by group and position
        chapters = (
            CanonChapter.select()
            .where(CanonChapter.canon == self)
            .order_by(CanonChapter.group, CanonChapter.position)
        )

        # Group chapters by their group
        grouped_content = {}
        for chapter in chapters:
            if chapter.group not in grouped_content:
                grouped_content[chapter.group] = []

            # Get items for this chapter ordered by position
            items = list(
                CanonItem.select()
                .where(CanonItem.chapter == chapter)
                .order_by(CanonItem.position)
            )

            # Add chapter with its items to the group
            grouped_content[chapter.group].append({"chapter": chapter, "items": items})

        # Create ordered result following CanonChapterGroup order
        ordered_content = {}
        for group in CanonChapterGroup:
            if group.value in grouped_content:
                ordered_content[group.value] = grouped_content[group.value]

        return ordered_content


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
        return f"{self.chapter.title} - {self.type}"


class AggregatedCanon(BaseModel):
    """Model representing an aggregated canon composed of multiple canons."""

    name = CharField(max_length=255)
    canon_ids = TextField(unique=True)

    class Meta:
        table_name = "aggregatedcanon"

    def __str__(self):
        return self.name

    @classmethod
    def find_existing_combination(cls, canon_ids):
        """
        Find an existing aggregated canon with the same combination of canons.

        Args:
            canon_ids: List of canon IDs in the order they should appear

        Returns:
            AggregatedCanon instance if found, None otherwise
        """
        # Convert list to string for comparison
        canon_ids_str = ",".join(map(str, canon_ids))

        try:
            return cls.get(cls.canon_ids == canon_ids_str)
        except cls.DoesNotExist:
            return None

    def get_data(self):
        """
        Get aggregated canon content grouped by group and ordered by position.

        Returns a dictionary where keys are group names and values are lists of
        chapters with their sorted items, ordered by:
        1. CanonChapterGroup order
        2. User-specified canon order
        3. Chapter position within each canon
        4. Item position within each chapter
        """
        # Parse canon IDs and their positions
        canon_positions = [
            (int(canon_id), pos)
            for pos, canon_id in enumerate(self.canon_ids.split(","))
        ]

        # Group chapters by their group
        grouped_content = {}
        for canon_id, position in canon_positions:
            canon = Canon.get_or_none(Canon.id == canon_id)
            if not canon:
                continue

            # Get all chapters ordered by group and position
            chapters = (
                CanonChapter.select()
                .where(CanonChapter.canon == canon)
                .order_by(CanonChapter.group, CanonChapter.position)
            )

            for chapter in chapters:
                if chapter.group not in grouped_content:
                    grouped_content[chapter.group] = []

                # Get items for this chapter ordered by position
                items = list(
                    CanonItem.select()
                    .where(CanonItem.chapter == chapter)
                    .order_by(CanonItem.position)
                )

                # Add chapter with its items to the group
                grouped_content[chapter.group].append(
                    {"chapter": chapter, "items": items, "canon_order": position}
                )

        # Create ordered result following CanonChapterGroup order
        ordered_content = {}
        for group in CanonChapterGroup:
            if group.value in grouped_content:
                # Sort chapters within each group by canon_order and position
                chapters = grouped_content[group.value]
                chapters.sort(key=lambda x: (x["canon_order"], x["chapter"].position))
                ordered_content[group.value] = chapters

        return ordered_content
