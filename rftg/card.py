TYPE_WORLD = 1
TYPE_DEVELOPMENT = 2


class Card:
    def __init__(self, name, type, cost, vp, expansion, flags, extra_victory):
        self.name = name
        self.type = type
        self.cost = cost
        self.vp = vp
        self.expansion = expansion
        self.flags = flags
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
        elif "F" == line[:1]:
            for item in line[2:].split("|"):
                card["flags"].append(item.strip())
        elif "V" == line[:1]:
            card["extra_victory"].append(line[2:])
    return Card(
        card["name"],
        card["type"],
        card["cost"],
        card["vp"],
        card["expansion"],
        card["flags"],
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
