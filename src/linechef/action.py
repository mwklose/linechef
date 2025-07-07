from abc import abstractmethod
from dataclasses import dataclass

from linechef.battle_state import BattleState
from linechef.pokemon import Pokemon
from linechef.pokemove import Pokemove


SWITCH_PRIORITY = 10000
MEGAEVOLVE_PRIORITY = 9000
PRIORITY_MULTIPLIER = 1000
MAX_SPEED = 998


@dataclass
class Slot:
    trainer: str
    pokemon: Pokemon

    def get_pokemon(self) -> Pokemon:
        return self.pokemon

    def set_pokemon_in_slot(self, poke: Pokemon) -> None:
        self.pokemon = poke
        return


class Action:
    performing_slot: Slot

    @abstractmethod
    def get_performing_slot(self) -> Slot:
        return self.performing_slot

    @abstractmethod
    def get_action_speed(self, trick_room_active: bool = False) -> int:
        ...

    @abstractmethod
    def perform_action(self, bs: BattleState) -> BattleState:
        ...


@dataclass
class AttackAction(Action):
    performing_slot: Slot
    target_slot: Slot | None
    move: Pokemove
    best_case: bool = False
    trick_room_active: bool = False

    def get_action_speed(self, trick_room_active: bool = False) -> int:
        priority_bracket: int = self.move.get_priority() * PRIORITY_MULTIPLIER
        speed_in_bracket: int = self.performing_slot.get_pokemon(
        ).get_functional_speed(best_case=self.best_case)

        if self.trick_room_active and speed_in_bracket < MAX_SPEED:
            speed_in_bracket = 1024 - speed_in_bracket

        return priority_bracket + speed_in_bracket

    def perform_action(self, bs: BattleState) -> BattleState:
        return super().perform_action()


@dataclass
class MegaevolveAction(Action):
    performing_slot: Slot

    def get_action_speed(self, trick_room_active: bool = False) -> int:
        return MEGAEVOLVE_PRIORITY + self.performing_slot.get_pokemon().get_speed()

    def perform_action(self, bs: BattleState) -> BattleState:
        return super().perform_action()


@dataclass
class SwitchAction(Action):
    performing_slot: Slot
    target_slot: Slot
    switching_to_pokemon: Pokemon

    def get_action_speed(self, trick_room_active: bool = False):
        # Occurs first regardless
        return SWITCH_PRIORITY + self.performing_slot.get_pokemon().get_speed()

    def perform_action(self, bs: BattleState) -> BattleState:
        # Will always be able to switch before others...
        if self.performing_slot.get_pokemon().is_fainted():
            return bs

        return super().perform_action()
