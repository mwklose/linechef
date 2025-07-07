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

    yield spinda


@pytest.fixture
def torterra():
    ...


@pytest.fixture
def mareanie():
    ...


def test_stat_calculation(spinda: Pokemon):
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
