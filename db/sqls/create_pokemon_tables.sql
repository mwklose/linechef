CREATE TABLE IF NOT EXISTS trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    route TEXT,
    battle_type INTEGER,
    gauntlet_id INTEGER,
    b2b_id INTEGER
);

CREATE TABLE IF NOT EXISTS held_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT
);

-- types
CREATE TABLE IF NOT EXISTS poketype (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO poketype (name) SELECT ("Normal") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Normal");
INSERT INTO poketype (name) SELECT ("Fighting") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Fighting");
INSERT INTO poketype (name) SELECT ("Flying") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Flying");
INSERT INTO poketype (name) SELECT ("Poison") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Poison");
INSERT INTO poketype (name) SELECT ("Ground") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Ground");
INSERT INTO poketype (name) SELECT ("Rock") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Rock");
INSERT INTO poketype (name) SELECT ("Bug") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Bug");
INSERT INTO poketype (name) SELECT ("Ghost") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Ghost");
INSERT INTO poketype (name) SELECT ("Steel") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Steel");
INSERT INTO poketype (name) SELECT ("Fire") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Fire");
INSERT INTO poketype (name) SELECT ("Water") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Water");
INSERT INTO poketype (name) SELECT ("Grass") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Grass");
INSERT INTO poketype (name) SELECT ("Electric") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Electric");
INSERT INTO poketype (name) SELECT ("Psychic") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Psychic");
INSERT INTO poketype (name) SELECT ("Ice") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Ice");
INSERT INTO poketype (name) SELECT ("Dragon") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Dragon");
INSERT INTO poketype (name) SELECT ("Dark") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Dark");
INSERT INTO poketype (name) SELECT ("Fairy") WHERE NOT EXISTS(SELECT 1 FROM poketype WHERE name = "Fairy");


-- natures
CREATE TABLE IF NOT EXISTS pokenature (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL
);

INSERT INTO pokenature (name) SELECT ("Hardy") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Hardy");
INSERT INTO pokenature (name) SELECT ("Lonely") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Lonely");
INSERT INTO pokenature (name) SELECT ("Adamant") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Adamant");
INSERT INTO pokenature (name) SELECT ("Naughty") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Naughty");
INSERT INTO pokenature (name) SELECT ("Brave") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Brave");
INSERT INTO pokenature (name) SELECT ("Bold") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Bold");
INSERT INTO pokenature (name) SELECT ("Docile") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Docile");
INSERT INTO pokenature (name) SELECT ("Impish") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Impish");
INSERT INTO pokenature (name) SELECT ("Lax") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Lax");
INSERT INTO pokenature (name) SELECT ("Relaxed") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Relaxed");
INSERT INTO pokenature (name) SELECT ("Modest") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Modest");
INSERT INTO pokenature (name) SELECT ("Mild") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Mild");
INSERT INTO pokenature (name) SELECT ("Bashful") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Bashful");
INSERT INTO pokenature (name) SELECT ("Rash") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Rash");
INSERT INTO pokenature (name) SELECT ("Quiet") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Quiet");
INSERT INTO pokenature (name) SELECT ("Calm") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Calm");
INSERT INTO pokenature (name) SELECT ("Gentle") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Gentle");
INSERT INTO pokenature (name) SELECT ("Careful") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Careful");
INSERT INTO pokenature (name) SELECT ("Quirky") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Quirky");
INSERT INTO pokenature (name) SELECT ("Sassy") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Sassy");
INSERT INTO pokenature (name) SELECT ("Timid") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Timid");
INSERT INTO pokenature (name) SELECT ("Hasty") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Hasty");
INSERT INTO pokenature (name) SELECT ("Jolly") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Jolly");
INSERT INTO pokenature (name) SELECT ("Naive") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Naive");
INSERT INTO pokenature (name) SELECT ("Serious") WHERE NOT EXISTS(SELECT 1 FROM pokenature WHERE name="Serious");

-- Abilities Table
CREATE TABLE IF NOT EXISTS pokeability (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL
);

-- Species base stats
CREATE TABLE IF NOT EXISTS species_stat (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    type1 INTEGER REFERENCES poketype(id),
    type2 INTEGER REFERENCES poketype(id),
    base_hp INTEGER NOT NULL, 
    base_attack INTEGER NOT NULL,  
    base_defense INTEGER NOT NULL, 
    base_spattack INTEGER NOT NULL, 
    base_spdefense INTEGER NOT NULL, 
    base_speed INTEGER NOT NULL
);


-- Moves for Pokemon
CREATE TABLE IF NOT EXISTS pokemove (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    movename TEXT NOT NULL, 
    damage_class TEXT NOT NULL, 
    target TEXT,
    power INTEGER,
    accuracy INTEGER,
    priority INTEGER, 
    poketype INTEGER REFERENCES poketype(id), 
    flinch_chance INTEGER, 
    ailment TEXT,
    ailment_chance INTEGER, 
    crit_rate INTEGER, 
    stat TEXT, 
    stat_chance INTEGER, 
    drain INTEGER, 
    healing INTEGER,
    min_hits INTEGER, 
    max_hits INTEGER
);


CREATE TABLE IF NOT EXISTS pokemon (
    poke_id INTEGER PRIMARY KEY AUTOINCREMENT,
    trainer_id INTEGER NOT NULL REFERENCES trainers(id),
    
    lead_pokemon BOOLEAN, 
    species INTEGER NOT NULL REFERENCES species_stats(id), 
    nature INTEGER NOT NULL REFERENCES pokenature(id),
    ability INTEGER NOT NULL REFERENCES pokeability(id),
    pokelevel INTEGER, 
    held_item INTEGER REFERENCES held_item(id),
    move1 INTEGER NOT NULL REFERENCES pokemove(id),
    move2 INTEGER REFERENCES pokemove(id),
    move3 INTEGER REFERENCES pokemove(id),
    move4 INTEGER REFERENCES pokemove(id)
);