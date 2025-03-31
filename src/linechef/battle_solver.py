from linechef.battle_state import BattleState
import sys

if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) < 3:
        raise Exception(
            "[Usage]: first arg is route like 103, second arg is trainer name.")
    BattleState.find_by_route_and_name(
        route=sys.argv[1], trainer_name=sys.argv[2])

    # TODO: get battle state, begin model deployment?
    ...
