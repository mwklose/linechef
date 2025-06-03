from dataclasses import dataclass

import sqlite3
from typing import List, Tuple

from linechef.pokemon import Pokemon
from linechef.poketype import Poketype


@dataclass
class Pokemove:
    movename: str
    damage_class: str
    target: str
    power: int
    accuracy: int
    priority: int
    poketype: int
    flinch_chance: int
    ailment: str
    ailment_chance: int
    crit_rate: int
    stat: str
    stat_chance: int
    drain: int
    healing: int
    min_hits: int | None
    max_hits: int | None

    @staticmethod
    def get_pokemove_by_id(move_id: int | None) -> "Pokemove | None":
        if move_id is None:
            return None

        db = sqlite3.connect("db/rnb.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        movedetails = cursor.execute(
            "SELECT * FROM pokemove WHERE id == (?)", (move_id,)).fetchone()

        if movedetails is None:
            breakpoint()

        movedict = dict(movedetails)
        movedict.pop("id")

        return Pokemove(**movedict)

    def calculate_damage_rolls(self, own_pokemon: Pokemon, opponent_pokemon: List[Pokemon], weather: str | None = None) -> List[Tuple[List[int], List[int]]]:
        if self.damage_class == "status":
            # Should be impossible
            breakpoint()

        level: int = own_pokemon.get_level()

        effective_attack, effective_attack_crit = own_pokemon.get_effective_attack(
            damage_class=self.damage_class)

        effective_defenses = [o.get_effective_defense(
            self.damage_class) for o in opponent_pokemon]

        # Spread damage multiplier?
        if self.target == "all-opponents":
            target_multiplier = 0.75
        else:
            target_multiplier = 1.0

        # Weather
        if own_pokemon.ability == "Cloud Nine" or own_pokemon.ability == "Air Lock":
            weather_mult = 1.0
        elif any([o.ability == "Cloud Nine" or o.ability == "Air Lock" for o in opponent_pokemon]):
            weather_mult = 1.0
        elif weather is None:
            weather_mult = 1.0
        elif weather == "Rain" and self.poketype == Poketype.WATER:
            weather_mult = 1.5
        elif weather == "Rain" and self.poketype == Poketype.FIRE:
            weather_mult = 0.5
        elif weather == "Harsh Sunlight" and self.poketype == Poketype.WATER:
            weather_mult = 0.5
        elif weather == "Harsh Sunlight" and self.poketype == Poketype.FIRE:
            weather_mult = 1.0
        else:
            weather_mult = 1.0
            breakpoint()

        # STAB
        stab_multiplier: float = own_pokemon.stab_multiplier(
            attack_type=self.poketype)

        # Freeze-Dry
        # Flying press?

        # Burn
        burn_multiplier: float = own_pokemon.get_burn_multiplier(
            damage_class=self.damage_class)

        # Per-pokemon multipliers
        type_effectiveness_mults: List[float] = []
        noncritical_multipliers: List[float] = []
        critical_multipliers: List[float] = []
        berry_multipliers: List[float] = []
        opponent_ability_multipliers: List[float] = []

        for opp in opponent_pokemon:

            type_effectiveness = Poketype.type_effectiveness(
                attack_type=self.poketype,
                defense_type1=opp.get_type1(),
                defense_type2=opp.get_type2(),
            )

            if type_effectiveness > 1.0 and own_pokemon.ability != "Mold Breaker" and (opp.ability == "Solid Rock" or opp.ability == "Filter"):
                opponent_ability_multipliers.append(0.75)
            elif type_effectiveness > 1.0 and own_pokemon.held_item == "Expert Belt":
                opponent_ability_multipliers.append(1.2)
            elif type_effectiveness < 1 and own_pokemon.ability == "Tinted Lens":
                opponent_ability_multipliers.append(2)

            # Critical hits
            if opp.ability == "Battle Armor" or opp.ability == "Shell Armor":
                noncritical_multipliers.append(1.0)
                critical_multipliers.append(1.0)

            elif self.movename in ["storm-throw", "frost-breath", "zippy-zap", "surging-strikes", "wicked-blow", "flower-trick"]:
                noncritical_multipliers.append(1.5)
                critical_multipliers.append(1.5)

            elif own_pokemon.ability == "Sniper":
                noncritical_multipliers.append(1.0)
                critical_multipliers.append(2.25)

            elif opp.is_poisoned() and own_pokemon.ability == "Merciless":
                noncritical_multipliers.append(1.5)
                critical_multipliers.append(1.5)
            elif self.movename == "Future Sight":
                noncritical_multipliers.append(1.0)
                critical_multipliers.append(1.0)
            else:
                noncritical_multipliers.append(1.0)
                critical_multipliers.append(1.5)

            # Berries
            berry_multipliers.append(opp.get_berry_multiplier(
                move_type=Poketype(value=self.poketype)))

            # TODO: finish "other" category as needed

        # Random
        random_multipliers: List[int] = [i for i in range(85, 101)]

        # # Multihit moves? -> save for elsewhere calculations
        # if self.min_hits is None or self.max_hits is None:
        #     multihit_multipliers = [1]
        # elif own_pokemon.ability == "Skill Link":
        #     multihit_multipliers = [self.max_hits]
        # else:
        #     multihit_multipliers = [i for i in range(
        #         self.min_hits, self.max_hits + 1)]

        # TODO: Combine with itertools.product

        return [([0] * 16, [0] * 16)]
