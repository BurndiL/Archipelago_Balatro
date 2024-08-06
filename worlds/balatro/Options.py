from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict, Dict
from BaseClasses import Item
from .Items import item_table, is_joker, stake_to_number, number_to_stake
from .Locations import max_shop_items
from Options import DefaultOnToggle, OptionSet, PerGameCommonOptions, Toggle, Range, Choice, Option
from .BalatroDecks import deck_id_to_name


class Goal(Choice):
    """Goal for this playthrough
        Beat Decks: Beat Ante 8 a specific 
        Unlock Jokers: Unlock the specified amount of Jokers
        Beat Ante: Beat the specified Ante to reach the goal, can be higher than 8
        Beat Decks on Stake: The same as beat decks, but you have to beat them on a specific stake.
        Win with jokers on stake: Win with a specified amount of jokers on a specified stake.
    """
    display_name = "Goal"
    option_beat_decks = 0
    option_unlock_jokers = 1
    option_beat_ante = 2
    option_beat_decks_on_stake = 3
    option_win_with_jokers_on_stake = 4
    option_beat_unique_decks = 5
    default = option_beat_decks


class BeatAnteToWin(Range):
    """What ante you need to beat to win (if that's the selected goal), note that this can go up to 38
    This setting can be ignored if your goal isn't "beat ante" """
    display_name = "What Ante you need to beat to win"
    range_start = 1
    range_end = 38
    default = 12


class DecksToWin(Range):
    """Number of decks you need to beat to win.
    This setting can be ignored if your goal isn't "beat decks" or "beat decks on stake" """
    display_name = "How many decks to win"
    range_start = 1
    range_end = 15
    default = 4


class UniqueDeckWins(Range):
    """Number of unique deck wins you need to get.
    This setting can be ignored if your goal isn't "beat unique decks"""
    display_name = "How many unique deck wins for goal"
    range_start = 1
    range_end = 120
    default = 4


class JokerGoal(Range):
    """Number of jokers you need to win
    This setting can be ignored if your goal isn't "unlock jokers" or "Win with jokers on stake" """
    display_name = "How many jokers to win"
    range_start = 1
    range_end = 150
    default = 75


class RequiredStakeForGoal(OptionSet):
    """The required stake for your goal.
    This setting can be ignored if your goal isn't "Win with jokers on stake" or "beat decks on stake" 
    If the stake specified is not in the playable stakes it will default to the highest one."""
    display_name = "Required Stake for goal"
    default = ['White Stake']
    valid_keys = [key for key, _ in stake_to_number.items()]


class JokerBundles(Toggle):
    """Instead of making every joker an individual item, you have the option to put them into bundles, 
    resulting in faster progress and less items that need to be placed in the world.
    If set to true: All 150 joker items are put in 15 randomly generated joker bundles."""
    display_name = "Joker Bundles"


class TarotBundle(Toggle):
    """Instead of making every tarot card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    If set to true: All tarot cards are put into 1 tarot bundle"""
    display_name = "Tarot Bundle"


class PlanetBundle(Toggle):
    """Instead of making every planet card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    If set to true: All planet cards are put into 1 planet bundle"""
    display_name = "Planet Bundle"


class SpectralBundle(Toggle):
    """Instead of making every spectral card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    If set to true: All spectral cards are put into 1 spectral bundle"""
    display_name = "Spectral Bundle"


class RemoveOrDebuffJokers(Toggle):
    """Decide whether locked jokers will not appear at all, or if they will appear but in a debuffed state. 
    Setting this to true will remove them, setting this to false will debuff them."""


class RemoveOrDebuffConsumables(Toggle):
    """Decide whether locked consumables will not appear at all, or if they will appear but in a debuffed state. 
    Setting this to true will remove them, setting this to false will debuff them."""


class FillerJokers(OptionSet):
    """Which Jokers are supposed to be filler (every Joker not in this list will be considered useful)
    Be careful with this option if your goal is "Unlock Jokers"

    Valid Jokers:
        "Abstract Joker"
        "Acrobat"
        "Ancient Joker" 
        "....."

        for a full list go to https://balatrogame.fandom.com/wiki/Category:Jokers

    Example: ['Abstract Joker', 'Acrobat', 'Ancient Joker']
    """
    display_name = "Set jokers as filler"
    default = []
    valid_keys = [key for key, _ in item_table.items(
    ) if is_joker(key)] + ["Canio", "Riff-Raff"]


class IncludeDecksMode(Choice):
    """Decide how it is determined what decks will be playable.
    all: All decks will be playable. 
    choose: You can choose below what decks will be playable.
    number: You can choose how many randomly selected decks will be playable."""
    display_name = "Playable Decks Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_all


class IncludeDecksList(OptionSet):
    """Decide which decks will be playable in the game. 
    This option is only considered if Playable Decks is set to choose. """
    display_name = "Include selection of playable decks"
    default = [value for key, value in deck_id_to_name.items()]
    valid_keys = [value for key, value in deck_id_to_name.items()]


