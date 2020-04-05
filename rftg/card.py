TYPE_WORLD = 1
TYPE_DEVELOPMENT = 2
GOODTYPE_NOVELTY = "NOVELTY"

class Card:
    def __init__(self, name, type, cost, vp, expansion, goodtype, flags, powers, extra_victory):
        self.name = name
        self.type = type
        self.cost = cost
        self.vp = vp
        self.expansion = expansion
        self.goodtype = goodtype
        self.flags = flags
        self.powers = powers
        self.extra_victory = extra_victory


def load_one(lines):
    """
# N:card name
# T:type:cost:vp
#   Type is 1: world, 2: development
# E@e0:n0@e1:n1[...]
#   Number of this card introduced at each expansion level
# G:goodtype
#   Only valid for worlds, and optional there
# F:flags
#   START world, MILITARY, WINDFALL, REBEL, ALIEN, IMPERIUM, etc
# P:phase:code:value:times
#   Times is only relevant for certain consume powers
# V:value:type:name
#   Extra victory points for 6-cost developments
    """
    card = {"flags": [], "extra_victory": []}
    goodtype = None
    powers = dict()
    for line in lines:
        if "N" == line[:1]:
            card["name"] = line[2:].strip()
        elif "T" == line.split(":")[0]:
            card["type"] = int(line.split(":")[1])
            card["cost"] = int(line.split(":")[2])
            card["vp"] = int(line.split(":")[3])
        elif "E" == line[:1]:
            card["expansion"] = dict()
            exp_lines = line[2:].split("@")
            for exp_line in exp_lines:
                card["expansion"][exp_line.split(":")[0]] = int(exp_line.split(":")[1])
        elif "G" == line[:1]:
            goodtype = line[2:]
        elif "F" == line[:1]:
            for item in line[2:].split("|"):
                card["flags"].append(item.strip())
        elif "P" == line[:1]:
            power_line = line[2:]
            power_step = power_line[:1]
            if (power_step not in powers):
                powers[power_step] = list()
            powers[power_step].append(power_line[2])
        elif "V" == line[:1]:
            card["extra_victory"].append(line[2:])
    return Card(
        card["name"],
        card["type"],
        card["cost"],
        card["vp"],
        card["expansion"],
        goodtype,
        card["flags"],
        powers,
        card["extra_victory"],
    )


def load_file(file):
    cards = dict()

    with open(file) as card_file:
        lines = list()
        for line in card_file.readlines():
            if "#" == line[:1]:
                pass
            elif "" == line.strip():
                # manage previous card
                if lines is not None and len(lines) > 0:
                    card = load_one(lines)
                    cards[card.name] = card
                lines = list()
            else:
                lines.append(line.strip())
        # manage previous card
        if lines is not None and len(lines) > 0:
            card = load_one(lines)
            cards[card.name] = card
    return cards


def build_base_set_1st_edition(card_types):
    cards = list()
    for name in card_types:
        card_type = card_types[name]
        if "0" in card_type.expansion and "PROMO" not in card_type.flags:
            for _ in range(card_type.expansion["0"]):
                cards.append({"type": card_type})
    return cards
