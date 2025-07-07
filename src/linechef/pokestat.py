from enum import IntEnum


class PokeStat(IntEnum):
    """An enumeration for which stat to adjust.

    Args:
        IntEnum (_type_): _description_
    """
    ATTACK = 0
    DEFENSE = 1
    SPECIAL_ATTACK = 2
    SPECIAL_DEFENSE = 3
    SPEED = 4
    HP = 5
    EVASION = 6
