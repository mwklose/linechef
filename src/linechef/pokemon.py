from dataclasses import dataclass
from typing import Any, Dict, List
from linechef.pokemove import Pokemove
import sqlite3
import os
import re
from linechef.pokenature import get_pokenature_by_id

LUA_REGEX = r"(?P<species>\w+)(\n| @ (?P<item>.+))?\nAbility: (?P<ability>.+\n)Level: (?P<level>\d{1,3}\n)(?P<nature>\w+) Nature\nIVs: (?P<hp_iv>\d{1,2}) HP / (?P<atk_iv>\d{1,2}) Atk / (?P<def_iv>\d{1,2}) Def / (?P<spa_iv>\d{1,2}) SpA / (?P<spd_iv>\d{1,2}) SpD / (?P<spe_iv>\d{1,2}) Spe\n- (?P<move1>.+)\n(- (?P<move2>.+)\n)?(- (?P<move3>.+)\n)?(- (?P<move4>.+)\n)?\n?"



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
        ...

    @staticmethod
    def get_pokemon_by_trainer_id(trainer_id: int) -> List["Pokemon"]:
        db = sqlite3.connect("db/rnb.db")
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        pokemon_list: List[Pokemon] = []

        # See if matching trainer id
        num_pokemon,  = cursor.execute(
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
            lead_pokemon = cursor.execute(query, (trainer_id, True)).fetchall()
            remaining_pokemon = cursor.execute(query, (trainer_id, False)).fetchall()

        if len(lead_pokemon) == 0:
            breakpoint()
            raise Exception(
                f"[pokemon] Unable to find lead pokemon for trainer {trainer_id}")

        # Calculate stats, add to pokemon_list

        lead_mon = get_pokemon_from_dict(dict(lead_pokemon[0]))
        pokemon_list.append(lead_mon)

        for mon in remaining_pokemon: 
            pokemon_list.append(
                get_pokemon_from_dict(dict(mon))
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
            breakpoint()


            ... 
        
        ...

def calculate_hp(base_hp: int, iv: int, level: int) -> int: 
    numerator: int = (2 * base_hp + iv) * level
    hp: int = numerator // 100 + level + 10
    return hp

def calculate_stat(base_stat: int, iv: int, level: int, nature: int) -> int: 
    numerator: int = (2 * base_stat + iv) * level
    stat: int = numerator // 100 + 5
    # Nature given as either 100 (neutral), 90 (lower), or 110 (higher)
    nature_stat: int = (stat * nature) // 100
    return nature_stat


def get_pokemon_from_dict(poke_dict: Dict[str, Any]) -> Pokemon:
    return_dict = {}

    # Basic things stay the same
    for item in ["name", "type1", "type2", "nature", "held_item", "ability"]:
        if item in poke_dict:
            return_dict[item] = poke_dict[item]
        else: 
            return_dict[item] = None
    
    # Calculate the stats
    return_dict["level"] = poke_dict["pokelevel"]
    return_dict["hp"] = calculate_hp(poke_dict["base_hp"], 31, poke_dict["pokelevel"])

    

    for i, stat in enumerate(["attack", "defense", "spattack", "spdefense", "speed"]): 
        
        return_dict[stat] = calculate_stat(
            base_stat=poke_dict[f"base_{stat}"], 
            iv=31 if f"{stat}_iv" not in poke_dict else poke_dict[f"{stat}_iv"], 
            level=poke_dict["pokelevel"], 
            nature=get_pokenature_by_id(nature_id=poke_dict["nature"], stat_num=i)
        )

    # Get the move list and modifiers
    return_dict["move_list"] = [Pokemove.get_pokemove_by_id(id) 
                                for k, id in poke_dict.items() 
                                if str(k).startswith("move") and id is not None]
    return Pokemon(**return_dict)

def get_pokemon_from_lua_dict(poke_dict: Dict[str, Any]) -> Pokemon:
    db = sqlite3.connect("db/rnb.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    # TODO: continue here
    # Name

    # Types

    # Nature

    # Held Item?

    # Ability

    # Level

    # IVs

    # Moves

    # Construct into Dataclass
 
    return_dict = {}

    # Basic things stay the same
    for item in ["name", "type1", "type2", "nature", "held_item", "ability"]:
        if item in poke_dict:
            return_dict[item] = poke_dict[item]
        else: 
            return_dict[item] = None
    
    # Calculate the stats
    return_dict["level"] = poke_dict["pokelevel"]
    return_dict["hp"] = calculate_hp(poke_dict["base_hp"], 31, poke_dict["pokelevel"])

    

    for i, stat in enumerate(["attack", "defense", "spattack", "spdefense", "speed"]): 
        
        return_dict[stat] = calculate_stat(
            base_stat=poke_dict[f"base_{stat}"], 
            iv=31 if f"{stat}_iv" not in poke_dict else poke_dict[f"{stat}_iv"], 
            level=poke_dict["pokelevel"], 
            nature=get_pokenature_by_id(nature_id=poke_dict["nature"], stat_num=i)
        )

    # Get the move list and modifiers
    return_dict["move_list"] = [Pokemove.get_pokemove_by_id(id) 
                                for k, id in poke_dict.items() 
                                if str(k).startswith("move") and id is not None]
    return Pokemon(**return_dict)
  