from linechef.pokemon import Pokemon


def test_get_ruin_maniac_georgie(): 
    
    georgie = Pokemon.get_pokemon_by_trainer_id(13)

    georgie_expected = [
        {"hp": 40, "attack": 27, "defense": 31, "spattack": 16, "spdefense": 18, "speed": 23}, 
        {"hp": 43, "attack": 26, "defense": 27, "spattack": 28, "spdefense": 21, "speed": 13},
        {"hp": 40, "attack": 34, "defense": 31, "spattack": 20, "spdefense": 23, "speed": 22}, 
        {"hp": 62, "attack": 31, "defense": 19, "spattack": 17, "spdefense": 31, "speed": 11}
    ]

    for i, mon in enumerate(georgie_expected): 
        for stat, value in mon.items(): 
            assert hasattr(georgie[i], stat)
            assert getattr(georgie[i], stat) == value
