from itertools import product
from random import choice

DICE = [
    [1, 5, 15, 34, 44, 48],
    [2, 4, 7, 8, 9, 11, 16, 17],
    [10, 27, 31],
    [12, 13, 23, 24, 32, 33, 41, 42],
    [18, 22, 39],
    [19, 20, 21, 28, 29, 30],
    [25, 26, 36, 37, 38, 40, 45, 47],
]


def rolls():
    return product(*DICE)


def roll():
    return sorted(choice(d) for d in DICE)
