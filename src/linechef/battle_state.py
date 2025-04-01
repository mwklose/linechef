from dataclasses import dataclass


@dataclass
class BattleState:
    opponent_name: str
    opponent_id: int
    opponent_gauntlet_id: int
    opponent_b2b_id: int
    battle_type: int
