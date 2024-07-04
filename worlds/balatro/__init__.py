import typing

from typing import Any, Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, is_joker, jokers, offset, ItemData, BalatroItem, \
    is_deck, is_progression, is_useful, tarots, planets, vouchers, spectrals
from .BalatroDecks import deck_id_to_name
import random
from worlds.generic.Rules import add_rule
from .Options import BalatroOptions, Traps
from .Locations import BalatroLocation, balatro_location_id_to_name, balatro_location_name_to_id, \
    balatro_location_id_to_stake, shop_id_offset, balatro_location_id_to_ante, max_shop_items


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
            if is_progression(item_name):
                classification = ItemClassification.progression
            elif is_useful(item_name):
                classification = ItemClassification.useful

            if not item_name in excludedItems and \
                classification == ItemClassification.progression or \
                classification == ItemClassification.useful:
                    
                # fix typo from base game
                joker_Filler = item_name
                if joker_Filler == "Caino":
                    joker_Filler = "Canio"
                
                if joker_Filler.upper() in [name.upper() for name in self.options.filler_jokers.value]:
                    classification = ItemClassification.filler
                    
                # print(item_name + " with class: " + str(classification)) 
                self.itempool.append(self.create_item(item_name, classification))
            # else: 
            # print("Excluded Item: " + item_name)

        pool_count = self.locations_set

        # if there's any free space fill it with filler, for example traps
        counter = 0
        trap_amount = -1
        if self.options.trap_amount == Traps.option_no_traps:
            trap_amount = -1
        elif (self.options.trap_amount == Traps.option_low_amount):
            trap_amount = 15
        elif (self.options.trap_amount == Traps.option_medium_amount):
            trap_amount = 7
        elif (self.options.trap_amount == Traps.option_high_amount):
            trap_amount = 2
        elif (self.options.trap_amount == Traps.option_mayhem):
            trap_amount = 1

        op_filler_max = self.options.permanent_filler.value
        op_filler = 1

        while len(self.itempool) < pool_count:
            counter += 1

            if (trap_amount != -1 and counter % trap_amount == 0):
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
        print("class: " + str(classification) + " for item: " + item_name)
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
                    ante = balatro_location_id_to_ante[location_id]

                    new_location = BalatroLocation(self.player, location, location_id, deck_region)

                    new_location.progress_type = LocationProgressType.DEFAULT
                    
                    # to make life easier for players require some jokers to be found to beat ante 4 and up!
                    if ante > 4:
                        add_rule(new_location, lambda state, _ante_ = ante: 
                        state.has_from_list(list(jokers.values()), self.player, 8 + _ante_ * 2) )
                    
                    # limit later stakes to "require" jokers so progression is distributed better
                    add_rule(new_location, lambda state, _stake_ = stake: 
                        state.has_from_list(list(jokers.values()), self.player, (_stake_ - 1) * 12) and
                        state.has_from_list(list(tarots.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(spectrals.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(planets.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(vouchers.values()), self.player, (_stake_ - 1) * 1))

                    if stake <= self.options.include_stakes:
                        self.locations_set += 1
                        deck_region.locations.append(new_location)

                        
            self.multiworld.regions.append(deck_region)
            # has to have deck collected to access it
            # print(deck_name)
            menu_region.connect(deck_region, None,
                                lambda state, _deck_name_ = deck_name: state.has(_deck_name_, self.player))

        # Shop Region
        
        for location in balatro_location_name_to_id:
            if str(location).startswith("Shop Item"):
                self.shop_locations[balatro_location_name_to_id[location]] = location

        for i in range(self.options.include_stakes.value):
            stake = i + 1
            shop_region = Region("Shop Stake " + str(stake), self.player, self.multiworld)
            id_offset = shop_id_offset + i*max_shop_items
            
            for j in range(self.options.shop_items.value):
                location_name = self.shop_locations[id_offset + j]
                location_id = id_offset + j
                new_location = BalatroLocation(self.player, location_name, location_id, shop_region)

                new_location.progress_type = LocationProgressType.DEFAULT
                
                # balance out shop items a bit
                add_rule(new_location, lambda state, _require_ = j / 3: 
                state.has_from_list(list(jokers.values()), self.player, _require_))
                
                shop_region.locations.append(new_location)
                self.locations_set += 1
                
            self.multiworld.regions.append(shop_region)
            menu_region.connect(shop_region, rule = lambda state, _stake_ = stake: state.has_from_list(list(jokers.values()),
                            self.player,
                            (_stake_ - 1) * 12) and
                        state.has_from_list(list(tarots.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(spectrals.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(planets.values()), self.player, (_stake_ - 1) * 2) and
                        state.has_from_list(list(vouchers.values()), self.player, (_stake_ - 1) * 1) and
                        state.has_any(list(deck_id_to_name.values()), self.player))
            
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
        min_price = self.options.minimum_price.value
        max_price = self.options.maximum_price.value
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        
        base_data = {
            "goal": self.options.goal.value,
            "ante_win_goal": self.options.ante_win_goal.value,
            "decks_win_goal": self.options.decks_win_goal.value,
            "jokers_unlock_goal": self.options.jokers_unlock_goal.value,
            "stake1_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 1")],
            "stake2_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 2")],
            "stake3_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 3")],
            "stake4_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 4")],
            "stake5_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 5")],
            "stake6_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 6")],
            "stake7_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 7")],
            "stake8_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__("Stake 8")],
            "minimum_price": min_price,
            "maximum_price": max_price,
            "deathlink": bool(self.options.deathlink)
        }
        return base_data
