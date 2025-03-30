from dataclasses import dataclass
from typing import List
from linechef.pokemove import Pokemove
import sqlite3


@dataclass
class Pokemon:
    name: str
    type1: str
    type2: str | None
    level: int
    ability: str
    nature: int
    held_item: str
    status: str
    hp: int
    attack: int
    defense: int
    spattack: int
    spdefense: int
    speed: int
    move_list: List[Pokemove]
    stat_modifiers: List[int]

    @staticmethod
    def get_pokemon_by_trainer_id(trainer_id: int) -> List["Pokemon"]:
        db = sqlite3.connect("db/rnb.db")
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

        if len(lead_pokemon) == 0:
            breakpoint()
            raise Exception(
                f"[pokemon] Unable to find lead pokemon for trainer {trainer_id}")

        # Calculate stats, add to pokemon_list

        # Get other pokemon

        # Calculate stats, add to pokemon_list

        return pokemon_list
