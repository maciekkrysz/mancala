from classes.side import *
from copy import deepcopy
from consts import *
from utils.utilities import *
from random import shuffle


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

        successors = AI.movgen(players[current_player])
        if not successors:
            return AI.get_rating(players[0]), ""

        path = ""
        if current_player == 0:
            value = float('-inf')
        elif current_player == 1:
            value = float('inf')

        for s, next_player in successors:
            # p_copy = [deepcopy(players[0]), deepcopy(players[1])]
            p_copy = deepcopy(players)
            p_copy[current_player].move(
                s, p_copy[other_player(current_player)])

            if next_player == 'other':
                next_p = other_player(current_player)
            elif next_player == 'me':
                next_p = current_player

            t_value, t_path = AI._minmax(p_copy, depth+1, next_p)

            if (current_player == 0 and value < t_value) or (current_player == 1 and value > t_value):
                value = t_value
                path = str(s) + ' ' + t_path
        return value, path

    def alphabeta(p1, p2):
        p1_copy = deepcopy(p1)
        p2_copy = deepcopy(p2)
        return AI._alphabeta([p1_copy, p2_copy])

    def _alphabeta(players, depth=0, alpha=float('-inf'), beta=float('inf'), current_player=0):

        if depth == ALPHABETA_DEPTH:
            return AI.get_rating(players[0]), ""

        successors = AI.movgen(players[current_player])
        shuffle(successors)

        if not successors:
            return AI.get_rating(players[0]), ""

        # MAX's turn
        if current_player == 0:
            val = float('-inf')
        # MIN's turn
        elif current_player == 1:
            val = float('inf')

        val_path = ""

        for s, next_player in successors:
            if next_player == 'me':
                next_p = current_player
            elif next_player == 'other':
                next_p = other_player(current_player)

            p_copy = deepcopy(players)
            p_copy[current_player].move(
                s, p_copy[other_player(current_player)])

            # print(p_copy, depth+1, alpha, beta, next_p)

            t_value, t_path = AI._alphabeta(
                p_copy, depth+1, alpha, beta, next_p)

            # MAX's turn to move
            if current_player == 0:
                if t_value > val:
                    val = t_value
                    val_path = t_path
                    ret_s = s
                if t_value >= beta:
                    return t_value, str(s) + ' ' + t_path
                if t_value > alpha:
                    alpha = t_value
                # if t_value > alpha:
                #     alpha = t_value
                # if alpha > beta:
                #     return alpha, str(s) + ' ' + t_path
                # return alpha, str(s) + ' ' + t_path

            # MIN's turn to move
            elif current_player == 1:
                if t_value < val:
                    val = t_value
                    val_path = t_path
                    ret_s = s
                if t_value <= alpha:
                    return t_value, str(s) + ' ' + t_path
                if t_value < beta:
                    beta = t_value
                # return val, str(s) + ' ' + t_path
                # if t_value < beta:
                #     beta = t_value
                # if beta <= alpha:
                #     return beta, str(s) + ' ' + t_path
                # return beta, str(s) + ' ' + t_path
        return val, str(ret_s) + ' ! ' + val_path
        
        # return AI.get_rating(players[0]), ""

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
        return p1.count() - n * k
