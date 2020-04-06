import pytest
from rftg.card import (
    load_file,
    load_one,
    TYPE_DEVELOPMENT,
    TYPE_WORLD,
    GOODTYPE_NOVELTY,
    GOODTYPE_RARE,
    GOODTYPE_GENE,
    GOODTYPE_ALIEN,
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


def test_load_one_with_produce():
    lines = [
        "N:New Vinland",
        "T:1:2:1",
        "E@0:1",
        "G:NOVELTY",
        "P:4:CONSUME_ANY | GET_2_CARD:1:1",
        "P:5:PRODUCE:0:0",
    ]
    res = load_one(lines)
    assert TYPE_WORLD == res.type
    assert len(res.powers) == 2
    assert GOODTYPE_NOVELTY == res.goodtype
    assert "5" in res.powers
    assert len(res.powers["5"]) == 1


def test_load_file():
    CARD_TYPES = load_file("cards.txt")
    assert len(CARD_TYPES) == 280


def test_gambling_world():
    lines = [
        "N:Gambling World",
        "T:1:1:1",
        "E@0:1@2:-1",
        "P:4:CONSUME_ANY | GET_VP:1:1",
        "P:4:DRAW_LUCKY:0:0",
    ]
    res = load_one(lines)
    assert TYPE_WORLD == res.type
    assert len(res.expansion) == 2
    assert "0" in res.expansion
    assert res.expansion["0"] == 1
    assert "2" in res.expansion
    assert res.expansion["2"] == -1


def test_build_base_set_1st_edition():
    CARD_TYPES = load_file("cards.txt")
    cards = build_base_set_1st_edition(CARD_TYPES)

    nb_base = 0
    nb_military_worlds = 0
    nb_no_military_worlds = 0
    nb_dev_6 = 0
    nb_dev_no_6 = 0
    nb_military_worlds_all = 0
    nb_military_worlds = dict()
    nb_military_worlds = dict()
    for i in range(8):
        nb_military_worlds[i] = list()
    nb_worlds_windfall_total = 0
    nb_worlds_windfall = dict()
    nb_worlds_windfall[GOODTYPE_NOVELTY] = 0
    nb_worlds_windfall[GOODTYPE_RARE] = 0
    nb_worlds_windfall[GOODTYPE_GENE] = 0
    nb_worlds_windfall[GOODTYPE_ALIEN] = 0
    nb_worlds_produce_total = 0
    nb_worlds_produce = dict()
    nb_worlds_produce[GOODTYPE_NOVELTY] = 0
    nb_worlds_produce[GOODTYPE_RARE] = 0
    nb_worlds_produce[GOODTYPE_GENE] = 0
    nb_worlds_produce[GOODTYPE_ALIEN] = 0

    nb_cost = dict()
    for i in range(8):
        nb_cost[i] = list()
    for card in cards:
        card_type = card["type"]
        if "START" in card_type.flags:
            nb_base = nb_base + 1
        else:
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
            nb_military_worlds[card_type.cost].append(card)

        if (card_type.type == TYPE_WORLD) and ("WINDFALL" in card_type.flags):
            nb_worlds_windfall[card_type.goodtype] = (
                nb_worlds_windfall[card_type.goodtype] + 1
            )
            nb_worlds_windfall_total = nb_worlds_windfall_total + 1

        if (
            (card_type.type == TYPE_WORLD)
            and (len(card_type.powers) > 0)
            and (card_type.goodtype in [GOODTYPE_NOVELTY, "RARE", "GENE", "ALIEN"])
            and ("WINDFALL" not in card_type.flags)
        ):
            if card_type.goodtype != "ANY":
                nb_worlds_produce[card_type.goodtype] = (
                    nb_worlds_produce[card_type.goodtype] + 1
                )
            nb_worlds_produce_total = nb_worlds_produce_total + 1

        if "MILITARY" not in card_type.flags:
            nb_cost[card_type.cost].append(card)

    # for c in nb_cost[1]:
    #    print(f" {c['type'].name} :\t\t\t {c['type'].type} ")

    assert 5 == nb_base
    # assert 22 == len(nb_military_worlds)
    # assert 37 == nb_no_military_worlds
    assert 12 == nb_dev_6
    assert 38 == nb_dev_no_6

    assert 23 == nb_military_worlds_all
    assert len(nb_military_worlds[1]) == 6
    assert len(nb_military_worlds[2]) == 7
    assert len(nb_military_worlds[3]) == 3
    assert len(nb_military_worlds[4]) == 2

    assert 25 == nb_worlds_windfall_total
    assert 5 == nb_worlds_windfall[GOODTYPE_NOVELTY]
    assert 7 == nb_worlds_windfall[GOODTYPE_RARE]
    assert 7 == nb_worlds_windfall[GOODTYPE_GENE]
    assert 6 == nb_worlds_windfall[GOODTYPE_ALIEN]

    assert 21 == nb_worlds_produce_total
    assert 9 == nb_worlds_produce[GOODTYPE_NOVELTY]
    assert 6 == nb_worlds_produce[GOODTYPE_RARE]
    assert 4 == nb_worlds_produce[GOODTYPE_GENE]
    assert 2 == nb_worlds_produce[GOODTYPE_ALIEN]

    assert len(nb_cost[0]) == 2
    assert len(nb_cost[1]) == 18
    assert len(nb_cost[2]) == 23
    assert len(nb_cost[3]) == 14
    assert len(nb_cost[4]) == 13
    assert len(nb_cost[5]) == 7
    assert len(nb_cost[6]) == 14

    assert 114 == len(cards)
