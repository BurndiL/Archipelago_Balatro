deck_id_to_name = {
    1: "Red Deck",
    2: "Blue Deck",
    3: "Yellow Deck",
    4: "Green Deck",
    5: "Black Deck",
    6: "Magic Deck",
    7: "Nebula Deck",
    8: "Ghost Deck",
    9: "Abandoned Deck",
    10: "Checkered Deck",
    11: "Zodiac Deck",
    12: "Painted Deck",
    13: "Anaglyph Deck",
    14: "Plasma Deck",
    15: "Erratic Deck",
}

deck_name_to_key = {
    "Red Deck": "b_red",
    "Blue Deck": "b_blue",
    "Yellow Deck": "b_yellow",
    "Green Deck": "b_green",
    "Black Deck": "b_black",
    "Magic Deck": "b_magic",
    "Nebula Deck": "b_nebula",
    "Ghost Deck": "b_ghost",
    "Abandoned Deck": "b_abandoned",
    "Checkered Deck": "b_checkered",
    "Zodiac Deck": "b_zodiac",
    "Painted Deck": "b_painted",
    "Anaglyph Deck": "b_anaglyph",
    "Plasma Deck": "b_plasma",
    "Erratic Deck": "b_erratic"
}

challenge_id_to_name = {
    1: "The Omelette",
    2: "15 Minute City",
    3: "Rich get Richer",
    4: "On a Knife's Edge",
    5: "X-ray Vision",
    6: "Mad World",
    7: "Luxury Tax",
    8: "Non-Perishable",
    9: "Medusa",
    10: "Double or Nothing",
    11: "Typecast",
    12: "Inflation",
    13: "Bram Poker",
    14: "Fragile",
    15: "Monolith",
    16: "Blast Off",
    17: "Five-Card Draw",
    18: "Golden Needle",
    19: "Cruelty",
    20: "Jokerless"
}


class JokerUnlocks:
    golden_ticket = "Unlock Golden Ticket (Play a 5 card hand that only contains Gold cards)"
    mr_bones = "Unlock Mr. Bones (Lose 5 runs)"
    acrobat = "Unlock Acrobat (Play 200 hands)"
    sock_and_buskin = "Unlock Sock and Buskin (Play a total of 500 face cards)"
    swashbuckler = "Unlock Swashbuckler (Sell a total of 20 Jokers)"
    troubadour = "Unlock Troubadour (Win 5 consecutive rounds with a single hand each)"
    certificate = "Unlock Certificate (Have a gold card with a gold seal)"
    smeared_joker = "Unlock Smeared Joker (Have 3 or more wild cards in your deck)"
    throwback = "Unlock Throwback (Continue a run from the main menu)"
    hanging_chad = "Unlock Hanging Chad (Beat a Boss Blind with a high card)"
    rough_gem = "Unlock Rough Gem (Have at least 30 diamond cards in your deck)"
    bloodstone = "Unlock Bloodstone (Have at least 30 heart cards in your deck)"
    arrowhead = "Unlock Arrowhead (Have at least 30 spade cards in your deck)"
    onyx_agate = "Unlock Onyx Agate (Have at least 30 club cards in your deck)"
    glass_joker = "Unlock Glass Joker (Have 5 or more glass cards in your deck)"
    showman = "Unlock Showman (Reach Ante 4)"
    flower_pot = "Unlock Flower Pot (Reach Ante 8)"
    blueprint = "Unlock Blueprint (Win a run)"
    wee_joker = "Unlock Wee Joker (Win a run in 18 or fewer rounds)"
    merry_andy = "Unlock Merry Andy (Win a run in 12 or fewer rounds)"
    oops_all_6s = "Unlock Oops! All 6s (Earn at least 10,000 chips)"
    the_idol = "Unlock The Idol (In one hand, earn at least 1,000,000 chips)"
    seeing_double = "Unlock Seeing Double (Play a hand that contains four 7 of clubs)"
    matador = "Unlock Matador (Defeat a Boss Blind in one hand, without using discards)"
    hit_the_road = "Unlock Hit the Road (Discard 5 Jacks at the same time)"
    the_duo = "Unlock The Duo (Win a run without playing a pair)"
    the_trio = "Unlock The Trio (Win a run without playing a Three of a Kind)"
    the_family = "Unlock The Family (Win a run without playing a Four of a Kind)"
    the_order = "Unlock The Order (Win a run without playing a Straight)"
    the_tribe = "Unlock The Tribe (Win a run without playing a Flush)"
    the_stuntman = "Unlock The Stuntman (Earn 100,000,000 chips in one hand)"
    invisible_joker = "Unlock Invisible Joker (Win a run without ever having more than 4 Jokers)"
    brainstorm = "Unlock Brainstorm (Discard a Royal Flush)"
    satellite = "Unlock Satellite (Have $400 or more)"
    shoot_the_moon = "Unlock Shoot the Moon (Play every heart card in your deck in a single round)"
    drivers_license = "Unlock Driver's License (Enhance 16 cards in your deck)"
    cartomancer = "Unlock Cartomancer (Discover every Tarot card)"
    astronomer = "Unlock Astronomer (Discover every Planet card)"
    burnt_joker = "Unlock Burnt Joker (Sell a total of 50 cards)"
    bootstraps = "Unlock Bootstraps (Have at least 2 Polychrome Jokers)"
    canio = "Unlock Canio (Find Canio using The Soul)"
    triboulet = "Unlock Triboulet (Find Triboulet using The Soul)"
    yorick = "Unlock Yorick (Find Yorick using The Soul)"
    chicot = "Unlock Chicot (Find Chicot using The Soul)"
    perkeo = "Unlock Perkeo (Find Perkeo using The Soul)"


