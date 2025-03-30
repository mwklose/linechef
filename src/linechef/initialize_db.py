import sqlite3
from linechef.learnset_into_db import insert_learnsets_and_base_stats
from linechef.trainer_battles_to_db import insert_battles_to_db

if __name__ == "__main__":

    db = sqlite3.connect("db/rnb.db")
    cursor = db.cursor()

    with open("db/sqls/create_pokemon_tables.sql") as f:
        query = f.read()
        cursor.executescript(query)

    with open("db/sqls/create_learnset_tables.sql") as f:
        query = f.read()
        cursor.executescript(query)

    # 1. Populate all different pokemon species, types, base stats
    # 2. Import Learnsets (populates pokemove table partially)
    print("[initialize_db] Starting to insert learnset and base stats")
    insert_learnsets_and_base_stats()

    # 3. Import Battles (completes pokemove table for all necessary; trainer table)
    # 4. Import Move Category, Type, Power, Accuracy, whether secondary effects
    print("[initialize_db] Starting to insert trainer battles")
    insert_battles_to_db()
