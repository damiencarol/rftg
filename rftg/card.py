class Card:
    def __init__(self, name, type, cost, vp, expansion, expansion_number):
        self.name = name
        self.type = type
        self.cost = cost
        self.vp = vp
        self.expansion = expansion
        self.expansion_number = expansion_number


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
    card = {}
    for line in lines:
        if "N" == line[:1]:
            card["name"] = line[2:].strip()
        elif "T" == line.split(":")[0]:
            card["type"] = line.split(":")[1]
            card["cost"] = int(line.split(":")[2])
            card["vp"] = int(line.split(":")[3])
        elif "E" == line[:1]:
            exp_line = line[2:]
            card["expansion"] = exp_line.split(":")[0]
            card["expansion_number"] = exp_line.split(":")[1]
    return Card(
        card["name"],
        card["type"],
        card["cost"],
        card["vp"],
        card["expansion"],
        card["expansion_number"],
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
