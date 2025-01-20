import os
import re
import sqlite3
from typing import Any, Dict, List, Tuple

from linechef.battle_type import BattleType

def read_trainer_battles(trainer_battle_file: str) -> Dict[str, List[str]]: 
    if not os.path.exists(trainer_battle_file): 
        raise Exception(f"[trainer_battles_to_db] Could not find file {trainer_battle_file}")

    with open(trainer_battle_file, "r") as f: 
        battles = f.read()


    # Step 1: Split the file into route sections
    route_split_pattern = r"------\n(.*?)\n------"  # Match routes delimited by '------'
    route_sections = re.split(route_split_pattern, battles, flags=re.MULTILINE | re.DOTALL)

    # Initialize result dictionary
    split_data = {}

    # Iterate through route sections
    for i in range(1, len(route_sections), 2):
        route_name = route_sections[i].strip()
        trainers_data = route_sections[i + 1].strip()

        # Step 2: Split trainers within each route section
        trainer_split_pattern = r"^(.*?)\n([^-]*?)(?=\n(?:[A-Z][a-z]+ [A-Z][a-z]+|$))\n\n"  # Match trainers
        trainers = trainers_data
        trainers = re.findall(trainer_split_pattern, trainers_data, flags=re.MULTILINE | re.DOTALL)

        
        # Process trainers and notes
        trainer_list = []
        for trainer_name, trainer_details in trainers:
            trainer_name = trainer_name.strip()
            trainer_details = trainer_details.strip()
            if trainer_details:

                detail_dict, battle_type = parse_trainer_details(trainer_name=trainer_name, details=trainer_details)
                trainer_list.append({"trainer": trainer_name, "details": detail_dict, "battle_type": battle_type})

        split_data[route_name] = trainer_list

    return split_data

def parse_trainer_details(trainer_name: str, details: str) -> Tuple[List[Dict[str, str | Any]], BattleType]: 
    poke_list = []
    pokemon_regex = r"(?P<species>[A-Za-z_0-9]+) Lv.(?P<level>\d{1,3}) (@(?P<item>.*): )?(?P<moves>.*)\[(?P<nature>.*)\|(?P<ability>.*)\]"

    # TODO: check trainer name for Doubles/other effects
    bt = BattleType.SINGLE
    if "Double Battle With" in trainer_name: 
        bt = BattleType.DOUBLE_FRIEND
    elif "Double" in trainer_name: 
        bt = BattleType.DOUBLE_COMBINE

    for line in details.splitlines(): 
        possible_match = re.match(pokemon_regex, line)
        if not possible_match: 
            if "~" in line: 
                
                continue
            else: 
                # TODO: check if doubles here?
                raise Exception(f"[parse_trainer_details] unable to match {line}")

        gd = possible_match.groupdict()
        poke_list.append(gd)

    return poke_list, bt



def insert_battles_to_db():
    split_results = read_trainer_battles("db/trainer_battles.txt") 
    # For now, just print out trainers

    db = sqlite3.connect("db/rnb.db") 
    cursor = db.cursor()

    # Establish tables if they do not exist
    
    # Save or print results
    for route, trainers in split_results.items():
        print(f"Route: {route}")

        # For trainer db, insert name, route, ID, special?
        
        # for trainer in trainers:
        #     print(f"\tTrainer: {trainer['trainer']}")
        #     print(f"\t\tDetails: {trainer['details']}\n")

