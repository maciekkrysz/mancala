from consts import *


"""
cups
    [H][0][1][2][3][4][5]
    [5][4][3][2][1][0][H]
"""


class Side:
    def __init__(self, is_AI=False):
        self.home_cup = 0
        self.cups = [k for i in range(n)]
        self.AI = is_AI

    def move(self, index, other_side):
        rocks = self.cups[index]
        self.cups[index] = 0
        result, end_index = self.add(index, rocks, other_side)
        if result == 'steal':
            self.steal(end_index, other_side)

        return result

    def add(self, start_index, rocks, other_side, side_move=True):
        while True:
            if rocks == 0:
                return 'end', 0
            if start_index > 0:
                for index in range(start_index)[::-1]:
                    self.cups[index] += 1
                    rocks -= 1
                    if rocks <= 0:
                        if side_move and self.cups[index] == 1 and side_move==True:
                            return 'steal', index
                        return 'end', 0
            if side_move and rocks > 0:
                self.home_cup += 1
                rocks -= 1
                if rocks <= 0:
                    return 'again', 0
                    
            if rocks < n:
                return other_side.add(n, rocks, other_side=self, side_move=False)
            else:
                rocks -= n
                other_side.add(n, n, other_side=self, side_move=False)
            start_index = n

    def steal(self, cup_index, other_side):
        if not other_side.is_empty(n-cup_index - 1):
            self.cups[cup_index] = 0

            # +1 beacause of our cup
            self.home_cup += other_side.steal_victim(n-cup_index - 1) + 1

    def steal_victim(self, index):
        rocks = self.cups[index]
        self.cups[index] = 0
        return rocks

    def possible_move(self):
        for cup in self.cups:
            if cup > 0:
                return True
        return False

    def get_cups(self):
        return [self.home_cup] + self.cups

    def count(self):
        return sum(self.cups) + self.home_cup

    def is_empty(self, index):
        return self.cups[index] == 0
