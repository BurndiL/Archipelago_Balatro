import typing

from typing import Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, ItemData, BalatroItem, is_progression, is_useful
from .BalatroDecks import deck_id_to_name
# from .Options import BalatroOptions
from .Locations import BalatroLocation, balatro_location_id_to_name, balatro_location_name_to_id
# from .Options import BalatroOptions

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

    # options_dataclass = BalatroOptions
    # options: BalatroOptions

    
    itempool: Dict[str, int]

    def create_items(self):
        self.itempool = []
        # add option handling here later
        for item_name in item_table:

            #option handling goes here (once its added)
            classification = ItemClassification.filler 
            if is_progression(item_name):
                classification = ItemClassification.progression
            else: 
                if (is_useful(item_name)):
                    classification = ItemClassification.progression
                
            self.itempool.append(self.create_item(item_name, classification))
            

        pool_count = len(balatro_location_name_to_id)

        #if theres any free space fill it with filler, for example traps 
        while len(self.itempool) < pool_count:
            self.itempool.append(self.create_item("Filler Item", ItemClassification.filler))

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
            deck_locations : Dict[str, int] = {}

            for location in balatro_location_name_to_id:
                if str(location).startswith(deck_id_to_name[deck]):
                    deck_locations[location] = balatro_location_name_to_id[location]
                    # print("Added Location " + location + " to region " + deck_region.name )

            deck_region.add_locations(deck_locations, BalatroLocation)
            # has to have deck collected to access it
            menu_region.connect(deck_region, None, lambda state: state.has(deck_id_to_name[deck], self.player))
            

