import pytest

from storages.models import Canon, CanonChapter, CanonItem, CanonItemType


@pytest.fixture
def test_canon(init_test_db):
    """Create a test canon with chapters and items."""
    canon = Canon.create(name="Канон тестовий")
    # Create chapters in different groups
    s1 = CanonChapter.create(
        canon=canon,
        title="Песнь 1",
        position=0,
        type="song",
        group="song1",
    )

    tr1 = CanonChapter.create(
        canon=canon,
        title="Тропарь (після пісні 3)",
        position=1,
        group="intermediate1",
        type="troparion",
    )

    # Create items for chapters
    CanonItem.create(chapter=s1, type="hirmos", text="Ірмос першої пісні", position=0)
    CanonItem.create(
        chapter=s1,
        type="refrain",
        text="приспів канону",
        position=1,
    )
    CanonItem.create(
        chapter=s1,
        type="troparion",
        text="куплетт першої пісні",
        position=2,
    )
    CanonItem.create(
        chapter=s1,
        type="refrain",
        text="приспів канону",
        position=3,
    )

    CanonItem.create(
        chapter=tr1,
        type="refrain",
        text="Тропар після третьої пісні",
        position=0,
    )


def test_display_content(test_canon):
    """Test that display_content shows content in correct order.

    The order should follow CanonChapterGroup structure.
    """
    # Create test canon
    c = Canon.get(id=1)

    # Get grouped content
    content = c.get_data()

    # Check that groups are in correct order
    assert list(content.keys()) == [
        "song1",
        "intermediate1",
    ], "Groups are not in the correct order"

    # Check content in each group
    for group, chapters_data in content.items():
        # Check chapters in group
        for chapter_data in chapters_data:
            chapter = chapter_data["chapter"]
            items = chapter_data["items"]
            # Check that items are ordered by position
            item_positions = [item.position for item in items]
            assert item_positions == sorted(
                item_positions
            ), f"Items in chapter {chapter.title} are not ordered by position"

            # Check that items have correct types and text
            for item in items:
                assert (
                    item.type in CanonItemType.values()
                ), f"Invalid item type: {item.type}"
                assert item.text, f"Item text is empty for {item.type}"
