import copy
import pytest
import sqlite3

from linechef.pokemon import PokeStat, Pokemon
from linechef.pokemove import Pokemove
from linechef.pokenature import Pokenature
from linechef.poketype import Poketype

FAKE_OUT = 252
HEADBUTT = 29
EARTHQUAKE = 89
VENOSHOCK = 474
SURF = 57


@pytest.fixture
def spinda():
    db = sqlite3.connect("db/rnb.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    spinda_stats = cursor.execute(
        "SELECT * FROM species_stat WHERE name='spinda';"
    ).fetchone()

    spinda_stats_dict = dict(spinda_stats)

    spinda_movelist: list[Pokemove] = [Pokemove.get_pokemove_by_id(
        # type: ignore
        id) for id in [FAKE_OUT, HEADBUTT] if Pokemove.get_pokemove_by_id(id) is not None]

    for spinda_move in spinda_movelist:
        assert spinda_move is not None

    spinda = Pokemon(
        name=spinda_stats_dict["name"],
        type1=Poketype(spinda_stats_dict["type1"]),
        type2=None,
        level=50,
        ability="Own Tempo",
        nature=Pokenature.SERIOUS,
        held_item="None",
        hp=Pokemon.calculate_hp(
            base_hp=spinda_stats_dict["base_hp"], iv=31, level=50),
        attack=Pokemon.calculate_stat(
            statistic=PokeStat.ATTACK, base_stat=spinda_stats_dict["base_attack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        defense=Pokemon.calculate_stat(
            statistic=PokeStat.DEFENSE, base_stat=spinda_stats_dict["base_defense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spattack=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_ATTACK, base_stat=spinda_stats_dict["base_spattack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spdefense=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_DEFENSE, base_stat=spinda_stats_dict["base_spdefense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        speed=Pokemon.calculate_stat(
            statistic=PokeStat.SPEED, base_stat=spinda_stats_dict["base_speed"], iv=31, level=50, nature=Pokenature.SERIOUS),
        move_list=spinda_movelist
    )
    spinda.status = "Badly Poisoned"
    yield spinda


@pytest.fixture
def torterra():
    db = sqlite3.connect("db/rnb.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    torterra_stats = cursor.execute(
        "SELECT * FROM species_stat WHERE name='torterra';"
    ).fetchone()

    torterra_stats_dict = dict(torterra_stats)

    torterra_movelist: list[Pokemove] = [Pokemove.get_pokemove_by_id(
        # type: ignore
        id) for id in [HEADBUTT, EARTHQUAKE] if Pokemove.get_pokemove_by_id(id) is not None]

    for torterra_move in torterra_movelist:
        assert torterra_move is not None

    torterra = Pokemon(
        name=torterra_stats_dict["name"],
        type1=Poketype(torterra_stats_dict["type1"]),
        type2=Poketype(torterra_stats_dict["type2"]),
        level=50,
        ability="Battle Armor",
        nature=Pokenature.SERIOUS,
        held_item="None",
        hp=Pokemon.calculate_hp(
            base_hp=torterra_stats_dict["base_hp"], iv=31, level=50),
        attack=Pokemon.calculate_stat(
            statistic=PokeStat.ATTACK, base_stat=torterra_stats_dict["base_attack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        defense=Pokemon.calculate_stat(
            statistic=PokeStat.DEFENSE, base_stat=torterra_stats_dict["base_defense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spattack=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_ATTACK, base_stat=torterra_stats_dict["base_spattack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spdefense=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_DEFENSE, base_stat=torterra_stats_dict["base_spdefense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        speed=Pokemon.calculate_stat(
            statistic=PokeStat.SPEED, base_stat=torterra_stats_dict["base_speed"], iv=31, level=50, nature=Pokenature.SERIOUS),
        move_list=torterra_movelist
    )
    torterra.status = "Badly Poisoned"
    yield torterra


@pytest.fixture
def mareanie():
    db = sqlite3.connect("db/rnb.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    mareanie_stats = cursor.execute(
        "SELECT * FROM species_stat WHERE name='mareanie';"
    ).fetchone()

    mareanie_stats_dict = dict(mareanie_stats)

    mareanie_movelist: list[Pokemove] = [Pokemove.get_pokemove_by_id(
        # type: ignore
        id) for id in [SURF, VENOSHOCK] if Pokemove.get_pokemove_by_id(id) is not None]

    for mareanie_move in mareanie_movelist:
        assert mareanie_move is not None

    mareanie = Pokemon(
        name=mareanie_stats_dict["name"],
        type1=Poketype(mareanie_stats_dict["type1"]),
        type2=Poketype(mareanie_stats_dict["type2"]),
        level=50,
        ability="Merciless",
        nature=Pokenature.SERIOUS,
        held_item="None",
        hp=Pokemon.calculate_hp(
            base_hp=mareanie_stats_dict["base_hp"], iv=31, level=50),
        attack=Pokemon.calculate_stat(
            statistic=PokeStat.ATTACK, base_stat=mareanie_stats_dict["base_attack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        defense=Pokemon.calculate_stat(
            statistic=PokeStat.DEFENSE, base_stat=mareanie_stats_dict["base_defense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spattack=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_ATTACK, base_stat=mareanie_stats_dict["base_spattack"], iv=31, level=50, nature=Pokenature.SERIOUS),
        spdefense=Pokemon.calculate_stat(
            statistic=PokeStat.SPECIAL_DEFENSE, base_stat=mareanie_stats_dict["base_spdefense"], iv=31, level=50, nature=Pokenature.SERIOUS),
        speed=Pokemon.calculate_stat(
            statistic=PokeStat.SPEED, base_stat=mareanie_stats_dict["base_speed"], iv=31, level=50, nature=Pokenature.SERIOUS),
        move_list=mareanie_movelist
    )

    yield mareanie


def test_stat_calculation(spinda: Pokemon, torterra: Pokemon, mareanie: Pokemon):
    assert spinda.get_level() == 50
    assert spinda.get_hp() == 135
    assert spinda.attack == 80
    assert spinda.defense == 80
    assert spinda.spattack == 80
    assert spinda.spdefense == 80
    assert spinda.speed == 80
    # Functional speed should account for quick draw/quick claw activations...
    assert spinda.get_functional_speed(True) == 80
    assert spinda.get_functional_speed(False) == 80

    assert spinda.get_current_hp() == 135
    assert spinda.get_type1() == Poketype.NORMAL
    assert spinda.get_type2() is None


    # Check Torterra
    assert torterra.get_level() == 50
    assert torterra.get_hp() == 170
    assert torterra.attack == 129
    assert torterra.defense == 125
    assert torterra.spattack == 95
    assert torterra.spdefense == 105
    assert torterra.speed == 76
    # Functional speed should account for quick draw/quick claw activations...
    assert torterra.get_functional_speed(True) == 76
    assert torterra.get_functional_speed(False) == 76

    assert torterra.get_current_hp() == 170
    assert torterra.get_type1() == Poketype.GRASS
    assert torterra.get_type2() == Poketype.GROUND

    # Check Mareanie
    assert mareanie.get_level() == 50
    assert mareanie.get_hp() == 125
    assert mareanie.attack == 73
    assert mareanie.defense == 82
    assert mareanie.spattack == 63
    assert mareanie.spdefense == 72
    assert mareanie.speed == 65
    # Functional speed should account for quick draw/quick claw activations...
    assert mareanie.get_functional_speed(True) == 65
    assert mareanie.get_functional_speed(False) == 65

    assert mareanie.get_current_hp() == 125
    assert mareanie.get_type1() == Poketype.POISON
    assert mareanie.get_type2() == Poketype.WATER

    


def test_neutral_move(spinda: Pokemon):

    target_pokemon = copy.deepcopy(spinda)

    damage_rolls = spinda.calculate_damage_rolls(target_pokemon=target_pokemon)

    expected_damage_rolls = {
        spinda.move_list[0]: (
            [24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 27, 27, 27, 27, 27, 28],
            [34, 36, 36, 36, 36, 37, 37, 37, 39, 39, 39, 39, 40, 40, 40, 42]
        ),
        spinda.move_list[1]: (
            [40, 40, 40, 42, 42, 42, 43, 43, 43, 45, 45, 45, 46, 46, 46, 48],
            [60, 61, 61, 63, 63, 64, 64, 66, 66, 67, 67, 69, 69, 70, 70, 72]
        )
    }

    for pokemove, dr in damage_rolls.items():
        assert pokemove in expected_damage_rolls

        expected_dr = expected_damage_rolls[pokemove]

        for i in range(2):
            for j, (damage_roll, expected_damage_roll) in enumerate(zip(dr[i], expected_dr[i])):
                assert damage_roll == expected_damage_roll, f"Pokemove {pokemove.movename} has roll {j} mismatch: observed {damage_roll}, expected {expected_damage_roll}"


def test_super_effective_move(torterra: Pokemon, mareanie: Pokemon): 

    damage_rolls = torterra.calculate_damage_rolls(target_pokemon=mareanie)

    expected_damage_rolls = {
        torterra.move_list[0]: (
            [42, 43, 43, 44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 50],
            [63, 64, 65, 66, 66, 67, 68, 69, 69, 70, 71, 72, 72, 73, 74, 75]
        ), 
        torterra.move_list[1]: (
            [180, 182, 182, 186, 188, 188, 192, 194, 198, 198, 200, 204, 204, 206, 210, 212],
            [270, 272, 276, 278, 282, 284, 288, 290, 294, 296, 300, 302, 306, 308, 312, 318]
        )
    }

    for pokemove, dr in damage_rolls.items():
        assert pokemove in expected_damage_rolls

        expected_dr = expected_damage_rolls[pokemove]

        for i in range(2):
            for j, (damage_roll, expected_damage_roll) in enumerate(zip(dr[i], expected_dr[i])):
                assert damage_roll == expected_damage_roll, f"Pokemove {pokemove.movename} has roll {j} mismatch: observed {damage_roll}, expected {expected_damage_roll}"


def test_merciless(mareanie: Pokemon, spinda: Pokemon): 
    damage_rolls = mareanie.calculate_damage_rolls(target_pokemon=spinda)

    expected_damage_rolls = {
        mareanie.move_list[0]: (
            [61, 63, 63, 64, 64, 66, 66, 67, 67, 69, 69, 70, 70, 72, 72, 73],
            [61, 63, 63, 64, 64, 66, 66, 67, 67, 69, 69, 70, 70, 72, 72, 73]
        ), 
        mareanie.move_list[1]: (
            [88, 90, 90, 91, 93, 94, 94, 96, 97, 97, 99, 100, 100, 102, 103, 105],
            [88, 90, 90, 91, 93, 94, 94, 96, 97, 97, 99, 100, 100, 102, 103, 105]
        )
    }

    for pokemove, dr in damage_rolls.items():
        assert pokemove in expected_damage_rolls

        expected_dr = expected_damage_rolls[pokemove]

        for i in range(2):
            for j, (damage_roll, expected_damage_roll) in enumerate(zip(dr[i], expected_dr[i])):
                assert damage_roll == expected_damage_roll, f"Pokemove {pokemove.movename} has roll {j} mismatch: observed {damage_roll}, expected {expected_damage_roll}"


def test_merciless_against_battle_armor(torterra: Pokemon, mareanie: Pokemon): 
    damage_rolls = mareanie.calculate_damage_rolls(target_pokemon=torterra)

    expected_damage_rolls = {
        mareanie.move_list[0]: (
            [31, 31, 31, 33, 33, 33, 33, 34, 34, 34, 34, 36, 36, 36, 36, 37],
            [31, 31, 31, 33, 33, 33, 33, 34, 34, 34, 34, 36, 36, 36, 36, 37]
        ), 
        mareanie.move_list[1]: (
            [45, 45, 46, 46, 48, 48, 48, 49, 49, 49, 51, 51, 51, 52, 52, 54],
            [45, 45, 46, 46, 48, 48, 48, 49, 49, 49, 51, 51, 51, 52, 52, 54]
        )
    }

    for pokemove, dr in damage_rolls.items():
        assert pokemove in expected_damage_rolls

        expected_dr = expected_damage_rolls[pokemove]

        for i in range(2):
            for j, (damage_roll, expected_damage_roll) in enumerate(zip(dr[i], expected_dr[i])):
                assert damage_roll == expected_damage_roll, f"Pokemove {pokemove.movename} has roll {j} mismatch: observed {damage_roll}, expected {expected_damage_roll}"
