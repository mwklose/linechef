import os
import re
import sqlite3
from typing import Dict, Tuple

from linechef.learnset_into_db import adjust_pokemon_name, adjust_move_name, get_or_insert_move, insert_or_retrieve_pokemon_db


def get_or_insert_trainer(route_id: str, trainer_name: str, gauntlet_id: int, b2b_id: int, cursor: sqlite3.Cursor) -> Tuple[int, int, int]:
    trainer_ids = cursor.execute(
        "SELECT id, gauntlet_id, b2b_id FROM trainers WHERE name = (?) AND route = (?)", [trainer_name, route_id]).fetchall()

    if len(trainer_ids) == 1:
        return trainer_ids[0]
    elif len(trainer_ids) > 1:
        breakpoint()

    trainer_regex = r"^(?P<tname>[\w &♀♂\.1-9]+)(\W+\[(\W?(?P<db_solo>Double);?)?(\W?(?P<db_partner>Double Battle With [\w ♀♂]+);?)?(\W?(?P<gauntlet>Gauntlet);?)?(\W?(?P<b2b>B2B);?)?(\W?(?P<boss>Boss);?)?(\W?(?P<magma>Magma Storm);?)?(\W?(?P<sunny>Sunny);?)?(\W?(?P<rain>Rain);?)?(\W?(?P<thunderstorm>Thunderstorm);?)?(\W?(?P<aurora>Aurora Veil);?)?(\W?(?P<tailwind>Tailwind);?)?(\W?([\w ]+ Room);?)?(\W?(?P<partner>Partner);?)?\])?$"
    possible_match = re.search(trainer_regex, trainer_name)
    if possible_match is None:
        breakpoint()
        raise Exception(
            f"[get_or_insert_trainer] Could not match with regex ({trainer_name})")

    gd = possible_match.groupdict()
    trainer_dict = {}

    trainer_dict["route"] = route_id
    trainer_dict["name"] = gd["tname"]

    # TODO: Get Battle Type
    if gd["db_solo"] is None and gd["db_partner"] is None:
        trainer_dict["battle_type"] = 0
    elif gd["db_solo"] is not None:
        trainer_dict["battle_type"] = 1
    elif gd["db_partner"] is not None:
        trainer_dict["battle_type"] = 2
    else:
        breakpoint()
        raise Exception(
            f"[get_or_insert_trainer] Logically impossible battle type; {trainer_name}")

    # TODO:  If Gauntlet, get Gauntlet ID
    # If B2B, do not increment. Will not be always difference of 1, but all B2B should have same ID.
    if gd["b2b"] is not None:
        # b2b part of same gauntlet
        trainer_dict["b2b_id"] = b2b_id
        trainer_dict["gauntlet_id"] = gauntlet_id
    elif gd["gauntlet"] is not None:
        # but not all gauntlet part of same b2b
        trainer_dict["gauntlet_id"] = gauntlet_id
        trainer_dict["b2b_id"] = b2b_id + 1
        b2b_id += 2
    else:
        trainer_dict["b2b_id"] = b2b_id + 1
        b2b_id += 2
        trainer_dict["gauntlet_id"] = gauntlet_id + 1
        gauntlet_id += 2

    # Insert information into DB
    with open("db/sqls/insert_trainer.sql", mode="r") as f:
        query: str = f.read()

    cursor.execute(query, trainer_dict)

    assert cursor.lastrowid is not None
    return cursor.lastrowid, gauntlet_id, b2b_id


def get_or_insert_held_item_db(held_item: str, cursor: sqlite3.Cursor) -> int:
    with open("db/sqls/find_item.sql", "r") as f:
        query = f.read()

    result = cursor.execute(query, (held_item,)).fetchall()

    if len(result) == 1:
        return result[0][0]
    elif len(result) > 1:
        breakpoint()

    with open("db/sqls/insert_item.sql", "r") as f:
        query = f.read()

    cursor.execute(query, (held_item,))

    assert cursor.lastrowid is not None
    return cursor.lastrowid


def get_or_insert_ability_db(ability: str, cursor: sqlite3.Cursor) -> int:
    with open("db/sqls/find_ability.sql", mode="r") as f:
        query = f.read()

    result = cursor.execute(query, (ability,)).fetchall()

    if len(result) == 1:
        return result[0][0]
    elif len(result) > 1:
        breakpoint()

    with open("db/sqls/insert_ability.sql", mode="r") as f:
        query = f.read()

    cursor.execute(query, (ability,))

    assert cursor.lastrowid is not None
    return cursor.lastrowid


def get_last_4_moves(id: int, level: int, cursor: sqlite3.Cursor) -> Dict[str, int | None]:
    with open("db/sqls/get_last_4_moves.sql", "r") as f:
        sql_text = f.read()

    moves = cursor.execute(sql_text, (id, level)).fetchall()

    move_dict = {
        f"move{i+1}": m for i, (m, ) in enumerate(iterable=moves)
    }

    for j in range(len(move_dict) + 1, 4 + 1):  # type: ignore
        move_dict[f"move{j}"] = None

    return move_dict


