import typing

from typing import Any, Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, offset, ItemData, BalatroItem, is_deck, is_useful
from .BalatroDecks import deck_id_to_name
import random
from .Options import BalatroOptions
from .Locations import BalatroLocation, balatro_location_id_to_name, balatro_location_name_to_id, balatro_location_id_to_stake

class BalatroWebWorld(WebWorld):
    setup_en = Tutorial(

        # TODO: actually do this lmao (help)
        "Multiworld Setup Guide",
        "A guide to setting up Balatro on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Burndi"]
    )


class BalatroWorld(World):
    """
    Balatro is a (insert description about Balatro here).
    """
    game = "Balatro"
    web = BalatroWebWorld()

    #dont know what this does yet
    topology_present = False

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name
    
    location_id_to_name = balatro_location_id_to_name
    location_name_to_id = balatro_location_name_to_id

    options_dataclass = BalatroOptions
    options: BalatroOptions

    
    itempool: Dict[str, int]

    def create_items(self):

        decks_to_unlock = self.options.decks_unlocked 
        excludedItems : Dict[str, ItemData] = {}
        if decks_to_unlock > 0:
            # get all decks
            deck_table : Dict[str, ItemData] = {}
            for item in item_table:
                if is_deck(item): 
                    deck_table[item] = item_table[item]

            deck_table = list(deck_table.items())
            while decks_to_unlock > 0:
                deck = random.choice(deck_table)
                deck_name = deck[0]
                deck_data = deck[1]
                self.multiworld.precollected_items[self.player].append(self.create_item(deck_name, ItemClassification.progression))
                deck_table.remove(deck)
                print("start with this item: " + deck_name)
                excludedItems[deck_name] = deck_data
                decks_to_unlock-=1



        self.itempool = []
        # add option handling here later
        for item_name in item_table:

            #option handling goes here (once its added)
            classification = ItemClassification.filler 
            if is_deck(item_name):
                classification = ItemClassification.progression
            else: 
                if (is_useful(item_name)):
                    classification = ItemClassification.progression
                
            if not item_name in excludedItems: 
                self.itempool.append(self.create_item(item_name, classification))
            else: 
                print("Excluded Item: " + item_name) 
            

        pool_count = len(balatro_location_name_to_id)

        #if theres any free space fill it with filler, for example traps 
        # this code needs to be largely overhauled, dont care rn tho
        counter = 0
        while len(self.itempool) < pool_count:
            counter += 1
            # just make every fifth filler a trap
            if (counter % 5):
                trap_id = random.randint(220,222) 
                self.itempool.append(self.create_item(item_id_to_name[trap_id + offset], ItemClassification.trap))
            else:
                filler_id = random.randint(200,205) 
                # every second filler should be bonus money
                if (counter % 2): 
                    filler_id = 201
                    
                self.itempool.append(self.create_item(item_id_to_name[filler_id + offset], ItemClassification.filler))

        self.multiworld.itempool += self.itempool


    def create_item(self, item: Union[str, ItemData], classification: ItemClassification = None) -> BalatroItem:
        item_name = ""
        if isinstance(item, str):
            item_name = item
            item = item_table[item]
        else: 
            item_name = item_table[item]

        if classification is None:
            classification = item.classification
        return BalatroItem(item_name, classification, item.code, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        for deck in deck_id_to_name:
            deck_region = Region(deck_id_to_name[deck], self.player, self.multiworld)

            for location in balatro_location_name_to_id:
                if str(location).startswith(deck_id_to_name[deck]):
                    location_id = balatro_location_name_to_id[location]
                    ante = balatro_location_id_to_stake[location_id]

                    new_location = BalatroLocation(self.player, location, location_id, deck_region)

                    new_location.progress_type = LocationProgressType.DEFAULT
                    
                    if ante > self.options.include_stakes:
                        new_location.progress_type = LocationProgressType.EXCLUDED

                    deck_region.locations.append(new_location)
                    

            # has to have deck collected to access it
            menu_region.connect(deck_region, None, lambda state: state.has(deck_id_to_name[deck], self.player))
            

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()
    
    def fill_json_data(self) -> Dict[str, Any]:
        base_data = {
            "goal": self.options.goal.value,
            "ante_win_goal": self.options.ante_win_goal.value,
            "decks_win_goal": self.options.decks_win_goal.value,
            "jokers_unlock_goal": self.options.jokers_unlock_goal.value,
            "deathlink": bool(self.options.deathlink)
        }
        return base_data
    
