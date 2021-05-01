from classes.side import *
from copy import deepcopy
from consts import *
from utils.utilities import *

class AI:
    def __init__(self, own_side, other_side):
        self.side = own_side
        self.opponent = other_side


    def minmax(p1, p2):
        p1_copy = deepcopy(p1)
        p2_copy = deepcopy(p2)
        return AI._minmax([p1_copy, p2_copy])

    def _minmax(players, depth=0, current_player=0):
        # current_player == 0 or 1, 0 -> me; 1 -> other
        successors = []
        if depth == MINMAX_DEPTH:
            return AI.get_rating(players[0]), ""
        else:
            successors = AI.movgen(players[current_player])

        if not successors:
            return AI.get_rating(players[0]), ""
        else:
            path = ""
            if current_player == 0:
                value = float('inf')
            elif current_player == 1:
                value = float('-inf')

            for s, next_player in successors:
                # p_copy = [deepcopy(players[0]), deepcopy(players[1])]
                p_copy = deepcopy(players)
                p_copy[current_player].move(s, p_copy[other_player(current_player)])

                if next_player == 'other':
                    next_p = other_player(current_player)
                elif next_player == 'me':
                    next_p = current_player

                t_value, t_path = AI._minmax(p_copy, depth+1, next_p)

                if (current_player == 0 and value > t_value) or (current_player == 1 and value < t_value):
                    value = t_value
                    path = str(s) + ' ' + t_path
            return value, path

    def movgen(p):
        moves = []
        # cups: [H][0][1][2][3][4][5]
        cups = p.get_cups()
        for i, cup in enumerate(cups[1:], 1):
            if cup == 0:
                pass
            else:
                if (cup - i) % ((2 * n) + 1) == 0:
                    moves.append((i - 1, 'me'))
                else:
                    moves.append((i - 1, 'other'))
        return moves

    def get_rating(p1):
        return n * k - p1.count()