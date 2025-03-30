SELECT * 
    FROM pokemon 
    WHERE trainer_id = (?) 
        AND species = (?)
        AND nature = (?)
        AND ability = (?)
        AND pokelevel = (?);