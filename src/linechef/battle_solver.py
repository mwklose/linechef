from pathlib import Path
from typing import List
from linechef.ai import AI, OpponentAI, OwnAI
from linechef.battle_state import BattleState
from linechef.pokeitem import Pokeitem
from linechef.pokemon import Pokemon
import sys
from dataclasses import dataclass


@dataclass
class BattleSolver:
    opposing_team: List[Pokemon]
    own_box: List[Pokemon]
    own_items: List[Pokeitem]

    own_ai: AI
    opponent_ai: AI

    def generate_initial_battle_state(self) -> BattleState:

        ...

    def simulate_battle(self, verbose: bool = False, worst_case_scenario: bool = False) -> BattleState:
        # Determine own team
        my_team = self.own_ai.construct_team(
            opposing_team=self.opposing_team,
            own_box=self.own_box
        )

        # Set up initial battle state
        bs: BattleState = self.generate_initial_battle_state()

        # While battle still going on:
        while not bs.is_battle_completed():
            ...
            # Request next actions

            # Switch in if needed

            # Continue onwards

        ...

    def worst_case_scenario(self, opposing_team: List[Pokemon], own_team: List[Pokemon]):
        ...

    def train(self, ):
        ...
    ...


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
        raise Exception(
            "[Usage]: first arg is route like 103, second arg is trainer name.")

    # Load opposing team
    opposing_team, opposing_trainer_id = Pokemon.find_by_route_and_name(
        route=sys.argv[1], trainer_name=sys.argv[2])

    # Load own team
    own_box: List[Pokemon] = Pokemon.get_pokemon_from_file(
        filename="db/pokemon.txt")

    # Load own items

    own_items: List[Pokeitem] = Pokeitem.read_items_from_file(
        filename=Path("db/item_caps.csv"),
        level_cap=opposing_trainer_id
    )

    raise Exception("Finished test")

    # TODO: get battle state, begin model deployment?
    bsolver = BattleSolver(
        opposing_team=opposing_team,
        own_box=own_box,
        own_items=own_items,
        own_ai=OwnAI(),
        opponent_ai=OpponentAI()
    )

    # Run solver
    # 1. Create Own Team
    # 2. Simulate
    # 3. Save Top Results per generation
    # 4. Run worst-case scenario

    ...
