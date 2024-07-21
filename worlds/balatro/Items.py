
from BaseClasses import Item

from typing import Dict, NamedTuple

class ItemData(NamedTuple):
    code: int

class BalatroItem(Item):
    game: str = "Balatro"

offset = 5606_000

# important when adding new items: Do not make any items end with ".. Deck" because that will fuck the item logic
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

    #Jokers
    "Joker": ItemData(offset + 16),
    "Greedy Joker": ItemData(offset + 17),
    "Lusty Joker": ItemData(offset + 18),
    "Wrathful Joker": ItemData(offset + 19),
    "Gluttonous Joker": ItemData(offset + 20),
    "Jolly Joker": ItemData(offset + 21),
    "Zany Joker": ItemData(offset + 22),
    "Mad Joker": ItemData(offset + 23),
    "Crazy Joker": ItemData(offset + 24),
    "Droll Joker": ItemData(offset + 25),
    "Sly Joker": ItemData(offset + 26),
    "Wily Joker": ItemData(offset + 27),
    "Clever Joker": ItemData(offset + 28),
    "Devious Joker": ItemData(offset + 29),
    "Crafty Joker": ItemData(offset + 30),
    "Half Joker": ItemData(offset + 31),
    "Joker Stencil": ItemData(offset + 32),
    "Four Fingers": ItemData(offset + 33),
    "Mime": ItemData(offset + 34),
    "Credit Card": ItemData(offset + 35),
    "Ceremonial Dagger": ItemData(offset + 36),
    "Banner": ItemData(offset + 37),
    "Mystic Summit": ItemData(offset + 38),
    "Marble Joker": ItemData(offset + 39),
    "Loyalty Card": ItemData(offset + 40),
    "8 Ball": ItemData(offset + 41),
    "Misprint": ItemData(offset + 42),
    "Dusk": ItemData(offset + 43),
    "Raised Fist": ItemData(offset + 44),
    "Chaos the Clown": ItemData(offset + 45),
    "Fibonacci": ItemData(offset + 46),
    "Steel Joker": ItemData(offset + 47),
    "Scary Face": ItemData(offset + 48),
    "Abstract Joker": ItemData(offset + 49),
    "Delayed Gratification": ItemData(offset + 50),
    "Hack": ItemData(offset + 51),
    "Pareidolia": ItemData(offset + 52),
    "Gros Michel": ItemData(offset + 53),
    "Even Steven": ItemData(offset + 54),
    "Odd Todd": ItemData(offset + 55),
    "Scholar": ItemData(offset + 56),
    "Business Card": ItemData(offset + 57),
    "Supernova": ItemData(offset + 58),
    "Ride the Bus": ItemData(offset + 59),
    "Space Joker": ItemData(offset + 60),
    'Egg': ItemData(offset + 61),
    'Burglar': ItemData(offset + 62),
    'Blackboard': ItemData(offset + 63),
    'Runner': ItemData(offset + 64),
    'Ice Cream': ItemData(offset + 65),
    'DNA': ItemData(offset + 66),
    'Splash': ItemData(offset + 67),
    'Blue Joker': ItemData(offset + 68),
    'Sixth Sense': ItemData(offset + 69),
    'Constellation': ItemData(offset + 70),
    'Hiker': ItemData(offset + 71),
    'Faceless Joker': ItemData(offset + 72),
    'Green Joker': ItemData(offset + 73),
    'Superposition': ItemData(offset + 74),
    'To Do List': ItemData(offset + 75),
    "Cavendish": ItemData(offset + 76),
    "Card Sharp": ItemData(offset + 77),
    "Red Card": ItemData(offset + 78),
    "Madness": ItemData(offset + 79),
    "Square Joker": ItemData(offset + 80),
    "Seance": ItemData(offset + 81),
    "Riff-raff": ItemData(offset + 82),
    "Vampire": ItemData(offset + 83),
    "Shortcut": ItemData(offset + 84),
    "Hologram": ItemData(offset + 85),
    "Vagabond": ItemData(offset + 86),
    "Baron": ItemData(offset + 87),
    "Cloud 9": ItemData(offset + 88),
    "Rocket": ItemData(offset + 89),
    "Obelisk": ItemData(offset + 90),
    "Midas Mask": ItemData(offset + 91),
    "Luchador": ItemData(offset + 92),
    "Photograph": ItemData(offset + 93),
    "Gift Card": ItemData(offset + 94),
    "Turtle Bean": ItemData(offset + 95),
    "Erosion": ItemData(offset + 96),
    "Reserved Parking": ItemData(offset + 97),
    "Mail-In Rebate": ItemData(offset + 98),
    "To the Moon": ItemData(offset + 99),
    "Hallucination": ItemData(offset + 100),
    "Fortune Teller": ItemData(offset + 101),
    "Juggler": ItemData(offset + 102),
    "Drunkard": ItemData(offset + 103),
    "Stone Joker": ItemData(offset + 104),
    "Golden Joker": ItemData(offset + 105),
    "Lucky Cat": ItemData(offset + 106),
    "Baseball Card": ItemData(offset + 107),
    "Bull": ItemData(offset + 108),
    "Diet Cola": ItemData(offset + 109),
    "Trading Card": ItemData(offset + 110),
    "Flash Card": ItemData(offset + 111),
    "Popcorn": ItemData(offset + 112),
    "Spare Trousers": ItemData(offset + 113),
    "Ancient Joker": ItemData(offset + 114),
    "Ramen": ItemData(offset + 115),
    "Walkie Talkie": ItemData(offset + 116),
    "Seltzer": ItemData(offset + 117),
    "Castle": ItemData(offset + 118),
    "Smiley Face": ItemData(offset + 119),
    "Campfire": ItemData(offset + 120),
    "Golden Ticket": ItemData(offset + 121),
    "Mr. Bones": ItemData(offset + 122),
    "Acrobat": ItemData(offset + 123),
    "Sock and Buskin": ItemData(offset + 124),
    "Swashbuckler": ItemData(offset + 125),
    "Troubadour": ItemData(offset + 126),
    "Certificate": ItemData(offset + 127),
    "Smeared Joker": ItemData(offset + 128),
    "Throwback": ItemData(offset + 129),
    "Hanging Chad": ItemData(offset + 130),
    "Rough Gem": ItemData(offset + 131),
    "Bloodstone": ItemData(offset + 132),
    "Arrowhead": ItemData(offset + 133),
    "Onyx Agate": ItemData(offset + 134),
    "Glass Joker": ItemData(offset + 135),
    "Showman": ItemData(offset + 136),
    "Flower Pot": ItemData(offset + 137),
    "Blueprint": ItemData(offset + 138),
    "Wee Joker": ItemData(offset + 139),
    "Merry Andy": ItemData(offset + 140),
    "Oops! All 6s": ItemData(offset + 141),
    "The Idol": ItemData(offset + 142),
    "Seeing Double": ItemData(offset + 143),
    "Matador": ItemData(offset + 144),
    "Hit the Road": ItemData(offset + 145),
    "The Duo": ItemData(offset + 146),
    "The Trio": ItemData(offset + 147),
    "The Family": ItemData(offset + 148),
    "The Order": ItemData(offset + 149),
    "The Tribe": ItemData(offset + 150),
    "Stuntman": ItemData(offset + 151),
    "Invisible Joker": ItemData(offset + 152),
    "Brainstorm": ItemData(offset + 153),
    "Satellite": ItemData(offset + 154),
    "Shoot the Moon": ItemData(offset + 155),
    "Driver's License": ItemData(offset + 156),
    "Cartomancer": ItemData(offset + 157),
    "Astronomer": ItemData(offset + 158),
    "Burnt Joker": ItemData(offset + 159),
    "Bootstraps": ItemData(offset + 160),
    "Caino": ItemData(offset + 161),
    "Triboulet": ItemData(offset + 162),
    "Yorick": ItemData(offset + 163),
    "Chicot": ItemData(offset + 164),
    "Perkeo": ItemData(offset + 165),

    # Vouchers
    "Overstock": ItemData(offset + 166),
    "Clearance Sale": ItemData(offset + 167),
    "Hone": ItemData(offset + 168),
    "Reroll Surplus": ItemData(offset + 169),
    "Crystal Ball": ItemData(offset + 170),
    "Telescope": ItemData(offset + 171),
    "Grabber": ItemData(offset + 172),
    "Wasteful": ItemData(offset + 173),
    "Tarot Merchant": ItemData(offset + 174),
    "Planet Merchant": ItemData(offset + 175),
    "Seed Money": ItemData(offset + 176),
    "Blank": ItemData(offset + 177),
    "Magic Trick": ItemData(offset + 178),
    "Hieroglyph": ItemData(offset + 179),
    "Director's Cut": ItemData(offset + 180),
    "Paint Brush": ItemData(offset + 181),
    "Overstock Plus": ItemData(offset + 182),
    "Liquidation": ItemData(offset + 183),
    "Glow Up": ItemData(offset + 184),
    "Reroll Glut": ItemData(offset + 185),
    "Omen Globe": ItemData(offset + 186),
    "Observatory": ItemData(offset + 187),
    "Nacho Tong": ItemData(offset + 188),
    "Recyclomancy": ItemData(offset + 189),
    "Tarot Tycoon": ItemData(offset + 190),
    "Planet Tycoon": ItemData(offset + 191),
    "Money Tree": ItemData(offset + 192),
    "Antimatter": ItemData(offset + 193),
    "Illusion": ItemData(offset + 194),
    "Petroglyph": ItemData(offset + 195),
    "Retcon": ItemData(offset + 196),
    "Palette": ItemData(offset + 197),

    # Booster Packs

    "Arcana Pack": ItemData(offset + 198),
    "Jumbo Arcana Pack": ItemData(offset + 199),
    "Mega Arcana Pack": ItemData(offset + 200),
    "Celestial Pack": ItemData(offset + 201),
    "Jumbo Celestial Pack": ItemData(offset + 202),
    "Mega Celestial Pack": ItemData(offset + 203),
    "Spectral Pack": ItemData(offset + 204),
    "Jumbo Spectral Pack": ItemData(offset + 205),
    "Mega Spectral Pack": ItemData(offset + 206),
    "Standard Pack": ItemData(offset + 207),
    "Jumbo Standard Pack": ItemData(offset + 208),
    "Mega Standard Pack": ItemData(offset + 209),
    "Buffoon Pack": ItemData(offset + 210),
    "Jumbo Buffoon Pack": ItemData(offset + 211),
    "Mega Buffoon Pack": ItemData(offset + 212),
    
    # Tarot Cards

    "The Fool": ItemData(offset + 213),
    "The Magician": ItemData(offset + 214),
    "The High Priestess": ItemData(offset + 215),
    "The Empress": ItemData(offset + 216),
    "The Emperor": ItemData(offset + 217),
    "The Hierophant": ItemData(offset + 218),
    "The Lovers": ItemData(offset + 219),
    "The Chariot": ItemData(offset + 220),
    "Justice": ItemData(offset + 221),
    "The Hermit": ItemData(offset + 222),
    "The Wheel of Fortune": ItemData(offset + 223),
    "Strength": ItemData(offset + 224),
    "The Hanged Man": ItemData(offset + 225),
    "Death": ItemData(offset + 226),
    "Temperance": ItemData(offset + 227),
    "The Devil": ItemData(offset + 228),
    "The Tower": ItemData(offset + 229),
    "The Star": ItemData(offset + 230),
    "The Moon": ItemData(offset + 231),
    "The Sun": ItemData(offset + 232),
    "Judgement": ItemData(offset + 233),
    "The World": ItemData(offset + 234),

    # Planet Cards

    "Mercury": ItemData(offset + 235),
    "Venus": ItemData(offset + 236),
    "Earth": ItemData(offset + 237),
    "Mars": ItemData(offset + 238),
    "Jupiter": ItemData(offset + 239),
    "Saturn": ItemData(offset + 240),
    "Uranus": ItemData(offset + 241),
    "Neptune": ItemData(offset + 242),
    "Pluto": ItemData(offset + 243),
    "Planet X": ItemData(offset + 244),
    "Ceres": ItemData(offset + 245),
    "Eris": ItemData(offset + 246),

    # Spectral Cards

    "Familiar": ItemData(offset + 247),
    "Grim": ItemData(offset + 248),
    "Incantation": ItemData(offset + 249),
    "Talisman": ItemData(offset + 250),
    "Aura": ItemData(offset + 251),
    "Wraith": ItemData(offset + 252),
    "Sigil": ItemData(offset + 253),
    "Ouija": ItemData(offset + 254),
    "Ectoplasm": ItemData(offset + 255),
    "Immolate": ItemData(offset + 256),
    "Ankh": ItemData(offset + 257),
    "Deja Vu": ItemData(offset + 258),
    "Hex": ItemData(offset + 259),
    "Trance": ItemData(offset + 260),
    "Medium": ItemData(offset + 261),
    "Cryptid": ItemData(offset + 262),
    "The Soul": ItemData(offset + 263),
    "Black Hole": ItemData(offset + 264),

    # OP Filler Bonus Items
    "Bonus Discards": ItemData(offset + 301),
    "Bonus Starting Money" : ItemData(offset + 302),
    "Bonus Hands"    : ItemData(offset + 303),
    "Bonus Hand Size"    : ItemData(offset + 304),
    "Bonus Max Interest" : ItemData(offset + 305),
    "Bonus Joker Slot" : ItemData(offset + 306),
    "Bonus Consumable Slot" : ItemData(offset + 307),
    
    # Filler Bonus Items
    "Bonus Money": ItemData(offset + 310),
    "Receive Buffoon Pack" : ItemData(offset + 311),
    "Receive Consumable Pack" : ItemData(offset + 312),
    "Plus 3 Hand Size Next Round" : ItemData(offset + 313),
    "Rerolls Start At $0 Next Shop" : ItemData(offset + 314),
    "Free uncommon joker next shop" : ItemData(offset + 315),
    "Free rare joker next shop" : ItemData(offset + 316),
    "Free negative joker next shop" : ItemData(offset + 317),
    "Free foil joker next shop" : ItemData(offset + 318),
    "Free holographic joker next shop" : ItemData(offset + 319),
    "Free polychrome joker next shop" : ItemData(offset + 320),
    "Receive double tag" : ItemData(offset + 321),

    # Traps 
    "Lose All Money" : ItemData(offset + 330),
    "Lose Discard" : ItemData(offset + 331),
    "Lose Hand" : ItemData(offset + 332),
    "Make Random Joker Perishable" : ItemData(offset + 333),
    "Make Random Joker Eternal" : ItemData(offset + 334),
    "Make Random Joker Rental" : ItemData(offset + 335),
    
    # Joker Bundle (for short mode)
    "Joker Bundle 1" : ItemData(offset + 351),
    "Joker Bundle 2" : ItemData(offset + 352),
    "Joker Bundle 3" : ItemData(offset + 353),
    "Joker Bundle 4" : ItemData(offset + 354),
    "Joker Bundle 5" : ItemData(offset + 355),
    "Joker Bundle 6" : ItemData(offset + 356),
    "Joker Bundle 7" : ItemData(offset + 357),
    "Joker Bundle 8" : ItemData(offset + 358),
    "Joker Bundle 9" : ItemData(offset + 359),
    "Joker Bundle 10" : ItemData(offset + 360),
    "Joker Bundle 11" : ItemData(offset + 361),
    "Joker Bundle 12" : ItemData(offset + 362),
    "Joker Bundle 13" : ItemData(offset + 363),
    "Joker Bundle 14" : ItemData(offset + 364),
    "Joker Bundle 15" : ItemData(offset + 365),
    
    # Consumable Bundles
    "Tarot Bundle" : ItemData(offset + 371),
    "Planet Bundle" : ItemData(offset + 372),
    "Spectral Bundle" : ItemData(offset + 373),
    
    # Stakes as Items
    "White Stake" : ItemData(offset + 390),
    "Red Stake" : ItemData(offset + 391),
    "Green Stake" : ItemData(offset + 392),
    "Black Stake" : ItemData(offset + 393),
    "Blue Stake" : ItemData(offset + 394),
    "Purple Stake" : ItemData(offset + 395),
    "Orange Stake" : ItemData(offset + 396),
    "Gold Stake" : ItemData(offset + 397),   
}

