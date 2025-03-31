SELECT ss.*, hi.name as held_item, pa.name as ability, p.nature, p.pokelevel AS pokelevel, p.move1, p.move2, p.move3, p.move4
    FROM pokemon as p
    LEFT JOIN species_stat as ss ON ss.id = p.species
    LEFT JOIN pokeability as pa ON pa.id = p.ability
    LEFT JOIN held_item as hi ON hi.id = p.held_item
    WHERE p.trainer_id = (?)
        AND p.lead_pokemon = (?)
    ORDER BY p.poke_id
    ;

