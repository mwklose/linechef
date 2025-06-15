from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from linechef.action import Action
from linechef.battle_state import BattleState
from linechef.pokemon import Pokemon


class AI:

    @abstractmethod
    def find_next_move(self, bs: BattleState) -> Action:
        # TODO: attack, or switch?
        ...

    @abstractmethod
    def find_next_pokemon(self, bs: BattleState) -> BattleState:
        ...

    @abstractmethod
    def construct_team(self, opposing_team: List[Pokemon], own_box: List[Pokemon]) -> List[Pokemon]:

        ...


@dataclass
class OwnAI(AI):

    ...


@dataclass
class OpponentAI(AI):

    ...

    def construct_team(self, opposing_team: List[Pokemon], own_box: List[Pokemon]) -> List[Pokemon]:
        return opposing_team