def read_trainer_battles(trainer_battle_file: str, db_cursor: sqlite3.Cursor):
    if not os.path.exists(trainer_battle_file):
        raise Exception(f"[trainer_battles_to_db] Could not find file {
                        trainer_battle_file}")

    with open(trainer_battle_file, "r") as f:
        battles = f.read()

    # Step 1: Split the file into route sections
    # Match routes delimited by '------'
    route_split_pattern = r"------\n(.*?)\n------"
    route_sections = re.split(
        route_split_pattern, battles, flags=re.MULTILINE | re.DOTALL)

    # Iterate through route sections
    gauntlet_id = 0
    b2b_id = 0

    for i in range(1, len(route_sections), 2):
        route_name = route_sections[i].strip()
        print(f"[trainer_battles] ---- {route_name} ----")
        trainers_data = route_sections[i + 1].strip()

        # Step 2: Split trainers within each route section
        trainer_paragraphs = trainers_data.split("\n\n")

        for t in trainer_paragraphs:
            titer = iter(t.splitlines())
            trainer_name = next(titer)

            trainer_id, gauntlet_id, b2b_id = get_or_insert_trainer(
                route_id=route_name,
                trainer_name=trainer_name,
                gauntlet_id=gauntlet_id,
                b2b_id=b2b_id,
                cursor=db_cursor)

            for i, mons in enumerate(titer):

                get_or_insert_pokemon(first_pokemon=(
                    i == 0), trainer_id=trainer_id, pokemon_line=mons, db_cursor=db_cursor)


def get_or_insert_pokemon(first_pokemon: bool, trainer_id: int, pokemon_line: str, db_cursor: sqlite3.Cursor) -> None:
    pokemon_regex = r"^(?P<species>[\w ]+) Lv.(?P<level>\d{1,3}) (@(?P<item>.+):)?(?P<moves>.*)\[(?P<nature>.+)\|(?P<ability>.+)\]$"

    possible_match = re.search(
        pattern=pokemon_regex, string=pokemon_line, flags=re.MULTILINE)

    if possible_match is None:
        if pokemon_line == "~":
            return
        breakpoint()
        raise Exception(
            f"[get_or_insert_pokemon] Unable to match input string {pokemon_line}")

    gd = possible_match.groupdict()

    # Species
    if "species" not in gd:
        raise Exception(
            f"[get_or_insert_pokemon] Unable to find species from Regex ({pokemon_line})")

    species_name = adjust_pokemon_name(gd["species"])
    species_id = insert_or_retrieve_pokemon_db(
        pokemon_name=species_name, db_cursor=db_cursor)

    if isinstance(species_id, tuple):
        species_id, = species_id

    # Level
    if "level" not in gd:
        raise Exception(
            f"[get_or_insert_pokemon] Unable to find level from Regex ({pokemon_line})")

    level = int(gd["level"])

    # Item
    if "item" in gd:
        held_item: int | None = get_or_insert_held_item_db(
            held_item=gd["item"], cursor=db_cursor)
    else:
        held_item = None

    # Nature
    if "nature" not in gd:
        raise Exception(
            f"[get_or_insert_pokemon] Unable to find nature from Regex ({pokemon_line})")

    nature, = db_cursor.execute("SELECT id FROM pokenature WHERE name = (?)", [
                                gd["nature"]]).fetchone()

    # Ability
    if "ability" not in gd:
        raise Exception(
            f"[get_or_insert_pokemon] Unable to find ability from Regex ({pokemon_line})")

    ability = get_or_insert_ability_db(
        ability=gd["ability"], cursor=db_cursor)

    # Movelist
    if "moves" not in gd or gd["moves"] == "":
        # Handle Default Moveset
        move_id_dict = get_last_4_moves(
            id=species_id, level=level, cursor=db_cursor)

    else:
        move_list = gd["moves"].split(",")
        move_id_dict = {}
        for i, m in enumerate(move_list, start=1):
            adjusted_move_name = adjust_move_name(name=m)

            move_id: int = get_or_insert_move(
                move=adjusted_move_name, cursor=db_cursor)

            move_id_dict[f"move{i}"] = move_id

        for j in range(len(move_id_dict) + 1, 4 + 1):  # type: ignore
            move_id_dict[f"move{j}"] = None

    if len(move_id_dict) != 4:
        breakpoint()

    pokedict = {
        "trainer_id": trainer_id,
        "lead_pokemon": first_pokemon,
        "species": species_id,
        "nature": nature,
        "ability": ability,
        "pokelevel": level,
        "held_item": held_item,
        **move_id_dict
    }

    # First, see if already in DB
    with open("db/sqls/check_pokemon_in_db.sql", "r") as f:
        query = f.read()
        result = db_cursor.execute(
            query, (trainer_id, species_id, nature, ability, level)).fetchone()

    if result is not None:
        return

    # Next, insert into DB

    for k, v in pokedict.items():
        if isinstance(v, tuple):
            print(f"[tuple issue]: {k} -> {v}")
            breakpoint()

    with open("db/sqls/insert_pokemon_in_db.sql", mode="r") as f:
        query = f.read()
        result = db_cursor.execute(query, pokedict)

    print(f"[get_or_insert_pokemon]: inserted {pokemon_line}")


def insert_battles_to_db():
    db = sqlite3.connect("db/rnb.db")
    cursor = db.cursor()

    read_trainer_battles("db/trainer_battles.txt", cursor)
    db.commit()
    # For now, just print out trainers

    # Assume tables already created

    # Save or print results
    split_results = cursor.execute(
        "SELECT route, name, gauntlet_id FROM trainers ORDER BY id;").fetchall()
    for row in split_results:
        print(row)