class VoucherUnlocks:
    overstock_plus = "Unlock Overstock + (Spend a total of $2500)"
    liquidation = "Unlock Liquidation (Redeem at least 10 voucher cards in one run)"
    glow_up = "Unlock Glow Up (Have at least 5 joker cards with edition effect)"
    reroll_glut = "Unlock Reroll Glut (Reroll the shop a total of 100 times)"
    omen_globe = "Unlock Omen Globe (Use a total of 25 Tarot cards from booster packs)"
    observatory = "Unlock Observatory (Use a total of 25 Planet cards from booster packs)"
    nacho_tong = "Unlock Nacho Tong (Play a total of 2500 cards)"
    recyclomancy = "Unlock Recyclomancy (Discard a total of 2500 cards)"
    tarot_tycoon = "Unlock Tarot Tycoon (Buy a total of 50 Tarot cards from the shop)"
    planet_tycoon = "Unlock Planet Tycoon (Buy a total of 50 Planet cards from the shop)"
    money_tree = "Unlock Money Tree (Max out the interest per round earnings for ten consecutive rounds)"
    antimatter = "Unlock Antimatter (Redeem Blank 10 total times)"
    illusion = "Unlock Illusion (Buy a total of 20 Playing cards from the shop)"
    petroglyph = "Unlock Petroglyph (Reach Ante level 12)"
    retcon = "Unlock Retcon (Discover 25 Blinds)"
    palette = "Unlock Palette (Reduce your hand size down to 5 cards)"


class AchievementUnlocks:
    high_stakes = "High Stakes Achievement (Clear Gold Stakes on a deck)"
    flushed = "Flushed Achievement (Play a 5 card wild card flush)"
    roi = "ROI Achievement (Buy 5 vouchers by Ante 4)"
    shattered = "Shattered Achievement (Break 2 Glass Cards in a single hand)"
    royale = "Royale Achievement (Play a Royal Flush)"
    retrograde = "Retrograde Achievement (Get any poker hand to level 10)"
    tiny_hands = "Tiny Hands Achievement (Thin your deck down to 20 or fewer cards)"
    big_hands = "Big Hands Achievement (Have 80 or more cards in your deck)"
    you_get_what_you_get = "You Get What You Get Achievement (Win a run without rerolling the shop)"
    rule_bender = "Rule Bender Achievement (Complete any challenge run)"
    rule_breaker = "Rule Breaker Achievement (Complete every challenge run)"
    legendary = "Legendary Achievement (Discover a Legendary Joker)"
    clairvoyance = "Clairvoyance Achievement (Discover every Spectral card)"
    extreme_couponer = "Extreme Couponer Achievement (Discover every Voucher)"
    completionist = "Completionist Achievement (Discover your entire collection)"
    completionist_plus = "Completionist+ Achievement (Win every deck at Gold Stake difficulty)"
    completionist_plus_plus = "Completionist++ Achievement (Earn a Gold Sticker on every Joker)"
    ante_up = "Ante Up! Achievement (Reach Ante 4)"
    ante_upper = "Ante Upper! Achievement (Reach Ante 8)"
    heads_up = "Heads Up Achievement (Win a run)"
    low_stakes = "Low Stakes Achievement (Win a run on at least Red Stakes difficulty)"
    mid_stakes = "Mid Stakes Achievement (Win a run on at least Black Stakes difficulty)"
    card_player = "Card Player Achievement (Play at least 2500 cards)"
    card_discarder = "Card Discarder Achievement (Discard at least 2500 cards)"
    nest_egg = "Nest Egg Achievement (Have $400 or more)"
    speedrunner = "Speedrunner Achievement (Win a run with 12 or fewer rounds)"
    k10 = "10K Achievement (Score 10,000 Chips in a single hand)"
    k1_000 = "1,000K Achievement (Score 100,000,000 Chips in a single hand)"
    k100_000 = "100,000K Achievement (Score 100,000,000,000 Chips in a single hand)"
    astronomy = "Astronomy Achievement (Discover every Planet Card)"
    cartomancy = "Cartomancy Achievement (Discover every Tarot Card)"

