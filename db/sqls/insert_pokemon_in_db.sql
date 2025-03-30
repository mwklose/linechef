INSERT INTO pokemon (
    trainer_id, 
    lead_pokemon, 
    species, 
    nature, 
    ability, 
    pokelevel, 
    held_item, 
    move1, 
    move2, 
    move3, 
    move4
) 
    VALUES (
        :trainer_id, 
        :lead_pokemon,
        :species, 
        :nature, 
        :ability, 
        :pokelevel,
        :held_item, 
        :move1, 
        :move2, 
        :move3, 
        :move4
    );