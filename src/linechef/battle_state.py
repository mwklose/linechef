from dataclasses import dataclass
from typing import List

from linechef.pokemove import Pokemove


@dataclass
class BattleState:
    opponent_name: str
    opponent_id: int
    opponent_gauntlet_id: int
    opponent_b2b_id: int
    battle_type: int

    def submit_moves(self, opponent_moves: List[Pokemove], own_moves: List[Pokemove]) -> "BattleState":

        # Determine order of actions

        #

        ...

    def score_battle_state(self) -> int:
        ...
