from enum import IntEnum
from tokenize import Pointfloat


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
        attack = Poketype(attack_type)
        defense1 = Poketype(defense_type1)

        primary_effectiveness = POKETYPE_EFFECTIVENESS[attack].get(
            defense1, 1.0)

        if scrappy and primary_effectiveness == 0 and defense1 == Poketype.GHOST:
            primary_effectiveness = 1.0

        if defense_type2 is not None:
            defense2 = Poketype(defense_type2)

            # TODO: handle dual types
            secondary_effectiveness = POKETYPE_EFFECTIVENESS[attack].get(
                defense2, 1.0)
            if scrappy and secondary_effectiveness == 0 and defense2 == Poketype.GHOST:
                secondary_effectiveness = 1.0

            return primary_effectiveness * secondary_effectiveness

        return primary_effectiveness


POKETYPE_EFFECTIVENESS: dict[Poketype, dict[Poketype, float]] = {
    Poketype.NORMAL: {Poketype.ROCK: 0.5, Poketype.GHOST: 0, Poketype.STEEL: 0.5},
    Poketype.FIRE: {Poketype.FIRE: 0.5, Poketype.WATER: 0.5, Poketype.GRASS: 2, Poketype.ICE: 2, Poketype.BUG: 2, Poketype.ROCK: 0.5, Poketype.DRAGON: 0.5, Poketype.STEEL: 2},
    Poketype.WATER: {Poketype.FIRE: 2, Poketype.WATER: 0.5, Poketype.GRASS: 0.5, Poketype.GROUND: 2, Poketype.ROCK: 2, Poketype.DRAGON: 0.5},
    Poketype.ELECTRIC: {Poketype.WATER: 2, Poketype.ELECTRIC: 0.5, Poketype.GRASS: 0.5, Poketype.GROUND: 0, Poketype.FLYING: 2, Poketype.DRAGON: 0.5},
    Poketype.GRASS: {Poketype.FIRE: 0.5, Poketype.WATER: 2, Poketype.GRASS: 0.5, Poketype.POISON: 0.5, Poketype.GROUND: 2, Poketype.FLYING: 0.5, Poketype.BUG: 0.5, Poketype.ROCK: 2, Poketype.DRAGON: 0.5, Poketype.STEEL: 0.5},
    Poketype.ICE: {Poketype.FIRE: 0.5, Poketype.WATER: 0.5, Poketype.GRASS: 2, Poketype.ICE: 0.5, Poketype.GROUND: 2, Poketype.FLYING: 2, Poketype.DRAGON: 2, Poketype.STEEL: 0.5},
    Poketype.FIGHTING: {Poketype.NORMAL: 2, Poketype.ICE: 2, Poketype.POISON: 0.5, Poketype.FLYING: 0.5, Poketype.PSYCHIC: 0.5, Poketype.BUG: 0.5, Poketype.ROCK: 2, Poketype.GHOST: 0, Poketype.DARK: 2, Poketype.STEEL: 2, Poketype.FAIRY: 0.5},
    Poketype.POISON: {Poketype.GRASS: 2, Poketype.POISON: 0.5, Poketype.GROUND: 0.5, Poketype.ROCK: 0.5, Poketype.GHOST: 0.5, Poketype.STEEL: 0, Poketype.FAIRY: 2},
    Poketype.GROUND: {Poketype.FIRE: 2, Poketype.ELECTRIC: 2, Poketype.GRASS: 0.5, Poketype.POISON: 2, Poketype.FLYING: 0, Poketype.BUG: 0.5, Poketype.ROCK: 2, Poketype.STEEL: 2},
    Poketype.FLYING: {Poketype.ELECTRIC: 0.5, Poketype.GRASS: 2, Poketype.FIGHTING: 2, Poketype.BUG: 2, Poketype.ROCK: 0.5, Poketype.STEEL: 0.5},
    Poketype.PSYCHIC: {Poketype.FIGHTING: 2, Poketype.POISON: 2, Poketype.PSYCHIC: 0.5, Poketype.DARK: 0, Poketype.STEEL: 0.5},
    Poketype.BUG: {Poketype.FIRE: 0.5, Poketype.GRASS: 2, Poketype.FIGHTING: 0.5, Poketype.POISON: 0.5, Poketype.FLYING: 0.5, Poketype.PSYCHIC: 2, Poketype.GHOST: 0.5, Poketype.DARK: 2, Poketype.STEEL: 0.2, Poketype.FAIRY: 0.5},
    Poketype.ROCK: {Poketype.FIRE: 2, Poketype.ICE: 2, Poketype.FIGHTING: 0.5, Poketype.GROUND: 0.5, Poketype.FLYING: 2, Poketype.BUG: 2, Poketype.STEEL: 0.5},
    Poketype.GHOST: {Poketype.NORMAL: 0, Poketype.PSYCHIC: 2, Poketype.GHOST: 2, Poketype.DARK: 0.5},
    Poketype.DRAGON: {Poketype.DRAGON: 2, Poketype.STEEL: 0.5, Poketype.FAIRY: 0},
    Poketype.DARK: {Poketype.FIGHTING: 0.5, Poketype.PSYCHIC: 2, Poketype.GHOST: 2, Poketype.DARK: 0.5, Poketype.FAIRY: 0.5},
    Poketype.STEEL: {Poketype.FIRE: 0.5, Poketype.WATER: 0.5, Poketype.ELECTRIC: 0.5, Poketype.ICE: 2, Poketype.ROCK: 2, Poketype.STEEL: 0.5, Poketype.FAIRY: 2},
    Poketype.FAIRY: {Poketype.FIRE: 0.5, Poketype.FIGHTING: 2, Poketype.POISON: 0.5,
                     Poketype.DRAGON: 2, Poketype.DARK: 2, Poketype.STEEL: 0.5}
}
