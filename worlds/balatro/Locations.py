from .BalatroDecks import deck_id_to_name
from BaseClasses import Location

max_shop_items = 150

# ask what the fuck to put here lol
offset = 5606_000

class BalatroLocation(Location):
    game: str = "Balatro"


balatro_location_name_to_id = dict()
balatro_location_id_to_name = dict()
balatro_location_id_to_stake = dict()
balatro_location_id_to_ante = dict()

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
            balatro_location_id_to_ante[location_id] = ante + 1
            
# Shop Locations. Generate the maximum amount of locations but not 
# all of them will be included in the world
shop_id_offset = prev_id+1

for j in range(8):
    for i in range(max_shop_items):
        
        prev_id += 1
        
        location_name = "Shop Item " + str(i+1) + " at Stake "+ str(j+1)
        location_id = prev_id
        
        balatro_location_name_to_id[location_name] = location_id
        balatro_location_id_to_name[location_id] = location_name
        

