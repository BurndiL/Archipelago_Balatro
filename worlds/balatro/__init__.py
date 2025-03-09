import typing

from typing import Any, Dict, List, Union

from BaseClasses import ItemClassification, Region, Tutorial, LocationProgressType, CollectionState
from ..AutoWorld import WebWorld, World
from .Items import item_name_to_id, item_id_to_name, item_table, is_joker, is_joker_bundle, jokers, decks, joker_bundles, offset, ItemData, BalatroItem, \
    is_deck, is_progression, is_useful, is_bundle, tarots, planets, vouchers, spectrals, is_voucher, is_booster, is_stake, is_stake_per_deck, \
    stake_to_number, number_to_stake, is_tarot, is_planet, is_spectral, item_groups, is_challenge_unlock, is_import_license
from .BalatroDecks import deck_id_to_name, deck_name_to_key, challenge_id_to_name
import math
from worlds.generic.Rules import add_rule, CollectionRule
from .Options import BalatroOptions, Traps, IncludeDecksMode, StakeUnlockMode, \
    IncludeStakesMode, Goal, TarotBundle, SpectralBundle, PlanetBundle, ChallengeUnlockMode, IncludeJokerUnlocks, \
    IncludeAchievements, IncludeVoucherUnlocks, IncludeChallenges, ModdedItems
from Options import OptionError
from .Locations import BalatroLocation, balatro_location_id_to_name, balatro_location_name_to_id, \
    balatro_location_id_to_stake, shop_id_offset, balatro_location_id_to_ante, max_shop_items, consumable_id_offset, balatro_location_id_to_blind


class BalatroWebWorld(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://discord.gg/dESF3rzxQu"
    rich_text_options_doc = True
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Balatro on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Burndi"]
    )

    tutorials = [setup_en]


