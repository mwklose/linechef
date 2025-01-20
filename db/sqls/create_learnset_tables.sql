CREATE TABLE IF NOT EXISTS learnset (
    poke_id INTEGER NOT NULL REFERENCES species_stat(id),
    pokelevel INTEGER NOT NULL, 
    pokemove_id INTEGER NOT NULL REFERENCES pokemove(id)
)