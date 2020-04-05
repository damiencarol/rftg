import pytest
from rftg.card import load_file

cards = load_file("cards.txt")


@pytest.mark.parametrize("name", ["Galactic Survey: SETI"])
def test_name(name):
    assert name in cards.keys()


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
    assert name in cards.keys()
    assert cards[name].vp == vp
