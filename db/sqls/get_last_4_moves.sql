SELECT DISTINCT pokemove_id 
    FROM learnset
    WHERE poke_id = (?) 
    AND pokelevel <= (?)
    ORDER BY pokelevel DESC
    LIMIT 4;