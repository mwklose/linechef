import re
import sqlite3
import requests

LEARNSET_FILE: str = "db/learnsets.txt"

def insert_learnsets_and_base_stats(): 
    pokemon_regex: str = r"^(?P<species>[A-Z]\w+)\n"
    move_regex: str = r"^Lv.\W{1,3}(?P<level>\d{1,3})\W+(?P<movename>.*)\n"

    with open(LEARNSET_FILE, "r") as lsf: 
        lsf_text = lsf.readlines()

    pokemon: str | None = None
    db = sqlite3.connect("db/rnb.db")
    cursor = db.cursor()

    poke_api_query = "https://pokeapi.co/api/v2/pokemon/{poke}"
    headers = {"Content-Type": "application/json"}
    
    for line in lsf_text:
        if pokemon is None: 
            possible_match = re.search(pattern=pokemon_regex, string=line)
            if possible_match is None: 
                continue
            pokemon = possible_match["species"]

            adjusted_pokemon_name = (
                pokemon
                .lower()
                .replace(" ", "-")
                .replace("hisuian", "-hisui")
                .replace("alolan", "-alola")
                .replace("galarian", "-galar")
                .replace("nidoranf", "nidoran-f")
                .replace("nidoranm", "nidoran-m")
                .replace("porygonz", "porygon-z")
                .replace("midnight", "-midnight")
                .replace("rocdusk", "roc-dusk")
                .replace("jangmoo", "jangmo-o")
                .replace("hakamoo", "hakamo-o")
                .replace("kommoo", "kommo-o")
                .replace("lowkey", "-low-key")
                .replace("cityamped", "city-amped")
                .replace("rapidstrikestyle", "-rapid-strike")
                .replace("singlestrikestyle", "-single-strike")
                )

            found_in_db = cursor.execute("SELECT 1 FROM species_stat WHERE name = (?)", [adjusted_pokemon_name]).fetchall()

            if len(found_in_db) == 1: 
                print(f"found {adjusted_pokemon_name} already")
                continue
            elif len(found_in_db) > 1:
                breakpoint()
            

            
            # Fetch pokemon from PokeAPI into DB
            response = requests.get(url=poke_api_query.format(poke=adjusted_pokemon_name), headers=headers)

            if response.status_code != 200: 
                # Alternate way: look up through pokemon-species pathway
                pokeurl = f"https://pokeapi.co/api/v2/pokemon-species/{adjusted_pokemon_name}"
                backup_response = requests.get(url=pokeurl, headers=headers) 

                if backup_response.status_code != 200: 
                    raise Exception(f"[insert_learnsets] Unable to find {pokemon} ({poke_api_query.format(poke=adjusted_pokemon_name)})")

                poke_id = backup_response.json()["id"]
                response = requests.get(url=poke_api_query.format(poke=poke_id), headers=headers)
                

            
           
            response_dict = {}

            response_dict["name"] = adjusted_pokemon_name
            js = response.json()

            # Extract base stats and type
            # Set second type by default
            response_dict["type2"] = None
            
            for i, t in enumerate(js["types"], start=1): 
                poketype = str(t["type"]["name"]).capitalize()
                ptype, = cursor.execute(f"SELECT id FROM poketype WHERE name = (?);", [poketype]).fetchone()
                response_dict[f"type{i}"] = ptype

            for s in js["stats"]: 
                stat_value = s["base_stat"]
                stat_type = str(s["stat"]["name"]).replace("special-", "sp")
                response_dict[f"base_{stat_type}"] = stat_value


            # Insert base stat into DB if not exists? 
            # Update instead?
            cursor.execute("INSERT INTO species_stat ({cols}) VALUES({vals})".format(
                cols=", ".join(response_dict.keys()),
                vals=":" + ", :".join(response_dict.keys())
                ), response_dict)

            db.commit()
            
            
        else: 
            possible_match = re.search(pattern=move_regex, string=line)
            if possible_match is None: 
                pokemon = None
                continue

            level = possible_match["level"]
            move = possible_match["movename"]


            

            

            
            
    return 42 