class IncludeDecksNumber(Range):
    """Decide how many decks will be playable in the game.
    This option is only considered if Playable Decks is set to number. """
    display_name = "Include number of playable decks"
    range_start = 1
    range_end = 15
    default = 8


class IncludeStakesMode(Choice):
    """Decide how it is determined what stakes will be playable.
    all: All stakes will be playable. 
    choose: You can choose below what stakes will be playable.
    number: You can choose how many randomly selected stakes will be playable."""
    display_name = "Playable Stakes Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_number


class IncludeStakeList(OptionSet):
    """Decide which stakes are playable. 
    Example: ['White Stake','Red Stake','Gold Stake']
    This will make those stakes playable and remove the other ones.
    (Also make sure to capitalize the first letters, it's case sensitive.)
    """
    display_name = "Include Stakes to have important Locations"
    default = ["White Stake", "Red Stake"]
    valid_keys = [key for key, _ in stake_to_number.items()]


class IncludeStakesNumber(Range):
    """Decide how many stakes will be playable in the game.
    This option is only considered if Playable Stakes is set to number. """
    display_name = "Include number of playable stakes"
    range_start = 1
    range_end = 8
    default = 2


class StakeUnlockMode(Choice):
    """Decide how stakes are handled by the Randomizer.
    unlocked: all stakes are unlocked from the start
    vanilla: stakes are progressively unlocked (by beating the previous stake) and in the same order as in the base game
    linear: stakes are progressively unlocked (by beating the previous stake) but in a random order
    stake_as_item: stakes can be found as items and unlock the stake for every deck
    stake_as_item_per_deck: stakes can be found as items but only unlock it for a specific deck"""
    display_name = "Stake Unlock Mode"
    option_unlocked = 0
    option_vanilla = 1
    option_linear = 2
    option_stake_as_item = 3
    option_stake_as_item_per_deck = 4
    default = option_vanilla


class ShopItems(Range):
    """Number of AP Items that will be buyable in the shop at each included Stake.
    So for example if you include 3 Stakes and set this option to 11, then there 
    will be 33 findable Shop Items in your game."""
    display_name = "Number of AP shop Items"
    range_start = 0
    range_end = max_shop_items
    default = 15


class MinimumShopPrice(Range):
    """The minimum price for an AP Item in the shop"""
    display_name = "Minimum Price of AP Item in shop"
    range_start = 1
    range_end = 50
    default = 1


class MaximumShopPrice(Range):
    """The maximum price for an AP Item in the shop"""
    display_name = "Maximum Price of AP Item in shop"
    range_start = 1
    range_end = 100
    default = 10


class DecksUnlockedFromStart(Range):
    """Number of random decks you want to start with."""
    display_name = "Number of starting decks"
    range_start = 0
    range_end = 15
    default = 1


class DeathLink(Toggle):
    """When your run ends, everybody will die. When somebody else dies, your run will end."""
    display_name = "Death Link"


class OpFillerAmount(Range):
    """The amount of permanent filler items (like "+1 Hand Size") is gonna be generated.
    If you set this option to 3 for example its gonna make 3 "+1 Hand Size", 3 "+1 Joker Slot", etc."""
    display_name = "Permanent filler amount"
    range_start = 0
    range_end = 20
    default = 4


class Traps(Choice):
    """How often traps will appear as filler items
        No traps: No traps will appear
        Low traps: 1 in 15 filler items will be traps
        Medium traps: 1 in 7 filler items will be traps
        High traps: 1 in 2 filler items will be traps
        Mayhem: Every filler item will be a trap
    """
    display_name = "Trap Frequency"
    option_no_traps = 0
    option_low_amount = 1
    option_medium_amount = 2
    option_high_amount = 3
    option_mayhem = 4
    default = option_medium_amount


@dataclass
class BalatroOptions(PerGameCommonOptions):

    # goal
    goal: Goal
    ante_win_goal: BeatAnteToWin
    decks_win_goal: DecksToWin
    unique_deck_win_goal: UniqueDeckWins
    jokers_unlock_goal: JokerGoal
    required_stake_for_goal: RequiredStakeForGoal

    # modifiers
    joker_bundles: JokerBundles
    tarot_bundle: TarotBundle
    planet_bundle: PlanetBundle
    spectral_bundle: SpectralBundle

    remove_or_debuff_jokers: RemoveOrDebuffJokers
    remove_or_debuff_consumables: RemoveOrDebuffConsumables

    # deathlink
    deathlink: DeathLink

    # decks
    include_decksMode: IncludeDecksMode
    include_deckChoice: IncludeDecksList
    include_deckNumber: IncludeDecksNumber
    decks_unlocked_from_start: DecksUnlockedFromStart

    # stakes
    stake_unlock_mode: StakeUnlockMode
    include_stakesMode: IncludeStakesMode
    include_stakesList: IncludeStakeList
    include_stakesNumber: IncludeStakesNumber

    # items
    filler_jokers: FillerJokers
    shop_items: ShopItems
    minimum_price: MinimumShopPrice
    maximum_price: MaximumShopPrice
    permanent_filler: OpFillerAmount

    # traps
    trap_amount: Traps
