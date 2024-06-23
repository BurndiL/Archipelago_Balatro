from .BalatroDecks import deck_id_to_name
from BaseClasses import Location
from .Options import BalatroOptions

# ask what the fuck to put here lol
offset = 5606_000

class BalatroLocation(Location):
    game: str = "Balatro"


balatro_location_name_to_id = dict()
balatro_location_id_to_name = dict()
balatro_location_id_to_stake = dict()

prev_id = offset

# deck locations

for deck in deck_id_to_name:
    for ante in range(8):
        for stake in range(8):
            location_name = deck_id_to_name[deck] + " Ante " + str(ante+1) + " Stake " + str(stake + 1)
            location_id = prev_id
            prev_id += 1
            balatro_location_name_to_id[location_name] = location_id
            balatro_location_id_to_name[location_id] = location_name
            balatro_location_id_to_stake[location_id] = stake + 1

def create_shop_locations(amount) -> dict:
    # shop locations
    prev_id = len(balatro_location_name_to_id)
    ret = dict()
    for i in range(amount):
        
        prev_id += 1
        location_name = "Shop Item " + str(i+1)
        location_id = prev_id

        ret[location_id] = location_name
        balatro_location_name_to_id[location_name] = location_id
        balatro_location_id_to_name[location_id] = location_name
        
    return ret


