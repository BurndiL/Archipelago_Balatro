from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict, Dict
from BaseClasses import Item
from .Items import item_table, is_joker, stake_to_number, number_to_stake
from .Locations import max_shop_items, max_consumable_items
from Options import DefaultOnToggle, OptionSet, PerGameCommonOptions, Toggle, Range, Choice, Option, FreeText, Visibility
from .BalatroDecks import deck_id_to_name, challenge_id_to_name


class Goal(Choice):
    """Goal for this playthrough
        Beat Decks: Win with the specified amount of Decks 
        Unlock Jokers: Unlock the specified amount of Jokers
        Beat Ante: Beat the specified Ante (can be higher than 8)
        Beat Decks on Stake: Win with the specified amount of Decks on the specified Stake (or harder)
        Win with Jokers on Stake: Win with the specified amount of Jokers on the specified Stake (or harder)
        Unique Wins: Win with the specified amount of unique combinations of Decks and Stakes     
        Clear Challenges: Complete a set amount of challenges              
    """
    display_name = "Goal"
    option_beat_decks = 0
    option_unlock_jokers = 1
    option_beat_ante = 2
    option_beat_decks_on_stake = 3
    option_win_with_jokers_on_stake = 4
    option_beat_unique_decks = 5
    option_clear_challenges = 6
    default = option_beat_decks


class BeatAnteToWin(Range):
    """If your goal is 'beat ante,' specify the ante you need to beat.
    If your goal isn't 'beat ante', you can ignore this setting."""
    display_name = "Required ante to beat"
    range_start = 1
    range_end = 38
    default = 12


class DecksToWin(Range):
    """If your goal is 'beat Decks' or 'beat decks on stake', specify the number of wins you need to beat.
    If your goal isn't "beat decks" or "beat decks on stake", you can ignore this setting"""
    display_name = "Required decks to win"
    range_start = 1
    range_end = 15
    default = 4


class UniqueDeckWins(Range):
    """If your goal is 'beat unique decks', specify the number of unique decks you need to beat
    This setting can be ignored if your goal isn't "beat unique decks"""
    display_name = "Required unique deck wins for goal"
    range_start = 1
    range_end = 120
    default = 4


class JokerGoal(Range):
    """Number of jokers you need to collect to win.
    If your goal isn't 'unlock jokers' or 'Win with jokers on stake', this setting can be ignored. """
    display_name = "Required jokers to win"
    range_start = 1
    range_end = 150
    default = 75


class RequiredStakeForGoal(OptionSet):
    """The required stake for your goal.
    If no stake is specified or the stake specified is not in the playable stakes it will default to the highest playable one.
    If your goal isn't 'Win with jokers on stake' or 'beat decks on stake', this setting can be ignored."""
    display_name = "Required Stake for goal"
    default = ['White Stake']
    valid_keys = [key for key, _ in stake_to_number.items()]


class ChallengesForGoal(Range):
    """The amount of challenges you need to complete to reach the goal.
    Make sure you don't exclude too many challenges to make this impossible.
    If your goal isn't 'clear challenges', this setting can be ignored."""
    display_name = "Amount of challenges for goal"
    default = 10
    range_start = 1
    range_end = 20


class JokerBundles(Toggle):
    """Rather than handling each joker as an individual item, you can group them into bundles for quicker progress 
    and fewer items to manage in the world. When enabled, all 150 jokers will be placed into randomly generated bundles. 
    You can also specify the size of these joker bundles"""
    display_name = "Joker Bundles"


class JokerBundleSize(Range):
    """Specify the size of Joker Bundles."""
    display_name = "Joker Bundle Size"
    range_start = 5
    range_end = 30
    default = 10


class TarotBundle(Choice):
    """Instead of making every tarot card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Tarot Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2


class CustomTarotBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every tarot, otherwise it won't work (there is no proper check for this so PLEASE double or triple check yourself). 
    If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Tarot". Here is a list of all Tarot cards https://balatrogame.fandom.com/wiki/Tarot_Cards.
    The Syntax of this is the following: ['The Fool;The Magician;The High Priestess;The Empress;The Emperor', ...] where the bundles are separated by the commas.
    Make sure to use the right symbols."""
    display_name = "Custom Tarot Bundles"
    default = ["The Fool;The Magician;The High Priestess;The Empress;The Emperor", "The Hierophant;The Lovers",
               "The Chariot;Justice;The Hermit;The Wheel of Fortune;Strength;Death", "The Hanged Man;Temperance;The Devil;The Tower;The Star", "The Moon;The Sun;Judgement;The World"]


