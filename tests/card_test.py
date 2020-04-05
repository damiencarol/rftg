import pytest
from rftg.card import (
    load_file,
    load_one,
    TYPE_DEVELOPMENT,
    TYPE_WORLD,
    build_base_set_1st_edition,
)


def test_load_one():
    lines = [
        "N:Contact Specialist",
        "T:2:1:1",
        "E@0:2@1:1",
        "P:3:EXTRA_MILITARY:-1:0",
        "P:3:PAY_MILITARY:1:0",
    ]
    res = load_one(lines)
    assert "Contact Specialist" == res.name
    assert TYPE_DEVELOPMENT == res.type


def test_load_one_with_flags():
    lines = [
        "N:Gateway Station",
        "T:1:0:0",
        "E@0:1",
        "#E:1:1:1:1:1",
        "G:ANY",
        "F:PROMO",
    ]
    res = load_one(lines)
    assert res.flags is not None
    assert TYPE_WORLD == res.type
    assert "PROMO" in res.flags


def test_load_one_with_extra_victory():
    lines = [
        "N:Pan-Galactic League",
        "T:2:6:0",
        "E@0:1",
        "P:3:EXTRA_MILITARY:-1:0",
        "P:5:DRAW_WORLD_GENE:1:0",
        "V:2:GENE_PRODUCTION:N/A",
        "V:2:GENE_WINDFALL:N/A",
        "V:1:MILITARY:N/A",
        "V:3:NAME:Contact Specialist",
    ]
    res = load_one(lines)
    assert TYPE_DEVELOPMENT == res.type
    assert len(res.extra_victory) > 0


@pytest.mark.parametrize("name", ["Galactic Survey: SETI"])
def test_name(name):
    CARD_TYPES = load_file("cards.txt")
    assert name in CARD_TYPES.keys()


@pytest.mark.parametrize(
    "name, vp",
    [
        ("Space Marines", 1),
        ("Contact Specialist", 1),
        ("Pan-Galactic League", 0),
        ("Comet Zone", 2),
    ],
)
def test_name(name, vp):
    CARD_TYPES = load_file("cards.txt")
    assert name in CARD_TYPES.keys()
    assert CARD_TYPES[name].vp == vp


def test_build_base_set_1st_edition():
    CARD_TYPES = load_file("cards.txt")
    cards = build_base_set_1st_edition(CARD_TYPES)

    nb_base = 0
    nb_military_worlds = 0
    nb_no_military_worlds = 0
    nb_dev_6 = 0
    nb_dev_no_6 = 0
    nb_military_worlds_all = 0
    nb_worlds_windfall = 0
    for card in cards:
        card_type = card["type"]
        if "START" in card_type.flags:
            nb_base = nb_base + 1
        else:
            if ("MILITARY" in card_type.flags) and (card_type.type == TYPE_WORLD):
                nb_military_worlds = nb_military_worlds + 1
            if ("MILITARY" not in card_type.flags) and (card_type.type == TYPE_WORLD):
                nb_no_military_worlds = nb_no_military_worlds + 1
            if (
                (card_type.cost == 6)
                and (card_type.type == TYPE_DEVELOPMENT)
                and (len(card_type.extra_victory) > 0)
            ):
                nb_dev_6 = nb_dev_6 + 1
            if (
                (card_type.cost < 6)
                and (card_type.type == TYPE_DEVELOPMENT)
                and (len(card_type.extra_victory) == 0)
            ):
                nb_dev_no_6 = nb_dev_no_6 + 1

        if (card_type.type == TYPE_WORLD) and ("MILITARY" in card_type.flags):
            nb_military_worlds_all = nb_military_worlds_all + 1

        if (card_type.type == TYPE_WORLD) and ("WINDFALL" in card_type.flags):
            nb_worlds_windfall = nb_worlds_windfall + 1

    assert 5 == nb_base
    assert 22 == nb_military_worlds
    # assert 37 == nb_no_military_worlds
    assert 12 == nb_dev_6
    assert 38 == nb_dev_no_6

    assert 23 == nb_military_worlds_all

    assert 25 == nb_worlds_windfall
    # assert 114 == len(cards)
