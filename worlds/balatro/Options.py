from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict
from .Items import item_table, is_joker
from Options import DefaultOnToggle, OptionSet, PerGameCommonOptions, Toggle, Range, Choice

class Goal(Choice):
    """Goal for this playthrough
        Beat Decks: Beat Ante 8 for the specified number of decks
        Unlock Jokers: Unlock the specified amount of Jokers
        Beat Ante: Beat the specified Ante to reach the goal, can be higher than 8
    """
    display_name = "Goal"
    option_beat_decks = 0
    option_unlock_jokers = 1
    option_beat_ante = 2
    default = option_beat_decks

class BeatAnteToWin(Range):
    """What ante you need to beat to win (if that's the selected goal), note that this can go up to 38"""
    display_name = "What Ante you need to beat to win"
    range_start = 1
    range_end = 38
    default = 12

class DecksToWin(Range):
    """Number of decks you need to beat to win."""
    display_name = "How many decks to win"
    range_start = 1
    range_end = 15
    default = 4

class UnlockJokersToWin(Range):
    """Number of jokers you need to win"""
    display_name = "How many jokers to win"
    range_start = 1
    range_end = 150
    default = 75

class FillerJokers(OptionSet):
    """
    Which Jokers are supposed to be filler (every Joker not in this list will be considered useful)
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
    valid_keys = [key for key, _ in item_table.items() if is_joker(key)]


class IncludeStakes(Range):
    """Number of Stakes that can contain locations:
    1 is White Stake, 2 is White and Green Stake, etc
    minimum value: 1
    maximum value: 8
    """
    display_name = "Include Stakes to have important Checks"
    range_start = 1
    range_end = 8
    default = 2

class ShopItems(Range):
    """Number of AP Checks that will be buyable in the shop""" 
    display_name = "Number of AP shop Items"
    range_start = 0
    range_end = 60
    default = 30


class MinimumShopPrice(Range):
    """The minimum price for an AP Item in the shop"""
    display_name = "Minimum Price of AP Item in shop"
    range_start = 1
    range_end = 30
    default = 1

class MaximumShopPrice(Range):
    """The maximum price for an AP Item in the shop"""
    display_name = "Maximum Price of AP Item in shop"
    range_start = 1
    range_end = 100
    default = 10


class DecksUnlockedFromStart(Range):
    """Number of decks you want to start with."""
    display_name = "Number of starting decks"
    range_start = 0
    range_end = 15
    default = 1


class DeathLink(Toggle):
    """When your run ends, everybody will die. When somebody else dies, your run will end."""
    display_name = "Death Link"


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
    # deathlink
    deathlink: DeathLink

    # goal
    goal: Goal
    ante_win_goal : BeatAnteToWin
    decks_win_goal : DecksToWin
    jokers_unlock_goal : UnlockJokersToWin

    # locations
    include_stakes : IncludeStakes

    # items
    decks_unlocked_from_start : DecksUnlockedFromStart
    filler_jokers : FillerJokers
    shop_items : ShopItems
    minimum_price : MinimumShopPrice
    maximum_price : MaximumShopPrice

    #traps 
    trap_amount : Traps
