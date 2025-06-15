from dataclasses import dataclass
from typing import List

from linechef.pokeitem import Pokeitem
from linechef.pokemon import Pokemon


@dataclass
class BattleState:
    opponent_name: str
    opponent_id: int
    opponent_gauntlet_id: int
    opponent_b2b_id: int
    battle_type: int

    opponent_remaining_pokemon: List[Pokemon]

    own_remaining_pokemon: List[Pokemon]

    def __post_init__(self) -> None:
        self.active_trick_room = False
        self.trick_room_turns = 0
        self.other_moves = []

        self.opponent_fainted_pokemon: List[Pokemon] = []
        self.own_fainted_pokemon: List[Pokemon] = []

        self.own_consumed_items: List[Pokeitem] = []

    def is_battle_completed(self) -> bool:
        return len(self.own_remaining_pokemon) == 0

    # def submit_actions(self, actions_requested: List[Action], worst_case: bool = False, verbose: bool = False) -> "BattleState":
    #     # Sanity checking - ensure no pokemon is already fainted.

    #     for m in actions_requested:
    #         poke: Pokemon = m.get_performing_slot().get_pokemon()
    #         if poke.is_fainted():
    #             raise Exception(
    #                 f"[BattleState] Pokemon {poke} is already fainted, before applying any move?")

    #     for action_requested in sorted(actions_requested, key=lambda x: x.get_action_speed(trick_room_active=self.active_trick_room)):
    #         pokemon: Pokemon = action_requested.get_performing_slot().get_pokemon()
    #         if pokemon.is_fainted():
    #             if verbose:
    #                 print(
    #                     f"\tPokemon {pokemon.name} already fainted; not performing move")
    #             continue

    #         # Perform moves in order
    #         action_requested.perform_action(bs=self)

    #     # Switch in next if needed
    #     # TODO

    #     # Return new battle state

    #     if self.active_trick_room:
    #         self.trick_room_turns -= 1
    #         self.active_trick_room: bool = self.trick_room_turns > 0

    #     return self

    def score_battle_state(self) -> int:
        ...
