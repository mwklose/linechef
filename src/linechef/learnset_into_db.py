import json
import re
import sqlite3
import requests

LEARNSET_FILE: str = "db/learnsets.txt"


def adjust_move_name(name: str | None) -> str:
    if name is None:
        raise Exception("Could not adjust None name.")

    return name.strip().lower().replace(" ", "-")


def adjust_pokemon_name(name: str | None) -> str:
    if name is None:
        raise Exception("Could not adjust None name.")

    return (str(name)
            .lower()
            .replace(" ", "-")
            .replace("oricorio_", "oricorio-")
            .replace("pom_pom", "pom-pom")
            .replace("rotom_", "rotom-")
            .replace("_", "")
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
            .replace("zygarde10", "zygarde-10")
            .replace("furfrouhearttrim", "furfrou")
            .replace("meowsticf", "meowstic-f")
            .replace("gourgeists", "gourgeist-s")
            .replace("orangeflower", "")
            .replace("eternalflower", "-eternal")
            .replace("caramelswirl", "")
            .replace("mrmime", "mr-mime")
            .replace("mrrime", "mr-rime")
            .replace("indeedeef", "indeedee-f")
            .replace("trashcloak", "-trash")
            .replace("sandycloak", "-sandy")
            .replace("battlebond", "-battle-bond")
            .replace("shaymins", "shaymin-s")
            .replace("vivillonelegant", "vivillon")
            .replace("vivillonmodern", "vivillon")
            .replace("vivillonsun", "vivillon")
            .replace("vivillongarden", "vivillon")
            .replace("tapu", "tapu-")
            .replace("unbound", "-unbound")
            .replace("darmanitan-galar", "darmanitan-galar-standard")
            .replace("worldcap", "-world-cap")
            .replace("tinaorigin", "tina-origin")
            .replace("therian", "-therian")
            .replace("kyuremw", "kyurem-w")
            .replace("kyuremb", "kyurem-b")
            .replace("icerider", "-ice")
            .replace("50powerconstruct", "-50-power-construct")
            )


def insert_or_retrieve_pokemon_db(pokemon_name: str, db_cursor: sqlite3.Cursor) -> int:
    is_silvally = False
    if "silvally" in pokemon_name:
        silvally_type = pokemon_name[len("silvally"):]
        pokemon_name = "silvally"
        is_silvally = True

    poke_api_query = "https://pokeapi.co/api/v2/pokemon/{poke}"
    headers = {"Content-Type": "application/json"}

    found_in_db = db_cursor.execute("SELECT id FROM species_stat WHERE name = (?)", [
        pokemon_name]).fetchall()

    if len(found_in_db) == 1:
        return found_in_db[0]

    elif len(found_in_db) > 1:
        breakpoint()

    # Fetch pokemon from PokeAPI into DB
    response = requests.get(url=poke_api_query.format(
        poke=pokemon_name), headers=headers)

    if response.status_code != 200:
        # Alternate way: look up through pokemon-species pathway
        pokeurl = f"https://pokeapi.co/api/v2/pokemon-species/{
            pokemon_name}"
        backup_response = requests.get(url=pokeurl, headers=headers)

        if backup_response.status_code != 200:
            raise Exception(f"[insert_learnsets] Unable to find {pokemon_name} ({
                            poke_api_query.format(poke=pokemon_name)})")

        poke_id = backup_response.json()["id"]
        response = requests.get(url=poke_api_query.format(
            poke=poke_id), headers=headers)

    response_dict = {}

    response_dict["name"] = pokemon_name
    js = response.json()

    # Extract base stats and type
    # Set second type by default
    response_dict["type2"] = None

    for i, t in enumerate(js["types"], start=1):
        if is_silvally:
            poketype = silvally_type.capitalize()
        else:
            poketype = str(t["type"]["name"]).capitalize()
        ptype, = db_cursor.execute("SELECT id FROM poketype WHERE name = (?);", [
            poketype]).fetchone()
        response_dict[f"type{i}"] = ptype

    for s in js["stats"]:
        stat_value = s["base_stat"]
        stat_type = str(s["stat"]["name"]).replace("special-", "sp")
        response_dict[f"base_{stat_type}"] = stat_value

    if is_silvally:
        response_dict["name"] = f"silvally-{silvally_type}"

    # Insert base stat into DB if not exists?
    # Update instead?
    db_cursor.execute("INSERT INTO species_stat ({cols}) VALUES({vals})".format(
        cols=", ".join(response_dict.keys()),
        vals=":" + ", :".join(response_dict.keys())
    ), response_dict)

    assert db_cursor.lastrowid is not None

    return db_cursor.lastrowid


