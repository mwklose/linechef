import csv
import sqlite3
from typing import Dict
from linechef.learnset_into_db import adjust_move_name

def update_moves(move_csv_path: str) -> None: 

    with open(move_csv_path, "r") as f: 
        for line in csv.DictReader(f):
            update_move_by_dict(line)
            

def update_move_by_dict(move_update: Dict[str, str]):
    for col in ["Move", "BP", "PP", "Accuracy", "Effect Chance", "Type"]:
        if col not in move_update: 
            breakpoint()
            raise Exception(f"[update_move_by_dict] Unable to find column {col}")
    
    move_name: str = move_update["Move"]
    lookup_move_name: str = adjust_move_name(move_name)

    db = sqlite3.connect("db/rnb.db")
    cursor = db.cursor()

    # 1. BP
    if move_update["BP"] != "None": 
        cursor.execute(
            "UPDATE pokemove SET power = (?) WHERE movename = (?)", (move_update["BP"], lookup_move_name)
        )
    # 2. PP
    if move_update["PP"] != "None": 
        ...
    # 3. Accuracy
    if move_update["Accuracy"] != "None": 
        cursor.execute(
            "UPDATE pokemove SET accuracy = (?) WHERE movename = (?)", (move_update["Accuracy"], lookup_move_name)
        )
    # 4. Effect Chance
    if move_update["Effect Chance"] != "None": 
        cursor.execute(
            "UPDATE pokemove SET ailment_chance = (?) WHERE movename = (?)", (move_update["Effect Chance"], lookup_move_name)
        )
    # 5. Type
    if move_update["Type"] != "None": 
        newtype = cursor.execute("SELECT id FROM poketype WHERE name = (?)", (move_update["Type"], )).fetchone()
        cursor.execute(
            "UPDATE pokemove SET poketype = (?) WHERE movename = (?)", (newtype[0], lookup_move_name)
        )
     
    cursor.close()
    db.commit()
    db.close()
    print(f"[update_move_by_dict] Updated {lookup_move_name}")


if __name__ == "__main__":
    update_moves("db/move_changes.csv")