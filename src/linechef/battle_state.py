from dataclasses import dataclass
import re
import sqlite3
from linechef.pokemon import Pokemon


@dataclass
class BattleState:
    opponent_name: str
    opponent_id: int
    opponent_gauntlet_id: int
    opponent_b2b_id: int
    battle_type: int

    @staticmethod
    def find_by_route_and_name(route: str, trainer_name: str) -> "BattleState | None":
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

        poke = Pokemon.get_pokemon_by_trainer_id(trainer_id=first_trainer_id)

        breakpoint()