def get_or_insert_move(move: str, cursor: sqlite3.Cursor) -> int:
    move_ids = cursor.execute(
        "SELECT id FROM pokemove WHERE movename = (?)", [move]).fetchall()

    if len(move_ids) == 1:
        return move_ids[0][0]

    if len(move_ids) == 0:
        print(f"\tInserting move: {move}")
        move_dict = get_move_dict(
            cursor=cursor, movename=move)

        with open("db/sqls/insert_move.sql", "r") as f:
            query = f.read()
        cursor.execute(query, move_dict)

        assert cursor.lastrowid is not None

        return cursor.lastrowid

    elif len(move_ids) > 1:
        breakpoint()

    # Exactly 1 move guaranteed
    return move_ids[0][0]


def insert_learnsets_and_base_stats():
    pokemon_regex: str = r"^(?P<species>[A-Z]\w+)\n"
    move_regex: str = r"^Lv.\W{1,3}(?P<level>\d{1,3})\W+(?P<movename>.*)\n"

    with open(LEARNSET_FILE, "r") as lsf:
        lsf_text = lsf.readlines()

    pokemon: str | None = None
    adjusted_pokemon_name: str | None = None
    db = sqlite3.connect("db/rnb.db")
    cursor = db.cursor()

    for line in lsf_text:
        if pokemon is None:
            possible_match = re.search(pattern=pokemon_regex, string=line)
            if possible_match is None:
                continue
            pokemon = possible_match["species"]

            adjusted_pokemon_name = adjust_pokemon_name(name=pokemon)
            insert_or_retrieve_pokemon_db(
                pokemon_name=adjusted_pokemon_name, db_cursor=cursor)
            db.commit()
            continue

        possible_match = re.search(pattern=move_regex, string=line)
        if possible_match is None:
            pokemon = None
            adjusted_pokemon_name = None
            continue

        level = possible_match["level"]
        move = possible_match["movename"]

        adjusted_move_name: str = adjust_move_name(name=move)

        move_id = get_or_insert_move(move=adjusted_move_name, cursor=cursor)

        # Get PokeID
        poke_id, = cursor.execute("SELECT id FROM species_stat WHERE name = (?)", [
            adjusted_pokemon_name]).fetchone()

        # Insert into DB
        cursor.execute("INSERT INTO learnset (poke_id, pokelevel, pokemove_id) VALUES (?, ?, ?)", [
            poke_id, level, move_id])
        db.commit()


def get_move_dict(cursor: sqlite3.Cursor, movename: str):
    move_api_query = "https://pokeapi.co/api/v2/move/{movename}"
    headers = {"Content-Type": "application/json"}

    hidden_power = False
    if "hidden-power" in movename:
        hidden_power = True
        movename, hidden_power_type = movename.rsplit("-", maxsplit=1)

    move_response = requests.get(url=move_api_query.format(
        movename=movename), headers=headers)
    if move_response.status_code != 200:
        raise Exception(f"[insert_learnsets] Could not find move {
                        movename} in API")

    move_dict = {}
    js = move_response.json()

    # ID
    if "id" not in js:
        breakpoint()
    move_dict["id"] = js["id"]

    # name
    if hidden_power:
        move_dict["movename"] = f"{movename}-{hidden_power_type}"
    else:
        move_dict["movename"] = js["name"]

    # damage-class
    move_dict["damage_class"] = js["damage_class"]["name"]

    # target
    move_dict["target"] = js["target"]["name"]

    # power
    move_dict["power"] = js["power"]

    # accuracy
    move_dict["accuracy"] = js["accuracy"]

    # priority
    move_dict["priority"] = js["priority"]

    # poketype
    if hidden_power:
        move_type = hidden_power_type.capitalize()
    else:
        move_type = str(js["type"]["name"]).capitalize()

    typeid, = cursor.execute("SELECT id FROM poketype WHERE name = (?)", [
        move_type]).fetchone()

    # Special handling for hidden power to not create conflicting ids
    if hidden_power:
        move_dict["id"] = f"{js['id']}00{typeid}"
    move_dict["poketype"] = typeid

    # flinch_chance
    move_dict["flinch_chance"] = js["meta"]["flinch_chance"]

    # ailment
    move_dict["ailment"] = js["meta"]["ailment"]["name"]

    # ailment_chance
    move_dict["ailment_chance"] = js["meta"]["ailment_chance"]

    # crit_rate
    move_dict["crit_rate"] = js["meta"]["crit_rate"]

    # stat - serialize as JSON is StackOverflow suggestion
    move_dict["stat"] = json.dumps(js["stat_changes"])

    # stat_chance
    move_dict["stat_chance"] = js["meta"]["stat_chance"]

    # drain
    move_dict["drain"] = js["meta"]["drain"]

    # healing
    move_dict["healing"] = js["meta"]["healing"]

    # Min/Max Hits
    move_dict["min_hits"] = js["meta"]["min_hits"]
    move_dict["max_hits"] = js["meta"]["max_hits"]

    return move_dict
