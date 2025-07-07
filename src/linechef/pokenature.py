from enum import IntEnum

from linechef.pokestat import PokeStat


class Pokenature(IntEnum):
    """Creates an enum matching the Database information, for easier switching between types.

    Args:
        IntEnum (_type_): Pulls from built-in IntEnum type. 
    """
    HARDY = 1
    LONELY = 2
    ADAMANT = 3
    NAUGHTY = 4
    BRAVE = 5
    BOLD = 6
    DOCILE = 7
    IMPISH = 8
    LAX = 9
    RELAXED = 10
    MODEST = 11
    MILD = 12
    BASHFUL = 13
    RASH = 14
    QUIET = 15
    CALM = 16
    GENTLE = 17
    CAREFUL = 18
    QUIRKY = 19
    SASSY = 20
    TIMID = 21
    HASTY = 22
    JOLLY = 23
    NAIVE = 24
    SERIOUS = 25


def get_pokenature_modifier(nature: Pokenature, stat_num: PokeStat) -> int:
    """
    This function gets a nature, and returns either 100, 90, or 110 for immediate use in stat calculations.
    The "order" of natures was explicitly done so that this modulo magic can happen. 
    Note that if the stat_num equals increase and decrease, this is a "neutral" nature.
    """
    increase = (nature - 1) // 5
    decrease = (nature - 1) % 5
    return 100 + 10 * (stat_num == increase) - 10 * (stat_num == decrease)


def get_pokenature_by_id(nature_id: int, stat_num: int):
    """
    This function gets a nature id, and returns either 100, 90, or 110 for immediate use in stat calculations.
    The "order" of natures was explicitly done so that this modulo magic can happen. 
    Note that if the stat_num equals increase and decrease, this is a "neutral" nature.
    """
    pn = Pokenature(nature_id)
    return get_pokenature_modifier(nature=pn, stat_num=stat_num)
