SELECT id
    FROM trainers
    WHERE name LIKE (?) 
    AND route LIKE (?);
    -- WHERE name LIKE (?)
    -- AND route LIKE (?);