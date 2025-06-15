from dataclasses import dataclass
from typing import Any, Dict, List, Tuple
from linechef import poketype
from linechef.pokemove import Pokemove
import sqlite3
import os
import re
from linechef.pokenature import get_pokenature_by_id
from linechef.learnset_into_db import adjust_pokemon_name, adjust_move_name


LUA_REGEX = r"(?P<species>[\S]+)( @ (?P<item>.+))?\nAbility: (?P<ability>.+\n)Level: (?P<level>\d{1,3}\n)(?P<nature>\w+) Nature\nIVs: (?P<hp_iv>\d{1,2}) HP / (?P<attack_iv>\d{1,2}) Atk / (?P<defense_iv>\d{1,2}) Def / (?P<spattack_iv>\d{1,2}) SpA / (?P<spdefense_iv>\d{1,2}) SpD / (?P<speed_iv>\d{1,2}) Spe\n- (?P<move1>.+)\n(- (?P<move2>.+)\n)?(- (?P<move3>.+)\n)?(- (?P<move4>.+)\n)?\n?"


@dataclass
class Pokemon:
    name: str
    type1: int
    type2: int | None
    level: int
    ability: str
    nature: int
    held_item: str
    hp: int
    attack: int
    defense: int
    spattack: int
    spdefense: int
    speed: int
    move_list: List[Pokemove]

    def __post_init__(self):
        self.current_hp = self.hp
        self.stat_modifiers = [0] * 7
        self.status = "Healthy"

    def get_speed(self, worst_case: bool = False) -> int:
        ...

    def get_functional_speed(self, worst_case: bool) -> int:
        """This generates a speed value for the worst case scenario, accounting for

        Args:
            worst_case (bool): _description_

        Returns:
            int: _description_
        """
        ...

    def get_level(self) -> int:
        ...

    def get_effective_attack(self, damage_class: str) -> Tuple[int, int]:
        ...

    def get_effective_defense(self, damage_class: str) -> Tuple[int, int]:
        ...

    def stab_multiplier(self, attack_type: int) -> float:
        ...

    def get_type1(self) -> poketype.Poketype:
        ...

    def get_type2(self) -> poketype.Poketype | None:
        ...

    def get_burn_multiplier(self, damage_class: str) -> float:
        ...

    def is_poisoned(self) -> bool:
        ...

    def get_berry_multiplier(self, move_type: poketype.Poketype) -> float:
        ...

    def get_current_hp(self) -> int:
        ...

    def get_hp(self) -> int:
        ...

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def calculate_damage_rolls(self, target_pokemon: "Pokemon", weather: str | None = None, is_doubles: bool = False,
                               reflect_screen_up: bool = False,
                               light_screen_up: bool = False,
                               aurora_veil_up: bool = False
                               ) -> Dict[Pokemove, Tuple[List[int], List[int]]]:

        damage_rolls: Dict[Pokemove, Tuple[List[int], List[int]]] = {}

        for move in self.move_list:

            if move.damage_class == "status":
                # This is explicitly for damage roll calculation
                continue

            level: int = self.get_level()

            effective_attack, effective_attack_crit = self.get_effective_attack(
                damage_class=move.damage_class)

            effective_defense, effective_defense_crit = target_pokemon.get_effective_defense(
                damage_class=move.damage_class)

            # Spread damage multiplier?
            if move.target == "all-opponents" and is_doubles:
                target_multiplier = 0.75
            else:
                target_multiplier = 1.0

            # Weather
            if weather is None:
                weather_mult = 1.0
            elif weather == "Rain" and move.poketype == poketype.Poketype.WATER:
                weather_mult = 1.5
            elif weather == "Rain" and move.poketype == poketype.Poketype.FIRE:
                weather_mult = 0.5
            elif weather == "Harsh Sunlight" and move.poketype == poketype.Poketype.WATER:
                weather_mult = 0.5
            elif weather == "Harsh Sunlight" and move.poketype == poketype.Poketype.FIRE:
                weather_mult = 1.0
            else:
                weather_mult = 1.0
                breakpoint()

            # STAB
            stab_multiplier: float = self.stab_multiplier(
                attack_type=move.poketype)

            # Freeze-Dry
            # Flying press?

            # Burn
            burn_multiplier: float = self.get_burn_multiplier(
                damage_class=move.damage_class)

            # Other multipliers
            type_effectiveness = poketype.Poketype.type_effectiveness(
                attack_type=move.poketype,
                defense_type1=target_pokemon.get_type1(),
                defense_type2=target_pokemon.get_type2(),
            )

            # Critical hits
            if target_pokemon.ability == "Battle Armor" or target_pokemon.ability == "Shell Armor":
                noncritical_multiplier = 1.0
                critical_multiplier = 1.0

            elif move.movename in ["storm-throw", "frost-breath", "zippy-zap", "surging-strikes", "wicked-blow", "flower-trick"]:
                noncritical_multiplier = 1.5
                critical_multiplier = 1.5

            elif self.ability == "Sniper":
                noncritical_multiplier = 1.0
                critical_multiplier = 2.25

            elif target_pokemon.is_poisoned() and self.ability == "Merciless":
                noncritical_multiplier = 1.5
                critical_multiplier = 1.5
            elif move.movename == "Future Sight":
                noncritical_multiplier = 1.0
                critical_multiplier = 1.0
            else:
                noncritical_multiplier = 1.0
                critical_multiplier = 1.5

            # Berries
            berry_multiplier = target_pokemon.get_berry_multiplier(
                move_type=poketype.Poketype(value=move.poketype))

            # TODO: finish "other" category as needed
            # Minimize
            minimize_multiplier = 1

            # Screens
            # Not Infiltrator
            if self.ability == "Infiltrator":
                screens_multiplier = 1

            # Reflect
            elif reflect_screen_up and move.damage_class == "physical":
                screens_multiplier = 0.5

            # Light Screen
            elif light_screen_up and move.damage_class == "special":
                screens_multiplier = 0.5

            # Aurora Veil
            elif aurora_veil_up:
                screens_multiplier = 0.5

            else:
                screens_multiplier = 1.0

            # Multiscale
            if target_pokemon.ability == "Multiscale" and target_pokemon.get_current_hp() == target_pokemon.get_hp():
                multiscale_multiplier = 0.5
            else:
                multiscale_multiplier = 1.0

            # Fluffy
            fluffy_multiplier = 1.0

            # Punk Rock
            punk_rock_multiplier = 1.0

            # Friend Guard
            friend_guard_multiplier = 1.0

            # Filter, Solid Rock, Tinted Lens
            if type_effectiveness > 1.0 and self.ability != "Mold Breaker" and (target_pokemon.ability == "Solid Rock" or target_pokemon.ability == "Filter"):
                opponent_ability_multiplier = 0.75
            elif type_effectiveness > 1.0 and self.held_item == "Expert Belt":
                opponent_ability_multiplier = 1.2
            elif type_effectiveness < 1 and self.ability == "Tinted Lens":
                opponent_ability_multiplier = 2
            else:
                opponent_ability_multiplier = 1

            # Metronome

            # Random
            random_multipliers: List[int] = [i for i in range(85, 101)]

            # # Multihit moves? -> save for elsewhere calculations
            # if move.min_hits is None or move.max_hits is None:
            #     multihit_multipliers = [1]
            # elif self.ability == "Skill Link":
            #     multihit_multipliers = [move.max_hits]
            # else:
            #     multihit_multipliers = [i for i in range(
            #         self.min_hits, self.max_hits + 1)]

            power_level_base = 2 + 2 * level / 5 * move.power / 50
            base_damage = 2 + power_level_base * effective_attack // effective_defense
            base_damage_crit = 2 + power_level_base * \
                effective_attack_crit // effective_defense_crit

            static_multipliers = target_multiplier * weather_mult * stab_multiplier * \
                burn_multiplier * berry_multiplier * minimize_multiplier * screens_multiplier * \
                multiscale_multiplier * fluffy_multiplier * \
                punk_rock_multiplier * friend_guard_multiplier * opponent_ability_multiplier

            crit_total = (base_damage_crit *
                          critical_multiplier * static_multipliers) // 1
            base_total = (base_damage * noncritical_multiplier *
                          static_multipliers) // 1

            damage_rolls[move] = (
                [int((roll * base_total) // 100)
                 for roll in random_multipliers],
                [int((roll * crit_total) // 100)
                 for roll in random_multipliers],
            )

        return damage_rolls

    @staticmethod
    def get_pokemon_by_trainer_id(trainer_id: int) -> List["Pokemon"]:
        db = sqlite3.connect("db/rnb.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        pokemon_list: List[Pokemon] = []

        # See if matching trainer id
        num_pokemon, = cursor.execute(
            "SELECT COUNT(poke_id) FROM pokemon WHERE trainer_id = (?);",
            (trainer_id, )
        ).fetchone()

        if num_pokemon <= 0 or num_pokemon > 6:
            breakpoint()
            raise Exception(
                f"[pokemon] Found an invalid number of matching pokemon ({num_pokemon})")

            # Get lead pokemon
        with open("db/sqls/get_pokemon_by_trainer_id.sql", "r") as f:
            query = f.read()
            lead_pokemon = cursor.execute(
                query, (trainer_id, True)).fetchall()
            remaining_pokemon = cursor.execute(
                query, (trainer_id, False)).fetchall()

            if len(lead_pokemon) == 0:
                breakpoint()
                raise Exception(
                    f"[pokemon] Unable to find lead pokemon for trainer {trainer_id}")

        # Calculate stats, add to pokemon_list

        lead_mon = Pokemon.get_pokemon_from_dict(dict(lead_pokemon[0]))
        pokemon_list.append(lead_mon)

        for mon in remaining_pokemon:
            pokemon_list.append(
                Pokemon.get_pokemon_from_dict(dict(mon))
            )

        return pokemon_list

    @staticmethod
    def get_pokemon_from_file(filename: str) -> List['Pokemon']:
        if not os.path.exists(filename):
            raise Exception(f"[pokemon] File {filename} does not exist.")

        with open(filename, "r") as f:
            pokemon_list = f.read()

        team_list: List[Pokemon] = []
        for m in re.finditer(LUA_REGEX, pokemon_list):
            team_list.append(
                Pokemon.get_pokemon_from_lua_dict(m.groupdict())
            )

        return team_list

    @staticmethod
    def find_by_route_and_name(route: str, trainer_name: str) -> Tuple[List["Pokemon"], int]:
        db = sqlite3.connect(database="db/rnb.db")

        cursor = db.cursor()

        with open("db/sqls/get_trainer_id_by_route_and_name.sql", "r") as f:
            query_get_trainer_id: str = f.read()

        trainer_id = cursor.execute(
            query_get_trainer_id, (f"%{trainer_name}%", f"%{route}%")).fetchall()

        if len(trainer_id) == 0:
            raise Exception(f"[battle_state] Unable to find trainer {
                            trainer_name} on route {route}")

        first_trainer_id, = trainer_id[0]

        poke = Pokemon.get_pokemon_by_trainer_id(
            trainer_id=first_trainer_id)

        return poke, first_trainer_id

    @staticmethod
    def calculate_hp(base_hp: int, iv: int, level: int) -> int:
        numerator: int = (2 * base_hp + iv) * level
        hp: int = numerator // 100 + level + 10
        return hp

    @staticmethod
    def calculate_stat(base_stat: int, iv: int, level: int, nature: int) -> int:
        numerator: int = (2 * base_stat + iv) * level
        stat: int = numerator // 100 + 5
        # Nature given as either 100 (neutral), 90 (lower), or 110 (higher)
        nature_stat: int = (stat * nature) // 100
        return nature_stat

    @staticmethod
    def get_pokemon_from_dict(poke_dict: Dict[str, Any]) -> "Pokemon":
        return_dict = {}

        # Basic things stay the same
        for item in ["name", "type1", "type2", "nature", "held_item", "ability"]:
            if item in poke_dict:
                return_dict[item] = poke_dict[item]
            else:
                return_dict[item] = None

            # Calculate the stats
            return_dict["level"] = poke_dict["pokelevel"]
            return_dict["hp"] = Pokemon.calculate_hp(
                poke_dict["base_hp"], 31, poke_dict["pokelevel"])

        for i, stat in enumerate(["attack", "defense", "spattack", "spdefense", "speed"]):

            return_dict[stat] = Pokemon.calculate_stat(
                base_stat=poke_dict[f"base_{stat}"],
                iv=31 if f"{stat}_iv" not in poke_dict else poke_dict[f"{stat}_iv"],
                level=poke_dict["pokelevel"],
                nature=get_pokenature_by_id(
                    nature_id=poke_dict["nature"], stat_num=i)
            )

        # Get the move list and modifiers
        return_dict["move_list"] = [Pokemove.get_pokemove_by_id(id)
                                    for k, id in poke_dict.items()
                                    if str(k).startswith("move") and id is not None]

        return Pokemon(**return_dict)

    @staticmethod
    def get_pokemon_from_lua_dict(poke_dict: Dict[str, Any]) -> "Pokemon":
        db = sqlite3.connect("db/rnb.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        return_dict = {}
        # Name
        return_dict["name"] = adjust_pokemon_name(poke_dict["species"])

        # Types
        result = cursor.execute("SELECT * FROM species_stat WHERE name = (?)",
                                (return_dict["name"],)).fetchone()

        if result is None:
            breakpoint()

        return_dict["type1"] = result["type1"]
        return_dict["type2"] = result["type2"]

        # Nature
        nature = dict(cursor.execute(
            "SELECT id FROM pokenature WHERE name = (?)", (poke_dict["nature"], )).fetchone())
        return_dict["nature"] = nature["id"]

        # Held Item?
        return_dict["held_item"] = poke_dict["item"]

        # Ability
        return_dict["ability"] = str(
            poke_dict["ability"]).strip()

        # Level
        return_dict["level"] = int(
            str(poke_dict["level"]).strip())

        # IVs
        return_dict["hp"] = Pokemon.calculate_hp(
            result["base_hp"], int(poke_dict["hp_iv"]), return_dict["level"])

        for i, stat in enumerate(["attack", "defense", "spattack", "spdefense", "speed"]):
            return_dict[stat] = Pokemon.calculate_stat(
                base_stat=result[f"base_{stat}"],
                iv=31 if f"{stat}_iv" not in poke_dict else int(
                    poke_dict[f"{stat}_iv"]),
                level=return_dict["level"],
                nature=get_pokenature_by_id(
                    nature_id=nature["id"], stat_num=i)
            )

        # Moves
        move_ids = []
        for i in range(1, 5):
            if f"move{i}" in poke_dict:
                m = dict(cursor.execute("SELECT id FROM pokemove WHERE movename = (?)",
                                        (adjust_move_name(poke_dict[f"move{i}"]), )).fetchone())
                move_ids.append(m["id"])

        # Get the move list and modifiers
        return_dict["move_list"] = [
            Pokemove.get_pokemove_by_id(id) for id in move_ids]

        return Pokemon(**return_dict)
