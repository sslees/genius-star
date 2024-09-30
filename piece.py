from functools import cache

from transform import *
from triangle import *


class Piece:
    def __init__(self, points, color):
        self.points = points
        self.color = color

    @cache
    def transform(self, tf: Transform):
        points = []
        for a, b, c in self.points:
            if tf.flip:
                a, b, c = reflect(a, b, c)
                a, b, c = rotate(a, b, c, 60)
            if not upward(tf.da, tf.db, tf.dc):
                a, b, c = rotate(a, b, c, 60)
                a, b, c = a - 1, b - 1, c - 1
            a, b, c = rotate(a, b, c, tf.dr)
            points.append((a + tf.da, b + tf.db, c + tf.dc))
        return Piece(points, self.color)

    @cache
    def perimiter(self):
        nbrs = set()
        for p in self.points:
            nbrs.update(neighbors(*p))
        return nbrs - set(self.points)


PIECES = [
    Piece([(0, 0, 0)], "blue"),
    Piece([(0, 0, 0), (0, 0, -1)], "yellow"),
    # Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1)], "aqua"),  # 1
    # Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1)], "aqua"),  # 2
    Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1), (-1, 1, -1)], "orange"),
    Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1), (1, 0, -1)], "purple"),
    Piece([(0, 0, 0), (0, 0, -1), (1, 0, -1), (1, 0, -2)], "pink"),
    Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1), (-1, 1, -1), (-1, 1, 0)], "green"),
    Piece([(0, 0, 0), (0, 0, -1), (0, 1, -1), (1, 0, -1), (-1, 1, -1)], "brown"),
    Piece([(0, 0, 0), (0, 0, -1), (1, 0, -1), (1, 0, -2), (1, 1, -2)], "lime"),
    Piece([(0, 0, 0), (0, 0, -1), (1, 0, -1), (1, 0, -2), (2, 0, -2)], "red"),
    Piece(
        [(0, 0, 0), (0, 0, -1), (0, 1, -1), (-1, 1, -1), (-1, 1, 0), (-1, 0, 0)], "aqua"
    ),  # golden star
]
