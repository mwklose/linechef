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
    flinch_chance: int
    ailment: str
    ailment_chance: int
    crit_rate: int
    stat: str
    stat_chance: int
    drain: int
    healing: int
    min_hits: int
    max_hits: int

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
