from enum import IntEnum


class Poketype(IntEnum):
    NORMAL = 1
    FIGHTING = 2
    FLYING = 3
    POISON = 4
    GROUND = 5
    ROCK = 6
    BUG = 7
    GHOST = 8
    STEEL = 9
    FIRE = 10
    WATER = 11
    GRASS = 12
    ELECTRIC = 13
    PSYCHIC = 14
    ICE = 15
    DRAGON = 16
    DARK = 17
    FAIRY = 18

    @staticmethod
    def type_effectiveness(attack_type: int, defense_type1: int, defense_type2: int | None, scrappy: bool = False) -> float:

        ...
