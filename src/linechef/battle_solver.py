from linechef.pokemon import Pokemon
import sys
from dataclasses import dataclass


@dataclass
class BattleSolver:
    ...


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        raise Exception(
            "[Usage]: first arg is route like 103, second arg is trainer name.")

    # Load opposing team
    opposing_team = Pokemon.find_by_route_and_name(
        route=sys.argv[1], trainer_name=sys.argv[2])

    # TODO: get battle state, begin model deployment?

    # Load own team
    own_box = Pokemon.get_pokemon_from_file(filename="db/pokemon.txt")

    # Load own items
    own_items = "TODO"

    # Run solver
    # 1. Create Own Team
    # 2. Simulate
    # 3. Save Top Results per generation
    # 4. Run worst-case scenario

    ...