class BalatroWorld(World):
    """
    Balatro is a poker-themed roguelike deck-building video game developed by LocalThunk.
    In the game, players play poker hands to score points and defeat "blinds", while improving their deck and purchasing joker cards with a variety of effects. 
    Source: https://en.wikipedia.org/wiki/Balatro_(video_game)
    """
    game = "Balatro"
    web = BalatroWebWorld()

    topology_present = False

    options_dataclass = BalatroOptions
    options: BalatroOptions

    locations_set = 0
    shop_locations = dict()
    consumable_locations = dict()

    item_name_to_id = item_name_to_id
    item_id_to_name = item_id_to_name

    location_id_to_name = balatro_location_id_to_name
    location_name_to_id = balatro_location_name_to_id

    playable_decks = [value for _, value in deck_id_to_name.items()]
    playable_stakes = list([value for _, value in number_to_stake.items()])
    required_stake = "White Stake"

    short_mode_pool = list(jokers.keys())

    joker_bundles = []
    tarot_bundles = []
    spectral_bundles = []
    planet_bundles = []
    bundle_with_custom_tarot = "Tarot Bundle"
    bundle_with_custom_planet = "Planet Bundle"
    bundle_with_custom_spectral = "Spectral Bundle"

    item_name_groups = item_groups

    itempool: Dict[str, int]

    distributed_fillers = dict()

    def generate_early(self):

        self.random.shuffle(self.short_mode_pool)

        # decks
        if self.options.include_decksMode.value == IncludeDecksMode.option_all:
            self.playable_decks = [value for _,
                                   value in deck_id_to_name.items()]
        elif self.options.include_decksMode.value == IncludeDecksMode.option_number:
            playable_deck_choice = list(
                [value for key, value in deck_id_to_name.items()])
            self.random.shuffle(playable_deck_choice)
            self.playable_decks = playable_deck_choice[0:
                                                       self.options.include_deckNumber.value]
        elif self.options.include_decksMode.value == IncludeDecksMode.option_choose:
            self.playable_decks = self.options.include_deckChoice.value

        # stakes
        if self.options.include_stakesMode == IncludeStakesMode.option_all:
            self.playable_stakes = [value for _,
                                    value in number_to_stake.items()]
            self.random.shuffle(self.playable_stakes)
        elif self.options.include_stakesMode == IncludeStakesMode.option_number:
            playable_stake_choice = list(
                [value for key, value in number_to_stake.items()])
            self.random.shuffle(playable_stake_choice)
            self.playable_stakes = playable_stake_choice[0:
                                                         self.options.include_stakesNumber.value]
        elif self.options.include_stakesMode == IncludeStakesMode.option_choose:
            if len(self.options.include_stakesList.value) == 0:
                raise OptionError("Must choose at least 1 playable stake.")
            self.playable_stakes = list(self.options.include_stakesList.value)

        if self.options.stake_unlock_mode == StakeUnlockMode.option_vanilla:
            unsorted_stakes = list(
                map(lambda x: stake_to_number[x], self.playable_stakes))
            unsorted_stakes.sort()
            self.playable_stakes = list(
                map(lambda x: number_to_stake[x], unsorted_stakes))

        if len(list(self.options.required_stake_for_goal.value)) > 0 and list(self.options.required_stake_for_goal.value)[0] in self.playable_stakes:
            self.required_stake = list(
                self.options.required_stake_for_goal.value)[0]
        else:
            self.required_stake = self.playable_stakes[-1]

        self.options.decks_win_goal.value = min(
            self.options.decks_win_goal.value, len(self.playable_decks))

        self.options.unique_deck_win_goal.value = min(self.options.unique_deck_win_goal.value, len(
            self.playable_decks) * len(self.playable_stakes))

        # Joker Bundles
        number_of_bundles = round(
            len(jokers) / self.options.joker_bundle_size.value)
        self.joker_bundles = [None] * number_of_bundles
        for index, joker in enumerate(self.short_mode_pool):
            if self.joker_bundles[index % number_of_bundles] == None:
                self.joker_bundles[index % number_of_bundles] = []
            self.joker_bundles[index % number_of_bundles].append(joker)

        def get_bundles_from_option(bundles) -> list:
            result = [None] * len(bundles)
            counter = 0
            for bundle in bundles:
                if result[counter] == None:
                    result[counter] = []
                for card in bundle.split(';'):
                    result[counter].append(item_name_to_id[card.strip()])
                counter += 1

            return result

        # Consumable Bundles
        if (self.options.tarot_bundle == TarotBundle.option_custom_bundles):
            if len(self.options.custom_tarot_bundles.value) == 0:
                raise OptionError(
                    "No Custom Tarots Specified. To avoid this turn off custom tarot bundles")

            if len(self.options.custom_tarot_bundles.value) > 5:
                raise OptionError("Too many custom Tarot Bundles specified.")

            self.tarot_bundles = get_bundles_from_option(
                self.options.custom_tarot_bundles.value)
            for index, value in enumerate(self.tarot_bundles):
                if (value).__contains__(item_name_to_id["Archipelago Tarot"]):
                    self.bundle_with_custom_tarot = "Tarot Bundle " + \
                        str(index+1)

        if (self.options.planet_bundle == PlanetBundle.option_custom_bundles):
            if len(self.options.custom_planet_bundles.value) == 0:
                raise OptionError(
                    "No Custom Planets Specified. To avoid this turn off custom planet bundles")

            if len(self.options.custom_tarot_bundles.value) > 5:
                raise OptionError("Too many custom Planet Bundles specified.")

            self.planet_bundles = get_bundles_from_option(
                self.options.custom_planet_bundles.value)
            if (value).__contains__(item_name_to_id["Archipelago Belt"]):
                self.bundle_with_custom_planet = "Planet Bundle " + \
                    str(index+1)

        if (self.options.spectral_bundle == SpectralBundle.option_custom_bundles):
            if len(self.options.custom_spectral_bundles.value) == 0:
                raise OptionError(
                    "No Custom Spectrals Specified. To avoid this turn off custom spectral bundles")

            if len(self.options.custom_tarot_bundles.value) > 5:
                raise OptionError(
                    "Too many custom Spectral Bundles specified.")

            self.spectral_bundles = get_bundles_from_option(
                self.options.custom_spectral_bundles.value)
            if (value).__contains__(item_name_to_id["Archipelago Spectral"]):
                self.bundle_with_custom_spectral = "Spectral Bundle " + \
                    str(index+1)

        # make consumable pool accessible as soon as possible
        self.multiworld.local_early_items[self.player][self.random.choice(
            ["Archipelago Tarot", "Archipelago Belt"])] = 1
        self.multiworld.local_early_items[self.player][self.random.choice(
            [self.bundle_with_custom_tarot, self.bundle_with_custom_planet])] = 1

    def create_items(self):
        decks_to_unlock = self.options.decks_unlocked_from_start.value

        if decks_to_unlock > len(self.playable_decks):
            decks_to_unlock = len(self.playable_decks)

        excludedItems: Dict[str, ItemData] = {}
        if decks_to_unlock > 0:
            # unlock first stake
            if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item:
                stake_name = self.random.choice(self.playable_stakes)
                stake_data = item_table[stake_name]
                excludedItems[stake_name] = stake_data
                preCollected_item = self.create_item(
                    stake_name, ItemClassification.progression)
                self.multiworld.push_precollected(preCollected_item)

            # get all decks
            deck_table: Dict[str, ItemData] = {}
            for item in item_table:
                if is_deck(item) and (item in self.playable_decks):
                    deck_table[item] = item_table[item]

            deck_table = list(deck_table.items())
            while decks_to_unlock > 0:
                deck = self.random.choice(deck_table)
                deck_name = deck[0]
                deck_data = deck[1]
                if self.options.stake_unlock_mode != StakeUnlockMode.option_stake_as_item_per_deck:
                    preCollected_item = self.create_item(
                        deck_name, ItemClassification.progression)
                    self.multiworld.push_precollected(preCollected_item)
                    excludedItems[deck_name] = deck_data
                deck_table.remove(deck)
                decks_to_unlock -= 1

                if self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck:
                    stake_name = deck_name + " " + \
                        self.random.choice(self.playable_stakes)
                    stake_data = item_table[stake_name]
                    preCollected_stake = self.create_item(
                        stake_name, ItemClassification.progression)
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

            if (self.options.tarot_bundle != TarotBundle.option_one_bundle and item_name == "Tarot Bundle"):
                continue

            if (self.options.tarot_bundle != TarotBundle.option_individual and is_tarot(item_name)):
                continue

            if (self.options.tarot_bundle != TarotBundle.option_custom_bundles and item_name.startswith("Tarot Bundle ")):
                continue

            if (self.options.tarot_bundle == TarotBundle.option_custom_bundles and item_name.startswith("Tarot Bundle ") and item_name_to_id[item_name] - offset - 373 > len(self.tarot_bundles)):
                continue

            if (self.options.planet_bundle != PlanetBundle.option_one_bundle and item_name == "Planet Bundle"):
                continue

            if (self.options.planet_bundle != PlanetBundle.option_individual and is_planet(item_name)):
                continue

            if (self.options.planet_bundle != PlanetBundle.option_custom_bundles and item_name.startswith("Planet Bundle ")):
                continue

            if (self.options.planet_bundle == PlanetBundle.option_custom_bundles and item_name.startswith("Planet Bundle ") and item_name_to_id[item_name] - offset - 378 > len(self.planet_bundles)):
                continue

            if (self.options.spectral_bundle != SpectralBundle.option_one_bundle and item_name == "Spectral Bundle"):
                continue

            if (self.options.spectral_bundle != SpectralBundle.option_individual and is_spectral(item_name)):
                continue

            if (self.options.spectral_bundle != SpectralBundle.option_custom_bundles and item_name.startswith("Spectral Bundle ")):
                continue

            if (self.options.spectral_bundle == SpectralBundle.option_custom_bundles and item_name.startswith("Spectral Bundle ") and item_name_to_id[item_name] - offset - 383 > len(self.spectral_bundles)):
                continue

            if (self.options.joker_bundles and is_joker(item_name)):
                continue

            if (not self.options.joker_bundles and is_joker_bundle(item_name)):
                continue

            if (is_joker_bundle(item_name) and len(self.joker_bundles) < (item_name_to_id[item_name] - offset) - 520):
                continue

            if is_challenge_unlock(item_name):
                if self.options.challenge_unlock_mode != ChallengeUnlockMode.option_as_items:
                    continue
                if self.options.include_challenges == False:
                    continue

            if is_import_license(item_name):
                if self.options.modded_items != ModdedItems.option_include_as_ap_items:
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

                # add import license as many times as requested in the yaml
                if (is_import_license(item_name)):
                    for _ in range(self.options.import_licenses.value):
                        self.itempool.append(
                            self.create_item(item_name, classification))
                else:
                    self.itempool.append(
                        self.create_item(item_name, classification))

        if len(self.itempool) > self.locations_set:
            raise OptionError("Not enough Balatro locations to generate. Consider adding more decks or stakes or enabling joker bundles. There are " +
                              str(len(self.itempool) - self.locations_set) + " locations missing.")
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
                trap_id = self.random.randint(330, 335)
                self.itempool.append(self.create_item(
                    item_id_to_name[trap_id + offset], ItemClassification.trap))
            else:
                filler_id = 310

                filler_classification = ItemClassification.filler
                if op_filler_max > 0:
                    filler_classification = ItemClassification.useful
                    filler_id = op_filler + 300
                    op_filler += 1
                    if op_filler == 8:
                        op_filler = 1
                        op_filler_max -= 1

                # after all good filler items are placed, fill the rest with normal filler items
                else:
                    filler_id = self.random.randint(310, 321)

                self.itempool.append(self.create_item(
                    item_id_to_name[filler_id + offset], filler_classification))

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

        if classification is ItemClassification.filler:
            if self.distributed_fillers.get(item_name) is None:
                self.distributed_fillers[item_name] = 1
            else:
                self.distributed_fillers[item_name] += 1

        return BalatroItem(item_name, classification, item.code, self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        self.multiworld.regions.append(menu_region)
        all_locations: List[BalatroLocation] = list()
        challenge_complete_locations: List[BalatroLocation] = list()

        for deck in deck_id_to_name:
            deck_name = deck_id_to_name[deck]
            if (deck_name in self.playable_decks):
                deck_region = Region(deck_name, self.player, self.multiworld)
                for location in balatro_location_name_to_id:
                    if str(location).startswith(deck_name):
                        location_id = balatro_location_name_to_id[location]
                        stake = balatro_location_id_to_stake[location_id]
                        ante = balatro_location_id_to_ante[location_id]
                        blind = balatro_location_id_to_blind[location_id]

                        if self.options.only_boss_blinds_are_checks.value and (blind == "Small Blind" or blind == "Big Blind"):
                            continue

                        new_location = BalatroLocation(
                            self.player, location, location_id, deck_region)

                        new_location.ante = ante
                        new_location.stake = number_to_stake[stake]
                        new_location.deck = deck_name

                        new_location.progress_type = LocationProgressType.DEFAULT

                        # to make life easier for players require some jokers to be found to beat ante 4 and up!
                        if ante >= 4:
                            add_rule(new_location, lambda state, _ante3_=ante: state.has_from_list(list(jokers.values(
                            )), self.player, 5 + _ante3_ * 2) or state.has_from_list(list(joker_bundles.values()), self.player, round((_ante3_ * 10) / self.options.joker_bundle_size.value)))
                            add_rule(new_location, lambda state: state.has_from_list(
                                list(['Buffoon Pack']), self.player, 1))

                        # limit later stakes to "require" jokers so progression is distributed better

                        if ante > 2:
                            add_rule(new_location, lambda state, _stake2_=stake:
                                     (state.has_from_list(list(joker_bundles.values()), self.player, (_stake2_ - 2)) or
                                      state.has_from_list(list(jokers.values()), self.player, (_stake2_ - 2) * 5)) and
                                     state.has_from_list(list(vouchers.values()), self.player, _stake2_ - 2))

                        if self.options.stake_unlock_mode == StakeUnlockMode.option_linear or self.options.stake_unlock_mode == StakeUnlockMode.option_vanilla:
                            if number_to_stake[stake] in self.playable_stakes:
                                index = self.playable_stakes.index(
                                    number_to_stake[stake])
                                if index != 0:
                                    add_rule(new_location, lambda state, _deck_name_=deck_name, _index_=index: state.can_reach_location(
                                        _deck_name_ + " Ante 8 " + self.playable_stakes[_index_ - 1] + " Boss Blind", self.player))
                        elif self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item:
                            add_rule(new_location, lambda state, _stake_=stake: state.has(
                                number_to_stake[_stake_], self.player))
                        elif self.options.stake_unlock_mode == StakeUnlockMode.option_stake_as_item_per_deck:
                            add_rule(new_location, lambda state, _deck_name1_=deck_name, _stake1_=stake: state.has(
                                _deck_name1_ + " " + number_to_stake[_stake1_], self.player))

                        if stake in [stake_to_number.get(key) for key in self.playable_stakes]:
                            self.locations_set += 1
                            all_locations.append(new_location)
                            deck_region.locations.append(new_location)

                self.multiworld.regions.append(deck_region)
                # has to have deck collected to access it
                menu_region.connect(deck_region, None,
                                    lambda state, _deck_name_=deck_name: state.has(_deck_name_, self.player) or
                                    state.has_from_list(list([key for key, _ in item_table.items() if is_stake_per_deck(key) and key.startswith(_deck_name_)]), self.player, 1))

        def can_reach_count(state: CollectionState, locations: List[BalatroLocation], count: int = 1) -> bool:
            if count <= 0:
                return True
            counter = 0
            for loc in locations:
                if state.can_reach_location(loc.name, self.player):
                    counter += 1
                    if counter >= count:
                        return True
            return False

        def get_locations_where(deck: str = None, ante: int = None, stake: int = None) -> list:
            return list([element for element in all_locations if (ante == None or element.ante == ante) and (stake == None or stake_to_number[element.stake] == stake) and (deck == None or element.deck == deck)])

        # Shop Region
        for location in balatro_location_name_to_id:
            if str(location).startswith("Shop Item"):
                self.shop_locations[balatro_location_name_to_id[location]] = location

        for i in [stake_to_number.get(key) for key in self.playable_stakes]:
            stake = int(i)
            shop_region = Region(
                "Shop " + number_to_stake.get(stake), self.player, self.multiworld)
            id_offset = shop_id_offset + (stake - 1)*max_shop_items

            for j in range(self.options.shop_items.value):
                location_name = self.shop_locations[id_offset + j]
                location_id = id_offset + j
                new_location = BalatroLocation(
                    self.player, location_name, location_id, shop_region)

                # balance out shop items a bit
                add_rule(new_location, lambda state, _require_=j:
                         state.has_from_list(list(jokers.values()), self.player, _require_ / 3) or
                         state.has_from_list(list(joker_bundles.values()), self.player, _require_ / (self.options.joker_bundle_size.value * 2)))

                shop_region.locations.append(new_location)
                self.locations_set += 1

            self.multiworld.regions.append(shop_region)

            # Take stake unlock into account here
            menu_region.connect(shop_region, None, lambda state, _stake_=stake: can_reach_count(
                state, get_locations_where(None, None, _stake_)))

        # Consumable Pool
        consumable_region = Region(
            "Consumable Items", self.player, self.multiworld)

        counter = 0
        for location in balatro_location_name_to_id:
            if str(location).startswith("Consumable Item") and counter < self.options.ap_consumable_items.value:
                counter += 1
                self.consumable_locations[balatro_location_name_to_id[location]] = location
                location_name = location
                location_id = balatro_location_name_to_id[location]

                new_location = BalatroLocation(
                    self.player, location_name, location_id, consumable_region)
                consumable_region.locations.append(new_location)

                # balance out consumable items a bit
                add_rule(new_location, lambda state, _require_=counter:
                         state.has_from_list(list(jokers.values()), self.player, _require_ / 6) or
                         state.has_from_list(list(joker_bundles.values()), self.player, _require_ / (self.options.joker_bundle_size.value * 4)))

                self.locations_set += 1

        menu_region.connect(consumable_region, None, rule=lambda state: (state.has(
            "Archipelago Tarot", self.player) or state.has("Archipelago Belt", self.player) or state.has("Archipelago Spectral", self.player) or
            state.has(self.bundle_with_custom_planet, self.player) or state.has(self.bundle_with_custom_spectral, self.player) or state.has(self.bundle_with_custom_tarot, self.player)) and can_reach_count(state, get_locations_where(None, None, None)))

        # Challenges

        challenge_region = Region("Challenges", self.player, self.multiworld)

        if self.options.include_challenges.value == True:
            for challenge in challenge_id_to_name:
                challenge_name = challenge_id_to_name[challenge]
                if challenge_name in self.options.exclude_challenges.value:
                    continue
                for location in balatro_location_name_to_id:
                    if str(location).startswith(challenge_name):

                        location_id = balatro_location_name_to_id[location]
                        ante = balatro_location_id_to_ante[location_id]
                        blind = balatro_location_id_to_blind[location_id]

                        if self.options.only_boss_blinds_are_checks.value and (blind == "Small Blind" or blind == "Big Blind"):
                            continue

                        new_location = BalatroLocation(
                            self.player, location, location_id, challenge_region)

                        if (ante == 8 and blind == "Boss Blind"):
                            challenge_complete_locations.append(new_location)

                        new_location.progress_type = LocationProgressType.DEFAULT

                        if self.options.challenge_unlock_mode == ChallengeUnlockMode.option_vanilla:
                            if challenge > 1:
                                add_rule(new_location, lambda state, _challenge_=challenge, previous_challenge_complete_locations=challenge_complete_locations.copy():
                                         can_reach_count(state, previous_challenge_complete_locations[:-1], _challenge_ - 5 - len(self.options.exclude_challenges.value)))
                        elif self.options.challenge_unlock_mode == ChallengeUnlockMode.option_as_items:
                            add_rule(new_location, lambda state: state.has(
                                challenge_name + " Challenge Unlock", self.player))

                        # to make life easier for players require some jokers to be found to beat ante 4 and up! (copied over from deck locations)
                        if ante >= 4:
                            add_rule(new_location, lambda state, _ante3_=ante: state.has_from_list(list(jokers.values(
                            )), self.player, 5 + _ante3_ * 2) or state.has_from_list(list(joker_bundles.values()), self.player, round((_ante3_ * 10) / self.options.joker_bundle_size.value)))
                            add_rule(new_location, lambda state: state.has_from_list(
                                list(['Buffoon Pack']), self.player, 1))

                        # limit later stakes to "require" jokers so progression is distributed better

                        if ante > 2:
                            add_rule(new_location, lambda state:
                                     (state.has_from_list(list(joker_bundles.values()), self.player, 1) or
                                      state.has_from_list(list(jokers.values()), self.player, 5)) and
                                     state.has_from_list(list(vouchers.values()), self.player, 1))

                        self.locations_set += 1
                        challenge_region.locations.append(new_location)

        menu_region.connect(challenge_region, None, lambda state: can_reach_count(
            state, get_locations_where(None, None, None)))

        # Joker Discovery Locations

        # TODO: handle legendary jokers (also think about soul and spectral packs)
        if self.options.discover_jokers_as_locations.value == True:

            joker_discovery_region = Region(
                "Joker Discoveries", self.player, self.multiworld)

            for location in balatro_location_name_to_id:
                if str(location).startswith("Discover"):
                    location_id = balatro_location_name_to_id[location]
                    joker_name = str(location).replace("Discover ", "")

                    new_location = BalatroLocation(
                        self.player, location, location_id, joker_discovery_region)

                    add_rule(new_location, lambda state: state.has(
                        joker_name, self.player))

            menu_region.connect(joker_discovery_region, None, lambda state: can_reach_count(
                state, get_locations_where(None, None, None)))

        # Joker/Voucher unlocks (these are already instantiated in Locations.py but rules are only applied here)

        def bundle_with_joker(joker_name: str) -> str:
            if (self.options.joker_bundles):
                for idx, bundle in enumerate(self.joker_bundles):
                    if item_name_to_id[joker_name] in bundle:
                        return "Joker Bundle " + str(idx + 1)
            return joker_name

        def bundle_with_tarot(tarot_name: str) -> str:
            if (self.options.tarot_bundle == TarotBundle.option_one_bundle):
                return "Tarot Bundle"

            if (self.options.tarot_bundle == TarotBundle.option_custom_bundles):
                for idx, bundle in enumerate(self.tarot_bundles):
                    if item_name_to_id[tarot_name] in bundle:
                        return "Tarot Bundle " + str(idx + 1)
            return tarot_name

        def bundle_with_planet(planet_name: str) -> str:
            if (self.options.planet_bundle == PlanetBundle.option_one_bundle):
                return "Planet Bundle"

            if (self.options.planet_bundle == PlanetBundle.option_custom_bundles):
                for idx, bundle in enumerate(self.planet_bundles):
                    if item_name_to_id[planet_name] in bundle:
                        return "Planet Bundle " + str(idx + 1)
            return planet_name

        def bundle_with_spectral(spectral_name: str) -> str:
            if (self.options.spectral_bundle == SpectralBundle.option_one_bundle):
                return "Spectral Bundle"

            if (self.options.spectral_bundle == SpectralBundle.option_custom_bundles):
                for idx, bundle in enumerate(self.spectral_bundles):
                    if item_name_to_id[spectral_name] in bundle:
                        return "Spectral Bundle " + str(idx + 1)
            return spectral_name

        unlocks_region = Region("Joker/Voucher Unlocks",
                                self.player, self.multiworld)
        menu_region.connect(unlocks_region, None, rule=lambda state: can_reach_count(
            state, get_locations_where(None, None, None)))
        self.multiworld.regions.append(unlocks_region)

        def add_unlock_location(location_name: str, location_id: int, rule: CollectionRule, difficulty: int, diff_threshold: int):
            if difficulty <= diff_threshold:
                new_location = BalatroLocation(
                    self.player, location_name, location_id, unlocks_region)
                self.locations_set += 1
                unlocks_region.locations.append(new_location)

                add_rule(new_location, rule)

        def state_has_all_tarots(state: CollectionState) -> bool:
            return state.has_all(list([bundle_with_tarot("The Fool"), bundle_with_tarot("The Magician"), bundle_with_tarot("The High Priestess"), bundle_with_tarot("The Empress"), bundle_with_tarot("The Emperor"),
                                       bundle_with_tarot("The High Priestess"), bundle_with_tarot("The Hierophant"), bundle_with_tarot(
                "The Lovers"), bundle_with_tarot("The Chariot"), bundle_with_tarot("Justice"), bundle_with_tarot("The Hermit"),
                bundle_with_tarot("The Wheel of Fortune"), bundle_with_tarot("Strength"), bundle_with_tarot(
                "The Hanged Man"), bundle_with_tarot("Death"), bundle_with_tarot("Temperance"),
                bundle_with_tarot("The Devil"), bundle_with_tarot(
                "The Tower"), bundle_with_tarot("The Star"),
                bundle_with_tarot("The Moon"), bundle_with_tarot(
                "The Sun"), bundle_with_tarot("Judgement"),
                bundle_with_tarot("The World")]), self.player)

        def state_has_all_planets(state: CollectionState) -> bool:
            return state.has_all(list([bundle_with_planet("Mercury"), bundle_with_planet("Venus"), bundle_with_planet("Earth"), bundle_with_planet("Mars"), bundle_with_planet("Jupiter"),
                                       bundle_with_planet("Saturn"), bundle_with_planet("Uranus"), bundle_with_planet(
                "Neptune"), bundle_with_planet("Pluto"), bundle_with_planet("Planet X"),
                bundle_with_planet("Ceres"), bundle_with_planet("Eris")]), self.player)

        difficulty_easy = 1
        difficulty_medium = 2
        difficulty_hard = 3
        difficulty_extreme = 4
        counter = 1

        add_unlock_location("Unlock Golden Ticket (Play a 5 card hand that only contains Gold cards)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Devil"), self.player) or state.has(bundle_with_joker("Midas Mask"), self.player), difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Mr. Bones (Lose 5 runs)",
                            balatro_location_name_to_id["Joker Unlock " + str(counter)], lambda state: True, difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Acrobat (Play 200 hands)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        # maybe think about what happens if only abandoned deck unlocked? very unlikely -> not considered in logic
        add_unlock_location("Unlock Sock and Buskin (Play a total of 500 face cards)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Swashbuckler (Sell a total of 20 Jokers)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has_group("Jokers", self.player, 1), difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Troubadour (Win 5 consecutive rounds with a single hand each)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Certificate (Have a gold card with a gold seal)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: (state.has(bundle_with_tarot("The Devil"), self.player) or state.has(bundle_with_joker("Midas Mask"), self.player)) and
                            state.has(bundle_with_spectral("Talisman"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Smeared Joker (Have 3 or more wild cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Lovers"), self.player), difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Throwback (Continue a run from the main menu)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Hanging Chad (Beat a Boss Blind with a high card)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Rough Gem (Have at least 30 diamond cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Star"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Bloodstone (Have at least 30 heart cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Sun"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Arrowhead (Have at least 30 spade cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The World"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Onyx Agate (Have at least 30 club cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Moon"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Glass Joker (Have 5 or more glass cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("Justice"), self.player), difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Showman (Reach ante 4)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 4, None)), difficulty_easy, self.options.include_joker_unlocks.value)
        counter += 1
        add_unlock_location("Unlock Flower Pot (Reach ante 8)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Blueprint (Win a run)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Wee Joker (Win a run in 18 or fewer rounds)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Merry Andy (Win a run in 12 or fewer rounds)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Oops! All 6s (Earn at least 10,000 chips)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Idol (In one hand, eart at least 1,000,000 chips)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Seeing Double (Play a hand that contains four 7 of clubs)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Moon"), self.player) or state.has(
                                bundle_with_tarot("Death"), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Matador (Defeat a Boss Blind in one hand, without using discards)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Hit the Road (Discard 5 Jacks at the same time)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("Death"), self.player) or state.has(
                                bundle_with_tarot("Strength"), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Duo (Win a run without playing a pair)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Trio (Win a run without playing a Three of a Kind)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Family (Win a run without playing a Four of a Kind)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Order (Win a run without playing a Straight)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Tribe (Win a run without playing a Flush)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock The Stuntman (Earn 100,000,000 chips in one hand)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_extreme, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Invisible Joker (Win a run without ever having more than 4 Jokers)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: can_reach_count(state, get_locations_where(None, 8, None)), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Brainstorm (Discard a Royal Flush)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The World"), self.player) or state.has(bundle_with_tarot("The Sun"), self.player) or
                            state.has(bundle_with_tarot("The Moon"), self.player) or state.has(
                                bundle_with_tarot("The Star"), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        # added hermit and temperance requirement to make it more easy
        counter += 1
        add_unlock_location("Unlock Satellite (Have $400 or more)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Hermit"), self.player) and state.has(
                                bundle_with_tarot("Temperance"), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Shoot the Moon (Play every heart card in your deck in a single round)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: True, difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Driver's License (Enhance 16 cards in your deck)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has_any(list([bundle_with_tarot("The Magician"), bundle_with_tarot("The Empress"), bundle_with_tarot("Justice"), bundle_with_tarot("The Hierophant"), bundle_with_tarot("The Lovers"),
                                                              bundle_with_tarot("The Chariot"), bundle_with_tarot("The Devil"), bundle_with_tarot(
                                                                  "The Tower"), bundle_with_joker("Midas Mask"), bundle_with_joker("Marble Joker"),
                                                              bundle_with_spectral("Familiar"), bundle_with_spectral("Grim"), bundle_with_spectral("Incantation")]), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Cartomancer (Discover every Tarot card)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state_has_all_tarots(state), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Astronomer (Discover every Planet card)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state_has_all_planets(state), difficulty_hard, self.options.include_joker_unlocks.value)

        # consumable will also work for this, but too lazy to add to logic, also doesnt really matter
        counter += 1
        add_unlock_location("Unlock Burnt Joker (Sell a total of 50 cards)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has_group("Jokers", self.player, 1), difficulty_easy, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Bootstraps (Have at least 2 Polychrome Jokers)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has_group("Jokers", self.player, 2) and state.has(
                                bundle_with_tarot("The Wheel of Fortune"), self.player),
                            difficulty_medium, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Canio (Find Canio using The Soul)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and state.has(bundle_with_joker("Caino"), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Triboulet (Find Triboulet using The Soul)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and state.has(bundle_with_joker("Triboulet"), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Yorick (Find Yorick using The Soul)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and state.has(bundle_with_joker("Yorick"), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Chicot (Find Chicot using The Soul)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and state.has(bundle_with_joker("Chicot"), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player), difficulty_hard, self.options.include_joker_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Perkeo (Find Perkeo using The Soul)", balatro_location_name_to_id["Joker Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and state.has(bundle_with_joker("Perkeo"), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player), difficulty_hard, self.options.include_joker_unlocks.value)

        # Voucher Unlocks
        counter = 1

        add_unlock_location("Unlock Overstock + (Spend a total of $2500)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Liquidation (Redeem at least 10 voucher cards in one run)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_group("Vouchers", self.player, 10), difficulty_hard, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Glow Up (Have at least 5 joker cards with edition effect)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_group("Jokers", self.player), difficulty_hard, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Reroll Glut (Reroll the shop a total of 100 times)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Omen Globe (Use a total of 25 Tarot cards from booster packs)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_any(list(
                                ["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player) and state.has_group("Tarots", self.player),
                            difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Observatory (Use a total of 25 Planet cards from booster packs)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_any(list(
                                ["Celestial Pack", "Jumbo Celestial Pack", "Mega Celestial Pack"]), self.player) and state.has_group("Planets", self.player),
                            difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Nacho Tong (Play a total of 2500 cards)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Recyclomancy (Discard a total of 2500 cards)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Tarot Tycoon (Buy a total of 50 Tarot cards from the shop)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_group("Tarots", self.player), difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Planet Tycoon (Buy a total of 50 Planet cards from the shop)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has_group("Planets", self.player), difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Money Tree (Max out the interest per round earnings for ten consecutive rounds)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_medium, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Antimatter (Redeem Blank 10 total times)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has(
                                "Blank/Antimatter 1", self.player) or state.has("Blank/Antimatter 2", self.player),
                            difficulty_medium, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Illusion (Buy a total of 20 Playing cards from the shop)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has(
                                "Magic Trick/Illusion 1", self.player) or state.has("Magic Trick/Illusion 2", self.player),
                            difficulty_medium, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Petroglyph (Reach Ante level 12)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_extreme, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Retcon (Discover 25 Blinds)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: True, difficulty_easy, self.options.include_voucher_unlocks.value)

        counter += 1
        add_unlock_location("Unlock Palette (Reduce your hand size down to 5 cards)", balatro_location_name_to_id["Voucher Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("Ectoplasm"), self.player) and state.has_any(
                                list(["Spectral Pack", "Jumbo Spectral Pack", "Mega Spectral Pack"]), self.player)
                            and state.has(bundle_with_joker("Merry Andy"), self.player),
                            difficulty_medium, self.options.include_voucher_unlocks.value)

        counter = 1

        if ("Gold Stake" in self.playable_stakes):
            add_unlock_location("High Stakes Achievement (Clear Gold Stakes on a deck)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(
                                    state, get_locations_where(None, 8, 8)),
                                difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Flushed Achievement (Play a 5 card wild card flush)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(
                                bundle_with_tarot("The Lovers"), self.player),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("ROI Achievement (Buy 5 vouchers by Ante 4)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has_group("Vouchers", self.player, 5) and can_reach_count(
                                state, get_locations_where(None, 4, None)),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Shattered Achievement (Break 2 Glass Cards in a single hand)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(
                                bundle_with_tarot("Justice"), self.player),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Royale Achievement (Play a Royal Flush)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The World"), self.player) or state.has(
                                bundle_with_tarot("The Sun"), self.player)
                            or state.has(bundle_with_tarot("The Moon"), self.player) or state.has(bundle_with_tarot("The Star"), self.player),
                            difficulty_easy, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Retrograde Achievement (Get any poker hand to level 10)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has_group("Planets", self.player) or state.has(bundle_with_joker(
                                "Burnt Joker"), self.player) or state.has(bundle_with_joker("Space Joker"), self.player),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Tiny Hands Achievement (Thin your deck down to 20 or fewer cards)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Hanged Man"), self.player) or
                            (state.has(bundle_with_spectral("Immolate"), self.player) and state.has_any(list(
                                ["Spectral Pack", "Jumbo Spectral Pack", "Mega Spectral Pack"]), self.player)),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Big Hands Achievement (Have 80 or more cards in your deck)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: (state.has_any(list(["Spectral Pack", "Jumbo Spectral Pack", "Mega Spectral Pack"]), self.player) and
                            (state.has(bundle_with_spectral("Cryptid"), self.player) or state.has(bundle_with_spectral("Familiar"), self.player) or
                                state.has(bundle_with_spectral("Grim"), self.player) or state.has(bundle_with_spectral("Incantation"), self.player))) or
                            state.has(bundle_with_joker("DNA"), self.player) or state.has(bundle_with_joker("Marble Joker"), self.player) or
                            state.has_any(list(
                                ["Standard Pack", "Jumbo Standard Pack", "Mega Standard Pack"]), self.player),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("You Get What You Get Achievement (Win a run without rerolling the shop)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_achievements.value)

        if self.options.include_challenges == IncludeChallenges.option_true:
            counter += 1
            add_unlock_location("Rule Bender Achievement (Complete any challenge run)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(state, challenge_complete_locations, 1), difficulty_easy, self.options.include_achievements.value)

            counter += 1
            # only take size of challenge_complete_locations so it still works if hard challenges are excluded
            add_unlock_location("Rule Breaker Achievement (Complete every challenge run)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(
                                    state, challenge_complete_locations, len(challenge_complete_locations)),
                                difficulty_extreme, self.options.include_achievements.value)
        else:
            counter += 2

        counter += 1
        add_unlock_location("Legendary Achievement (Discover a Legendary Joker)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_spectral("The Soul"), self.player) and
                            state.has_any(list([bundle_with_joker("Perkeo"), bundle_with_joker("Caino"), bundle_with_joker("Triboulet"), bundle_with_joker("Yorick"), bundle_with_joker("Chicot"), ]), self.player) and
                            state.has_any(
                                list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player),
                            difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Clairvoyance Achievement (Discover every Spectral card)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has_all(list([bundle_with_spectral("Familiar"), bundle_with_spectral("Grim"), bundle_with_spectral("Incantation"),
                                                              bundle_with_spectral(
                                "Talisman"), bundle_with_spectral("Aura"),
                                bundle_with_spectral("Wraith"), bundle_with_spectral("Sigil"), bundle_with_spectral(
                                "Ouija"), bundle_with_spectral("Ectoplasm"), bundle_with_spectral("Immolate"),
                                bundle_with_spectral(
                                "Ankh"), bundle_with_spectral("Deja Vu"),
                                bundle_with_spectral("Hex"), bundle_with_spectral(
                                "Trance"), bundle_with_spectral("Medium"),
                                bundle_with_spectral("Cryptid"), bundle_with_spectral("The Soul"), bundle_with_spectral("Black Hole")]), self.player) and
                            state.has_any(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player) and
                            state.has_any(list(["Spectral Pack", "Jumbo Spectral Pack", "Mega Spectral Pack"]), self.player) and
                            # for black hole
                            state.has_any(list(
                                ["Celestial Pack", "Jumbo Celestial Pack", "Mega Celestial Pack"]), self.player),
                            difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Extreme Couponer Achievement (Discover every Voucher)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has_group("Vouchers", self.player, len(vouchers)), difficulty_extreme, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Completionist Achievement (Discover your entire collection)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.can_reach_location("Clairvoyance Achievement (Discover every Spectral card)", self.player) and
                            state_has_all_planets(state) and
                            state_has_all_tarots(state) and
                            state.has_all(list(["Arcana Pack", "Jumbo Arcana Pack", "Mega Arcana Pack"]), self.player) and
                            state.has_all(list(["Spectral Pack", "Jumbo Spectral Pack", "Mega Spectral Pack"]), self.player) and
                            state.has_all(list(["Celestial Pack", "Jumbo Celestial Pack", "Mega Celestial Pack"]), self.player) and
                            state.has_all(list(["Standard Pack", "Jumbo Standard Pack", "Mega Standard Pack"]), self.player) and
                            state.has_group("Decks", self.player, len(self.playable_decks)), difficulty_extreme, self.options.include_achievements.value)

        counter += 1
        if ("Gold Stake" in self.playable_stakes):
            add_unlock_location("Completionist+ Achievement (Win every deck at Gold Stake difficulty)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(state, get_locations_where(
                                    None, 8, 8), len(self.playable_decks)),
                                difficulty_extreme, self.options.include_achievements.value)

        counter += 1
        if ("Gold Stake" in self.playable_stakes):
            add_unlock_location("Completionist++ Achievement (Earn a Gold Sticker on every Joker)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(state, get_locations_where(None, 8, 8)) and
                                (state.has_all(list([key for _, key in jokers.items() if key not in self.options.filler_jokers]), self.player) or state.has_all(
                                    list(joker_bundles.values()), self.player)),
                                difficulty_extreme, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Ante Up! Achievement (Reach Ante 4)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 4, None)),
                            difficulty_easy, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Ante Upper! Achievement (Reach Ante 8)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_easy, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Heads Up Achievement (Win a run)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_easy, self.options.include_achievements.value)

        counter += 1
        if "Red Stake" in self.playable_stakes or "Green Stake" in self.playable_stakes or "Black Stake" in self.playable_stakes or "Blue Stake" in self.playable_stakes or \
                "Purple Stake" in self.playable_stakes or "Orange Stake" in self.playable_stakes or "Gold Stake" in self.playable_stakes:
            add_unlock_location("Low Stakes Achievement (Win a run on at least Red Stakes difficulty)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(state, get_locations_where(None, 8, 2)) or can_reach_count(
                                    state, get_locations_where(None, 8, 3)) or can_reach_count(state, get_locations_where(None, 8, 4))
                                or can_reach_count(state, get_locations_where(None, 8, 5)) or can_reach_count(state, get_locations_where(None, 8, 6)) or can_reach_count(state, get_locations_where(None, 8, 7))
                                or can_reach_count(state, get_locations_where(None, 8, 8)),
                                difficulty_easy, self.options.include_achievements.value)

        counter += 1
        if "Black Stake" in self.playable_stakes or "Blue Stake" in self.playable_stakes or \
                "Purple Stake" in self.playable_stakes or "Orange Stake" in self.playable_stakes or "Gold Stake" in self.playable_stakes:
            add_unlock_location("Mid Stakes Achievement (Win a run on at least Black Stakes difficulty)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                                lambda state: can_reach_count(
                                    state, get_locations_where(None, 8, 4))
                                or can_reach_count(state, get_locations_where(None, 8, 5)) or can_reach_count(state, get_locations_where(None, 8, 6)) or can_reach_count(state, get_locations_where(None, 8, 7))
                                or can_reach_count(state, get_locations_where(None, 8, 8)), difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Card Player Achievement (Play at least 2500 cards)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Card Discarder Achievement (Discard at least 2500 cards)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: True, difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Nest Egg Achievement (Have $400 or more)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state.has(bundle_with_tarot("The Hermit"), self.player) and state.has(
                                bundle_with_tarot("Temperance"), self.player),
                            difficulty_medium, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Speedrunner Achievement (Win a run with 12 or fewer rounds)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("10K Achievement (Score 10,000 Chips in a single hand)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_easy, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("1,000K Achievement (Score 100,000,000 Chips in a single hand)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("100,000K Achievement (Score 100,000,000,000 Chips in a single hand)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: can_reach_count(
                                state, get_locations_where(None, 8, None)),
                            difficulty_extreme, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Astronomy Achievement (Discover every Planet Card)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state_has_all_planets(state), difficulty_hard, self.options.include_achievements.value)

        counter += 1
        add_unlock_location("Cartomancy Achievement (Discover every Tarot Card)", balatro_location_name_to_id["Achievement Unlock " + str(counter)],
                            lambda state: state_has_all_tarots(state), difficulty_hard, self.options.include_achievements.value)

        # GOALS

        if self.options.goal.value == Goal.option_beat_decks:
            self.multiworld.completion_condition[self.player] = lambda state: can_reach_count(state, get_locations_where(
                None, 8, stake_to_number[self.required_stake]), self.options.decks_win_goal.value)  # you can use required stake because it really doesnt matter

        elif self.options.goal.value == Goal.option_unlock_jokers:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_from_list(list(jokers.values()),
                                                                                                  self.player,
                                                                                                  self.options.jokers_unlock_goal.value) or  \
                state.has_from_list(list(joker_bundles.values()), self.player, math.ceil(
                    self.options.jokers_unlock_goal.value / self.options.joker_bundle_size.value))

        elif self.options.goal.value == Goal.option_beat_ante:
            self.multiworld.completion_condition[self.player] = lambda state: can_reach_count(
                state, get_locations_where(None, 8, None), 1)

        elif self.options.goal.value == Goal.option_beat_decks_on_stake:
            self.multiworld.completion_condition[self.player] = lambda state: can_reach_count(
                state, get_locations_where(None, 8, stake_to_number[self.required_stake]), self.options.decks_win_goal.value)

        elif self.options.goal.value == Goal.option_win_with_jokers_on_stake:
            self.multiworld.completion_condition[self.player] = lambda state: \
                can_reach_count(state, get_locations_where(None, 8, stake_to_number[self.required_stake]), 1) and \
                (state.has_from_list(list(jokers.values()), self.player, self.options.jokers_unlock_goal.value) or
                 state.has_from_list(list(joker_bundles.values()), self.player, math.ceil(self.options.jokers_unlock_goal.value / self.options.joker_bundle_size.value)))

        elif self.options.goal.value == Goal.option_beat_unique_decks:
            self.multiworld.completion_condition[self.player] = lambda state: can_reach_count(
                state, get_locations_where(None, 8, None), self.options.unique_deck_win_goal.value)

        elif self.options.goal.value == Goal.option_clear_challenges:
            self.multiworld.completion_condition[self.player] = lambda state: \
                can_reach_count(state, challenge_complete_locations,
                                self.options.number_of_challenges_for_goal.value)

    def fill_slot_data(self) -> Dict[str, Any]:
        return self.fill_json_data()

    def fill_json_data(self) -> Dict[str, Any]:
        min_price = self.options.minimum_price.value
        max_price = self.options.maximum_price.value
        if min_price > max_price:
            min_price, max_price = max_price, min_price

        created_regions = self.multiworld.get_regions(self.player)
        created_regions = list(
            map(lambda region: region.name, created_regions))

        def get_addresses_from_region(region: str):
            return list(map(lambda location: location.address, self.get_region(region).locations)) if (region in created_regions) else [],

        base_data = {
            "goal": self.options.goal.value,
            "ante_win_goal": self.options.ante_win_goal.value,
            "decks_win_goal": self.options.decks_win_goal.value,
            "unique_deck_win_goal": self.options.unique_deck_win_goal.value,
            "jokers_unlock_goal": self.options.jokers_unlock_goal.value,
            "required_stake": stake_to_number[self.required_stake],
            "included_stakes": [stake_to_number.get(key) for key in self.playable_stakes],
            "included_decks": [deck_name_to_key.get(key) for key in self.playable_decks],
            "stake1_shop_locations": get_addresses_from_region("Shop White Stake")[0],
            "stake2_shop_locations": get_addresses_from_region("Shop Red Stake")[0],
            "stake3_shop_locations": get_addresses_from_region("Shop Green Stake")[0],
            "stake4_shop_locations": get_addresses_from_region("Shop Black Stake")[0],
            "stake5_shop_locations": get_addresses_from_region("Shop Blue Stake")[0],
            "stake6_shop_locations": get_addresses_from_region("Shop Purple Stake")[0],
            "stake7_shop_locations": get_addresses_from_region("Shop Orange Stake")[0],
            "stake8_shop_locations": get_addresses_from_region("Shop Gold Stake")[0],
            "consumable_pool_locations": [key for key, _ in self.consumable_locations.items()],
            "jokerbundles": self.joker_bundles,
            "tarot_bundles": self.tarot_bundles,
            "planet_bundles": self.planet_bundles,
            "spectral_bundles": self.spectral_bundles,
            "minimum_price": min_price,
            "maximum_price": max_price,
            "deathlink": bool(self.options.deathlink),
            "forceyaml": bool(self.options.forceyaml),
            "stake_unlock_mode": self.options.stake_unlock_mode.value,
            "remove_jokers": bool(self.options.remove_or_debuff_jokers),
            "remove_consumables": bool(self.options.remove_or_debuff_consumables),
            "distributed_fillers": self.distributed_fillers,
            "only_boss_blinds": bool(self.options.only_boss_blinds_are_checks),
            "import_licences": self.options.import_licenses.value,
            "excluded_challenges": [key for key in self.options.exclude_challenges.value]
        }
        return base_data
