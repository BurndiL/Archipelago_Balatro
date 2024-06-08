
from BaseClasses import Item

from typing import Dict, NamedTuple

class ItemData(NamedTuple):
    code: int

class BalatroItem(Item):
    game: str = "Balatro"

offset = 12345

# add other trash items like get money for current run or permanently increase
# hand size, many good ideas to have here!
# maybe also traps? for example discard two random cards if collected
item_table: Dict[str, ItemData] = {
    # deck unlocks
    "Red Deck"       : ItemData(offset + 1),
    "Blue Deck"      : ItemData(offset + 2),
    "Yellow Deck"    : ItemData(offset + 3),
    "Green Deck"     : ItemData(offset + 4),
    "Black Deck"     : ItemData(offset + 5),
    "Magic Deck"     : ItemData(offset + 6),
    "Nebula Deck"    : ItemData(offset + 7),
    "Ghost Deck"     : ItemData(offset + 8),
    "Abandoned Deck" : ItemData(offset + 9),
    "Checkered Deck" : ItemData(offset + 10),
    "Zodiac Deck"    : ItemData(offset + 11),
    "Painted Deck"   : ItemData(offset + 12),
    "Anaglyph Deck"  : ItemData(offset + 13),
    "Plasma Deck"    : ItemData(offset + 14),
    "Erratic Deck"   : ItemData(offset + 15),
    "Filler Item"    : ItemData(offset + 16)
}

# this might not be smart, maybe check for id range instead
def is_progression(item_name: str) -> bool:
    return item_name.endswith("Deck")

#add implementation here mayhaps
def is_useful(item_name: str) -> bool:
    return True



item_id_to_name: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}

def item_to_unlock_event(item_name: str) -> Dict[str, str]:
    message = f"{item_name} Acquired!"
    action = ""
    payload = ""
    if item_name.endswith("Deck"):
        action = "UNLOCK_DECK"
        payload = str(item_table[item_name])

    return {
        "message": message,
        "action": action,
        "payload": payload,
    }