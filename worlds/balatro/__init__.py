import typing

from typing import Any, Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, is_joker, is_joker_bundle, jokers, decks, joker_bundles, offset, ItemData, BalatroItem, \
    is_deck, is_progression, is_useful, is_bundle, tarots, planets, vouchers, spectrals, is_voucher, is_booster, is_stake, is_stake_per_deck, \
        stake_to_number, number_to_stake, is_tarot, is_planet, is_spectral
from .BalatroDecks import deck_id_to_name, deck_name_to_key
import random, math
from worlds.generic.Rules import add_rule
from .Options import BalatroOptions, Traps, IncludeDecksMode, StakeUnlockMode, \
    IncludeStakesMode
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
    
    playable_decks = [value for _, value in deck_id_to_name.items()]
    playable_stakes = list([value for _, value in number_to_stake.items()])
    required_stake = "White Stake"

    short_mode_pool = list(jokers.keys())
    random.shuffle(short_mode_pool)    
    
    itempool: Dict[str, int]
    
    def generate_early(self):
        # decks
        if self.options.include_decksMode.value == IncludeDecksMode.option_all:
            self.playable_decks = [value for _, value in deck_id_to_name.items()]
        elif self.options.include_decksMode.value == IncludeDecksMode.option_number:
            playable_deck_choice = list([value for key, value in deck_id_to_name.items()])
            random.shuffle(playable_deck_choice)
            self.playable_decks = playable_deck_choice[0:self.options.include_deckNumber.value]
        elif self.options.include_decksMode.value == IncludeDecksMode.option_choose:
            self.playable_decks = self.options.include_deckChoice.value
            
            
        # stakes
        if self.options.include_stakesMode == IncludeStakesMode.option_all:
            self.playable_stakes = [value for _, value in number_to_stake.items()]
            random.shuffle(self.playable_stakes)
        elif self.options.include_stakesMode == IncludeStakesMode.option_number:
            playable_stake_choice = list([value for key, value in number_to_stake.items()])
            random.shuffle(playable_stake_choice)
            self.playable_stakes = playable_stake_choice[0:self.options.include_stakesNumber.value]
        elif self.options.include_stakesMode == IncludeStakesMode.option_choose:
            self.playable_stakes = list(self.options.include_stakesList.value)
        
        
        if list(self.options.required_stake_for_goal.value)[0] in self.playable_stakes:
            self.required_stake = list(self.options.required_stake_for_goal.value)[0]
        else:
            self.required_stake = self.playable_stakes[0]
            
        self.options.decks_win_goal.value = min(self.options.decks_win_goal.value, len(self.playable_decks))

    def create_items(self):
        decks_to_unlock = self.options.decks_unlocked_from_start.value
                    
        if decks_to_unlock > len(self.playable_decks):
            decks_to_unlock = len(self.playable_decks)
        
        excludedItems: Dict[str, ItemData] = {}
        if decks_to_unlock > 0:
            # unlock first stake
            if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item:
                stake_name = random.choice(self.playable_stakes)
                stake_data = item_table[stake_name]
                excludedItems[stake_name] = stake_data
                preCollected_item = self.create_item(stake_name, ItemClassification.progression)
                self.multiworld.push_precollected(preCollected_item)
                
            # get all decks
            deck_table: Dict[str, ItemData] = {}
            for item in item_table:
                if is_deck(item) and (item in self.playable_decks):
                    deck_table[item] = item_table[item]

            deck_table = list(deck_table.items())
            while decks_to_unlock > 0:
                deck = random.choice(deck_table)
                deck_name = deck[0]
                deck_data = deck[1]
                if self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item_per_deck:
                    preCollected_item = self.create_item(deck_name, ItemClassification.progression)
                    self.multiworld.push_precollected(preCollected_item)
                    excludedItems[deck_name] = deck_data
                deck_table.remove(deck)
                decks_to_unlock -= 1
                
                if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck:
                    stake_name = deck_name + " " + random.choice(self.playable_stakes)
                    stake_data = item_table[stake_name]
                    preCollected_stake = self.create_item(stake_name, ItemClassification.progression)
                    self.multiworld.push_precollected(preCollected_stake)
                    excludedItems[stake_name] = stake_data

        self.itempool = []
        for item_name in item_table:

            if (is_stake(item_name) and (not self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item or not item_name in self.playable_stakes)):
                continue
            if (is_stake_per_deck(item_name) and (not self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck or 
                                                  (not item_name.split()[-2] + " " + item_name.split()[-1] in self.playable_stakes or 
                                                   not item_name.split()[0] + " " + item_name.split()[1] in self.playable_decks))):
                continue
            
            if (is_deck(item_name) and self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck):
                continue
            
            if (is_deck(item_name) and not item_name in self.playable_decks):
                continue
            
            if (self.options.tarot_bundle and is_tarot(item_name)):
                continue
            if (not self.options.tarot_bundle and item_name == "Tarot Bundle"):
                continue
            
            if (self.options.planet_bundle and is_planet(item_name)):
                continue
            
            if (not self.options.planet_bundle and item_name == "Planet Bundle"):
                continue
            
            if (self.options.spectral_bundle and is_spectral(item_name)):
                continue
            
            if (not self.options.spectral_bundle and item_name == "Spectral Bundle"):
                continue         
                
            if (self.options.joker_bundles and is_joker(item_name)):
                continue
            
            if (not self.options.joker_bundles and is_joker_bundle(item_name)):
                continue     
            
            if item_name in excludedItems:
                continue    
            
            
            classification = ItemClassification.filler
            if is_progression(item_name):
                classification = ItemClassification.progression
            elif is_useful(item_name):
                classification = ItemClassification.useful

            if classification == ItemClassification.progression or classification == ItemClassification.useful:
                joker_Filler = item_name
                
                if joker_Filler.upper() in [name.upper() for name in self.options.filler_jokers.value]:
                    classification = ItemClassification.filler
                    
                self.itempool.append(self.create_item(item_name, classification))
                    
            
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
                trap_id = random.randint(330, 335)
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
                    filler_id = random.randint(310, 321)

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
            
        # print(item_name + str(classification))
        return BalatroItem(item_name, classification, item.code, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        self.multiworld.regions.append(menu_region)
        
        for deck in deck_id_to_name:
            deck_name = deck_id_to_name[deck]
            if (deck_name in self.playable_decks):
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
                            add_rule(new_location, lambda state, _ante3_ = ante: state.has_from_list(list(jokers.values()), self.player, 5 + _ante3_ * 2) or state.has_from_list(list(joker_bundles.values()), self.player, _ante3_))
                            add_rule(new_location, lambda state: state.has_from_list(list(['Buffoon Pack']), self.player, 1))
                        
                        # limit later stakes to "require" jokers so progression is distributed better
                        
                        if ante > 2:
                            add_rule(new_location, lambda state, _stake2_ = stake: 
                                (state.has_from_list(list(joker_bundles.values()), self.player, _stake2_ - 2) or
                                    state.has_from_list(list(jokers.values()), self.player, (_stake2_ - 2) * 5)) and
                                    state.has_from_list(list(vouchers.values()), self.player, _stake2_ - 2))
                            
                        if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item:
                            add_rule(new_location, lambda state, _stake_ = stake: state.has(number_to_stake[_stake_], self.player))
                        elif self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck:
                            add_rule(new_location, lambda state, _deck_name1_ = deck_name, _stake1_ = stake: state.has(_deck_name1_ + " " + number_to_stake[_stake1_], self.player))
                        
                        if stake in [stake_to_number.get(key) for key in self.playable_stakes]:
                            self.locations_set += 1
                            deck_region.locations.append(new_location)

                            
                self.multiworld.regions.append(deck_region)
                # has to have deck collected to access it
                menu_region.connect(deck_region, None,
                                lambda state, _deck_name_ = deck_name: state.has(_deck_name_, self.player) or
                                state.has_from_list(list([key for key, _ in item_table.items() if is_stake_per_deck(key) and key.startswith(_deck_name_)]), self.player, 1))
        
        # Shop Region
        for location in balatro_location_name_to_id:
            if str(location).startswith("Shop Item"):
                self.shop_locations[balatro_location_name_to_id[location]] = location

        for i in [stake_to_number.get(key) for key in self.playable_stakes]:
            stake = int(i) 
            shop_region = Region("Shop " + number_to_stake.get(stake), self.player, self.multiworld)
            id_offset = shop_id_offset + (stake - 1)*max_shop_items
            
            list_of_decks_with_stake_attached = list()
            for j in self.playable_decks:
                list_of_decks_with_stake_attached.append(j + " " + number_to_stake[stake])
            
            for j in range(self.options.shop_items.value):
                location_name = self.shop_locations[id_offset + j]
                location_id = id_offset + j
                new_location = BalatroLocation(self.player, location_name, location_id, shop_region)

                new_location.progress_type = LocationProgressType.DEFAULT
                
                # balance out shop items a bit
                add_rule(new_location, lambda state, _require_ = (j / 3): 
                    state.has_from_list(list(jokers.values()), self.player, _require_) or
                    state.has_from_list(list(joker_bundles.values()), self.player, j / 11))
                
                shop_region.locations.append(new_location)
                self.locations_set += 1
                
            self.multiworld.regions.append(shop_region)
            
            menu_region.connect(shop_region, rule = lambda state, _stake_ = stake, _decklist_ = list_of_decks_with_stake_attached: 
                (self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck or state.has_any(list(deck_id_to_name.values()), self.player)) and
                (self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item or state.has(number_to_stake[_stake_], self.player)) and
                (self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item_per_deck or state.has_from_list(_decklist_, self.player, 1)))
            
            
            
        # GOALS 
        stake_as_item_per_deck_list = list()
        if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck:
            play_decks = list(self.playable_decks.copy())
            random.shuffle(play_decks)
            stake_as_item_per_deck_list = list([key + " " + self.required_stake for key in play_decks][0:self.options.decks_win_goal.value])
            
        if self.options.goal.value == Options.Goal.option_beat_decks:
            self.multiworld.completion_condition[self.player] = lambda state: (state.has_from_list(
                list(deck_id_to_name.values()), self.player, self.options.decks_win_goal.value)) or  \
                (self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck and state.has_all(stake_as_item_per_deck_list, self.player))
            
        elif self.options.goal.value == Options.Goal.option_unlock_jokers:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(list(jokers.values()),
                                                                                self.player,
                                                                                self.options.jokers_unlock_goal.value) or  \
            state.has_from_list(list(joker_bundles.values()), self.player, math.ceil(self.options.jokers_unlock_goal.value / 10))
            
        elif self.options.goal.value == Options.Goal.option_beat_ante:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_any(
                list(deck_id_to_name.values()), self.player)
            
        elif self.options.goal.value == Options.Goal.option_beat_decks_on_stake:
            self.multiworld.completion_condition[self.player] = lambda state: (state.has_from_list(
                list(deck_id_to_name.values()), self.player, self.options.decks_win_goal.value) and self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item) or \
                (self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item and state.has(self.required_stake, self.player) and state.has_from_list(
                list(deck_id_to_name.values()), self.player, self.options.decks_win_goal.value)) or \
                (self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck and state.has_all(stake_as_item_per_deck_list, self.player))
        elif self.options.goal.value == Options.Goal.option_win_with_jokers_on_stake:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(list(jokers.values()),
                                                                                self.player,
                                                                                self.options.jokers_unlock_goal.value) or  \
            state.has_from_list(list(joker_bundles.values()), self.player, math.ceil(self.options.jokers_unlock_goal.value / 10)) and \
                (self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item or state.has(self.required_stake, self.player)) and \
                (self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item_per_deck or state.has_any(stake_as_item_per_deck_list, self.player))

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
            "required_stake" : stake_to_number[self.required_stake],
            "included_stakes" : [stake_to_number.get(key) for key in self.playable_stakes],
            "included_decks" : [deck_name_to_key.get(key) for key in self.playable_decks],
            "stake1_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[1])],
            "stake2_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[2])],
            "stake3_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[3])],
            "stake4_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[4])],
            "stake5_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[5])],
            "stake6_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[6])],
            "stake7_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[7])],
            "stake8_shop_locations": [key for key, value in self.shop_locations.items() if str(value).__contains__(number_to_stake[8])],
            "jokerbundle1" : self.short_mode_pool[0:10],
            "jokerbundle2" : self.short_mode_pool[10:20],
            "jokerbundle3" : self.short_mode_pool[20:30],
            "jokerbundle4" : self.short_mode_pool[30:40],
            "jokerbundle5" : self.short_mode_pool[40:50],
            "jokerbundle6" : self.short_mode_pool[50:60],
            "jokerbundle7" : self.short_mode_pool[60:70],
            "jokerbundle8" : self.short_mode_pool[70:80],
            "jokerbundle9" : self.short_mode_pool[80:90],
            "jokerbundle10" : self.short_mode_pool[90:100],
            "jokerbundle11" : self.short_mode_pool[100:110],
            "jokerbundle12" : self.short_mode_pool[110:120],
            "jokerbundle13" : self.short_mode_pool[120:130],
            "jokerbundle14" : self.short_mode_pool[130:140],
            "jokerbundle15" : self.short_mode_pool[140:150],
            "minimum_price": min_price,
            "maximum_price": max_price,
            "deathlink": bool(self.options.deathlink),
            "stake_unlock_mode" : self.options.stake_unlock_mode.value,
            "remove_jokers" : bool(self.options.remove_or_debuff_jokers),
            "remove_consumables" : bool(self.options.remove_or_debuff_consumables),
        }
        return base_data