stake_to_number: Dict[str, int] = {
    "White Stake" : 1,
    "Red Stake" : 2, 
    "Green Stake" : 3, 
    "Black Stake" : 4, 
    "Blue Stake" : 5, 
    "Purple Stake" : 6, 
    "Orange Stake" : 7, 
    "Gold Stake" : 8
}

number_to_stake: Dict[int, str] = {
    1 : "White Stake",
    2 : "Red Stake", 
    3: "Green Stake", 
    4: "Black Stake" , 
    5: "Blue Stake" , 
    6: "Purple Stake" , 
    7: "Orange Stake" , 
    8: "Gold Stake"
}

def is_deck(item_name: str) -> bool:
    return item_name.endswith("Deck")

decks: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_deck(item_name)
}

prev_id = 400
for deck in decks.values():
    for stake in [key for key, _ in stake_to_number.items()]:
        item_table[str(deck) + " " + str(stake)] = ItemData(offset + prev_id)
        prev_id += 1


def is_joker(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 16 and item_id <= 165)

def is_voucher(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 166 and item_id <= 197)

def is_booster(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 198 and item_id <= 212)

def is_tarot(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 213 and item_id <= 234)

def is_planet(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 235 and item_id <= 246)

def is_spectral(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 247 and item_id <= 264)

def is_bundle(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 351 and item_id <= 373)

def is_joker_bundle(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 351 and item_id <= 365)

def is_stake(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 390 and item_id <= 397)

def is_stake_per_deck(item_name: str) -> bool:
    item_id = item_name_to_id[item_name] - offset
    return (item_id >= 400 and item_id <= 520)



def is_progression(item_name: str) -> bool:
    return (is_deck(item_name) or 
            is_joker(item_name) or 
            is_tarot(item_name) or 
            is_voucher(item_name) or 
            is_planet(item_name) or 
            is_spectral(item_name) or 
            is_stake(item_name) or
            is_stake_per_deck(item_name) or
            is_booster(item_name)
    )

def is_useful(item_name: str) -> bool:
    return False # maybe we will find a useful items in the future

item_id_to_name: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

item_name_to_id: Dict[str, int] = {
    item_name: data.code for item_name, data in item_table.items() if data.code
}


jokers: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_joker(item_name)
}

vouchers: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_voucher(item_name)
}

planets: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_planet(item_name)
}

spectrals: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_spectral(item_name)
}

tarots: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_tarot(item_name)
}

joker_bundles: Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code and is_joker_bundle(item_name)
}