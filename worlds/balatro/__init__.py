import typing

from typing import Any, Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, is_joker, jokers, offset, ItemData, BalatroItem, \
    is_deck, is_useful
from .BalatroDecks import deck_id_to_name
import random
from .Options import BalatroOptions
from .Locations import BalatroLocation, balatro_location_id_to_name, balatro_location_name_to_id, \
    balatro_location_id_to_stake


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

    # don't know what this does yet
    topology_present = False

    options_dataclass = BalatroOptions
    options: BalatroOptions

    locations_set = 0
    shop_locations = dict()

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = balatro_location_id_to_name
    location_name_to_id = balatro_location_name_to_id

    itempool: Dict[str, int]

    def create_items(self):

        decks_to_unlock = self.options.decks_unlocked_from_start
        excludedItems: Dict[str, ItemData] = {}
        if decks_to_unlock > 0:
            # get all decks
            deck_table: Dict[str, ItemData] = {}
            for item in item_table:
                if is_deck(item):
                    deck_table[item] = item_table[item]

            deck_table = list(deck_table.items())
            while decks_to_unlock > 0:
                deck = random.choice(deck_table)
                deck_name = deck[0]
                deck_data = deck[1]
                preCollected_item = self.create_item(deck_name, ItemClassification.progression)
                self.multiworld.push_precollected(preCollected_item)
                deck_table.remove(deck)
                # print("start with this item: " + deck_name)
                excludedItems[deck_name] = deck_data
                decks_to_unlock -= 1

        self.itempool = []
        for item_name in item_table:

            classification = ItemClassification.filler
            if is_deck(item_name) or (self.options.goal == "unlock_jokers" and is_joker(item_name)):
                classification = ItemClassification.progression
            else:
                if (is_useful(item_name) and not (item_name in self.options.filler_jokers)):
                    classification = ItemClassification.useful

            if not item_name in excludedItems:
                # print(item_name + " with class: " + str(classification)) 
                self.itempool.append(self.create_item(item_name, classification))
            # else: 
            # print("Excluded Item: " + item_name)

        pool_count = self.locations_set

        # if there's any free space fill it with filler, for example traps
        counter = 0
        trap_amount = 5
        if self.options.trap_amount.option_no_traps:
            trap_amount = 10000
        elif (self.options.trap_amount.option_low_amount):
            trap_amount = 15
        elif (self.options.trap_amount.option_medium_amount):
            trap_amount = 7
        elif (self.options.trap_amount.option_high_amount):
            trap_amount = 2
        elif (self.options.trap_amount.option_mayhem):
            trap_amount = 1


        op_filler_max = 3
        op_filler = 1

        while len(self.itempool) < pool_count:
            counter += 1

            if (counter % trap_amount == 0):
                trap_id = random.randint(320, 325)
                self.itempool.append(self.create_item(item_id_to_name[trap_id + offset], ItemClassification.trap))
            else:
                filler_id = 310
                if op_filler_max > 0:
                    filler_id = op_filler + 300
                    op_filler += 1
                    if op_filler == 8:
                        op_filler = 1
                        op_filler_max -= 1
                    
                # after all good filler items are placed, fill the rest with normal filler items
                else:
                    filler_id = random.randint(310, 314)

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
            classification = ItemClassification.filler

        return BalatroItem(item_name, classification, item.code, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        self.multiworld.regions.append(menu_region)

        for deck in deck_id_to_name:
            deck_name = deck_id_to_name[deck]
            # print(deck_name)

            deck_region = Region(deck_name, self.player, self.multiworld)
            for location in balatro_location_name_to_id:
                if str(location).startswith(deck_name):
                    location_id = balatro_location_name_to_id[location]
                    stake = balatro_location_id_to_stake[location_id]

                    new_location = BalatroLocation(self.player, location, location_id, deck_region)

                    new_location.progress_type = LocationProgressType.DEFAULT

                    if stake <= self.options.include_stakes:
                        self.locations_set += 1
                        deck_region.locations.append(new_location)

            self.multiworld.regions.append(deck_region)
            # has to have deck collected to access it
            # print(deck_name)
            menu_region.connect(deck_region, None,
                                lambda state: state.has(deck_name, self.player))

        # Shop Region
        
        for location in balatro_location_name_to_id:
            if str(location).startswith("Shop Item"):
                self.shop_locations[balatro_location_name_to_id[location]] = location

        shop_region = Region("Shop", self.player, self.multiworld)

        counter = 0
        for location in self.shop_locations:
            counter += 1
            new_location = BalatroLocation(self.player, str(self.shop_locations[location]), location, shop_region)

            new_location.progress_type = LocationProgressType.DEFAULT
            if (counter <= self.options.shop_items):
                self.locations_set += 1
                shop_region.locations.append(new_location)

        self.multiworld.regions.append(shop_region)
        menu_region.connect(shop_region, None, lambda state: state.has_any(list(deck_id_to_name.values()), self.player))

        if self.options.goal == "beat_decks":
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(
                list(deck_id_to_name.values()), self.player, self.options.decks_win_goal.value)
        elif self.options.goal == "unlock_jokers":
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(list(jokers.values()),
                                                                                                  self.player,
                                                                                                  self.options.jokers_unlock_goal.value)
        elif self.options.goal == "beat_ante":
            self.multiworld.completion_condition[self.player] = lambda state: state.has_any(
                list(deck_id_to_name.values()), self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()

    def fill_json_data(self) -> Dict[str, Any]:
        base_data = {
            "goal": self.options.goal.value,
            "ante_win_goal": self.options.ante_win_goal.value,
            "decks_win_goal": self.options.decks_win_goal.value,
            "jokers_unlock_goal": self.options.jokers_unlock_goal.value,
            "shop_locations": [key for key, _ in self.shop_locations.items()],
            "minimum_price": self.options.minimum_price.value,
            "maximum_price": self.options.maximum_price.value,
            "deathlink": bool(self.options.deathlink)
        }
        return base_data