class PlanetBundle(Choice):
    """Instead of making every planet card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Planet Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2


class CustomPlanetBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every planet, otherwise it won't work. If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Belt". Here is a list of all Planet cards https://balatrogame.fandom.com/wiki/Planet_Cards.
    For the Syntax refer to Custom Tarot Bundles, it's the same here."""
    display_name = "Custom Planet Bundles"
    default = []


class SpectralBundle(Choice):
    """Instead of making every spectral card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Spectral Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2


class CustomSpectralBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every spectral, otherwise it won't work. If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Spectral". Here is a list of all Planet cards https://balatrogame.fandom.com/wiki/Spectral_Cards.
    For the Syntax refer to Custom Tarot Bundles, it's the same here."""
    display_name = "Custom Spectral Bundles"
    default = []


class RemoveOrDebuffJokers(Toggle):
    """Choose whether locked jokers should be completely removed or appear in a debuffed state. 
    Set this to true to remove them entirely, or set it to false to have them appear debuffed."""


class RemoveOrDebuffConsumables(Toggle):
    """Choose whether locked consumables should be completely removed or appear in a debuffed state. 
    Set this to true to remove them entirely, or set it to false to have them appear debuffed."""


class FillerJokers(OptionSet):
    """Which Jokers are supposed to be filler (every Joker not in this list will be considered a progressive item)
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
    ) if is_joker(key)] + ["Riff-Raff"]


class IncludeDecksMode(Choice):
    """Choose how the playable decks are determined:
    all: All decks will be playable. 
    choose: Select specific decks to be playable from the options below.
    number: Specify how many randomly selected decks will be playable."""
    display_name = "Playable Decks Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_all


class IncludeDecksList(OptionSet):
    """Select which decks will be playable in the game. 
    This option is only considered if Playable Decks is set to choose. """
    display_name = "Include selection of playable decks"
    default = [value for key, value in deck_id_to_name.items()]
    valid_keys = [value for key, value in deck_id_to_name.items()]


class IncludeDecksNumber(Range):
    """Specify how many randomly selected decks will be playable.
    This option is only considered if playable Decks is set to number. """
    display_name = "Include number of playable decks"
    range_start = 1
    range_end = 15
    default = 8


class IncludeStakesMode(Choice):
    """Choose how the playable stakes are determined.
    all: All stakes will be playable. 
    choose: Select specific stakes to be playable from the options below.
    number: Specify how many randomly selected stakes will be playable."""
    display_name = "Playable Stakes Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_choose


class IncludeStakeList(OptionSet):
    """Select specific stakes to be playable. 
    Example: ['White Stake','Red Stake','Gold Stake']
    This will make those stakes playable and remove the other ones from the game.
    (Also make sure to capitalize the first letters, it's case sensitive.)
    This option is only considered if playable Stakes is set to choose.
    """
    display_name = "Include Stakes to have important Locations"
    default = ["White Stake", "Red Stake"]
    valid_keys = [key for key, _ in stake_to_number.items()]


class IncludeStakesNumber(Range):
    """Specify how many randomly selected stakes will be playable.
    This option is only considered if playable Stakes is set to number. """
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
    """Number of AP Items that will be buyable as vouchers in the shop at each included Stake.
    So for example if you include 3 Stakes and set this option to 11, then there 
    will be 33 findable Shop Items in your game."""
    display_name = "Number of AP shop Items"
    range_start = 0
    range_end = max_shop_items
    default = 15


class MinimumShopPrice(Range):
    """The minimum price for an AP Item Voucher in the shop"""
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


class ArchipelagoConsumableItems(Range):
    """Number of items that can be received by redeeming 
    an AP planet, tarot or spectral card"""
    display_name = "Number of AP consumable items"
    range_start = 0
    range_end = max_consumable_items  # 300
    default = 100


class DecksUnlockedFromStart(Range):
    """Number of random decks you want to start with."""
    display_name = "Number of starting decks"
    range_start = 0
    range_end = 15
    default = 1


class DeathLink(Toggle):
    """When your run ends, everybody will die. When somebody else dies, your run will end."""
    display_name = "Death Link"


class ForceYaml(Toggle):
    """Some settings (like death link or remove_or_debuff_jokers etc) can be changed in-game after the fact. 
    If you want to disallow this (for a race for example) set this option to true."""
    display_name = "Force Yaml"


class OpFillerAmount(Range):
    """The amount of permanent filler items (like "+1 Hand Size") that is going to be generated.
    If you set this option to 3 for example it's going to fill the world with 3 "+1 Hand Size", 3 "+1 Joker Slot", etc."""
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


class IncludeJokerUnlocks(Choice):
    """Include the Joker Unlocks from the vanilla game as locations.
        None: Don't include Joker Unlocks as locations.
        Easy: Include only some easier/shorter Joker Unlocks.
        Medium: Medium difficulty Joker Unlocks.
        Hard: Harder Joker Unlocks.
        All: Include all Joker Unlocks."""
    display_name = "Include Joker Unlocks"
    option_include_none = 0
    option_include_easy = 1
    option_include_medium = 2
    option_include_hard = 3
    option_include_all = 4
    default = option_include_medium


class IncludeVoucherUnlocks(Choice):
    """Include the Voucher Unlocks from the vanilla game as locations.
        None: Don't include Voucher Unlocks as locations.
        Easy: Include only some easier/shorter Voucher Unlocks that aren't that much of a headache.
        Medium: Medium difficulty Voucher Unlocks.
        Hard: Harder Voucher Unlocks.
        All: Include all Voucher Unlocks."""
    display_name = "Include Voucher Unlocks"
    option_include_none = 0
    option_include_easy = 1
    option_include_medium = 2
    option_include_hard = 3
    option_include_all = 4
    default = option_include_medium


class IncludeAchievements(Choice):
    """Include the Achievements from the vanilla game as locations.
        None: Don't include achievement locations.
        Easy: Include only some achievements that aren't that much of a headache.
        All: Include all achievements, even Completionist++ and similar.

        Side-Note: Completionist+ and Completionist++ will only be included if Gold Stake is a playable stake."""
    display_name = "Include Achievements"
    option_include_none = 0
    option_include_easy = 1
    option_include_medium = 2
    option_include_hard = 3
    option_include_all = 4
    default = option_include_medium


class IncludeChallenges(Toggle):
    """Include Challenges as Locations.
        You can exclude challenges you don't want to play in the ExcludeChallenges setting.
        False: Don't include challenges as locations.
        True: Include challenges as locations.
        """
    display_name = "Include Challenges"


class ExcludeChallenges(OptionSet):
    """If you included challenges to be locations, you can exclude the ones you do not want to play (like Jokerless or Golden Needle, you know).
    These are the Challenge names: 
    "The Omelette",
    "15 Minute City",
    "Rich get Richer",
    "On a Knife's Edge",
    "X-ray Vision",
    "Mad World",
    "Luxury Tax",
    "Non-Perishable",
    "Medusa",
    "Double or Nothing",
    "Typecast",
    "Inflation",
    "Bram Poker",
    "Fragile",
    "Monolith",
    "Blast Off",
    "Five-Card Draw",
    "Golden Needle",
    "Cruelty",
    "Jokerless"    """
    display_name = "Exclude Challenges"
    valid_keys = [value for key, value in challenge_id_to_name.items()]
    default = ['Golden Needle', 'Cruelty', 'Jokerless']


class ChallengeUnlockMode(Choice):
    """If Challenges are included, decide how to unlock them.
        Vanilla: beat challenges to unlock more challenges, just how it is handled in the base game.
        Unlocks as Items: find the challenges as items in the world and if collected, the corresponding challenge can be played.
        All Unlocked: All Challenges are unlocked from the start"""
    display_name = "Challenge Unlock Mode"
    option_vanilla = 0
    option_as_items = 1
    option_all_unlocked = 2
    default = option_as_items


class OnlyBossBlindsAreChecks(Toggle):
    """Decide whether you want only Boss Blinds as locations or if you also want to include beating the small and big blinds as additional locations.
    Skipped Small and Big Blinds will be checked after beating the Boss Blind of the Ante.
    Setting this to true will only have Boss Blinds, setting it to false will also include Small and Big Blinds."""
    display_name = "Only Boss Blinds as checks"


class DiscoverJokerAsLocations(Choice):
    """Make discovering (=acquiring) Jokers Locations.
        Off: Don't add these locations.
        Non-Legendary: Add all non-legendary discoveries as Locations.
        All: Add all Joker discoveries as locations."""
    display_name = "Discover Jokers as Locations"
    option_off = 0
    option_non_legendary = 1
    option_all = 2
    default = option_non_legendary


class ModdedItems(Choice):
    """Decide what to do with items from other mods.
        Remove: Remove items from other mods during Archipelago runs.
        Unlock: Have items from other mods always unlocked.
        Include as AP Items: Have a set amount of "import licenses", the more you collect the higher
            the chance that a modded item is unlocked. These are not considered in logic but the 
            easiest way to still include items from other mods in your world."""
    display_name = "Modded Items"
    option_remove = 0
    option_unlock = 1
    option_include_as_ap_items = 2
    default = option_remove


class NumberOfImportLicenses(Range):
    """This setting will be ignored if you did not set Modded Items to "Inlude as AP Items".
        Set the amount of Import Licenses in your world.
        The more you collect, the more modded items will be unlocked."""
    display_name = "Number of Import Licenses"
    range_start = 1
    range_end = 50
    default = 15


@dataclass
class BalatroOptions(PerGameCommonOptions):

    # goals
    goal: Goal
    ante_win_goal: BeatAnteToWin
    decks_win_goal: DecksToWin
    unique_deck_win_goal: UniqueDeckWins
    jokers_unlock_goal: JokerGoal
    required_stake_for_goal: RequiredStakeForGoal
    number_of_challenges_for_goal: ChallengesForGoal

    # decks
    include_decksMode: IncludeDecksMode
    include_deckChoice: IncludeDecksList
    include_deckNumber: IncludeDecksNumber

    # stakes
    stake_unlock_mode: StakeUnlockMode
    include_stakesMode: IncludeStakesMode
    include_stakesList: IncludeStakeList
    include_stakesNumber: IncludeStakesNumber

    # Blinds
    only_boss_blinds_are_checks: OnlyBossBlindsAreChecks

    # Unlocks
    include_joker_unlocks: IncludeJokerUnlocks
    include_voucher_unlocks: IncludeVoucherUnlocks
    include_achievements: IncludeAchievements

    # Discover Locations
    discover_jokers_as_locations: DiscoverJokerAsLocations

    # Challenges
    include_challenges: IncludeChallenges
    exclude_challenges: ExcludeChallenges
    challenge_unlock_mode: ChallengeUnlockMode

    # jokers
    joker_bundles: JokerBundles
    joker_bundle_size: JokerBundleSize
    remove_or_debuff_jokers: RemoveOrDebuffJokers

    # consumables
    tarot_bundle: TarotBundle
    custom_tarot_bundles: CustomTarotBundles
    planet_bundle: PlanetBundle
    custom_planet_bundles: CustomPlanetBundles
    spectral_bundle: SpectralBundle
    custom_spectral_bundles: CustomSpectralBundles
    remove_or_debuff_consumables: RemoveOrDebuffConsumables

    # items
    decks_unlocked_from_start: DecksUnlockedFromStart
    filler_jokers: FillerJokers
    ap_consumable_items: ArchipelagoConsumableItems
    permanent_filler: OpFillerAmount
    shop_items: ShopItems
    minimum_price: MinimumShopPrice
    maximum_price: MaximumShopPrice

    # traps
    trap_amount: Traps

    # deathlink
    deathlink: DeathLink

    # misc
    modded_items: ModdedItems
    import_licenses: NumberOfImportLicenses
    forceyaml: ForceYaml
