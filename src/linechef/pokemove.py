from dataclasses import dataclass

import sqlite3


@dataclass
class Pokemove:
    movename: str
    damage_class: str
    target: str
    power: int
    accuracy: int
    priority: int
    poketype: int
    flinch_change: int
    ailment: str
    ailment_chance: int
    crit_rate: int
    stat: str
    stat_change: int
    drain: int
    healing: int
    min_hits: int
    max_hits: int

    @staticmethod
    def get_pokemove_by_id(move_id: int) -> "Pokemove":
        db = sqlite3.connect("db/rnb.db")
        cursor = db.cursor()

        movedetails, = cursor.execute(
            "SELECT * FROM pokemove WHERE id == (?)", (move_id,)).fetchone()
        breakpoint()

        return Pokemove(**movedetails)
