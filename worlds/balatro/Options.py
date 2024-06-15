from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict
from Options import DefaultOnToggle, PerGameCommonOptions, Toggle, Range, Choice

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

class IncludeStakes(Range):
    """Number of Stakes that can have important checks: 
    1 is White Stake, 2 is White and Green Stake, etc"""
    display_name = "Include Stakes to have important Checks"
    range_start = 1
    range_end = 8
    default = 2

class DecksUnlockedFromStart(Range):
    """Number of decks you want to start with."""
    display_name = "Number of starting decks"
    range_start = 0
    range_end = 15
    default = 1


class DeathLink(Toggle):
    """When your run ends, everybody will die. When somebody else dies, your run will end."""
    display_name = "Death Link"


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
    decks_unlocked : DecksUnlockedFromStart
