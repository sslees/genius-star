from collections import defaultdict
from enum import Enum, auto
from functools import cache
from itertools import product

from piece import *
from transform import *

BOUNDS = [
    (a, b, c)
    for b, a, c in product(range(4, -4, -1), range(-3, 5), range(4, -4, -1))
    if valid(a, b, c)
    and ((a < 3 and b < 3 and c < 3) or (a > -2 and b > -2 and c > -2))
]


class Puzzle:
    class State(Enum):
        ADDING = auto()
        MOVING = auto()
        DISCARDING = auto()
        SOLVED = auto()
        EMPTY = auto()

    def __init__(self, blockers):
        self.blockers = {BOUNDS[i - 1] for i in blockers}
        self.unblocked = [
            p
            for p in sorted(BOUNDS, key=lambda p: -(abs(p[0]) + abs(p[1]) + abs(p[2])))
            if p not in self.blockers
        ]
        self.unblockedSet = set(self.unblocked)
        self.transformsAtPoint: defaultdict[tuple, list[Transform]] = defaultdict(list)
        self.pieces: list[Piece] = []
        self.transformsRemaining: dict[Piece, list[Transform]] = {}
        self.state = self.State.ADDING
        for piece in PIECES:
            for tf in self.unfiltered_transforms(piece):
                for point in piece.transform(tf).points:
                    self.transformsAtPoint[point].append(tf)

    @cache
    def unfiltered_transforms(self, piece: Piece) -> list[Transform]:
        transforms = []
        points_seen = set()
        for da, db, dc in self.unblocked:
            for dr in range(0, 360, 120):
                for flip in [False, True]:
                    tf = Transform(da, db, dc, dr, flip)
                    transformed = piece.transform(tf)
                    points = frozenset(transformed.points)
                    if points not in points_seen and all(
                        p in self.unblockedSet for p in transformed.points
                    ):
                        transforms.append(tf)
                        points_seen.add(points)
        return transforms

    def filtered_transforms(self, piece: Piece) -> list[Transform]:
        occupied = self.occupied_points()
        return sorted(
            [
                tf
                for tf in self.unfiltered_transforms(piece)
                if tf.conflicts == 0 and self.check_gaps(piece.transform(tf))
            ],
            key=lambda tf: sum(
                1
                for n in piece.transform(tf).perimiter()
                if n in occupied or n not in self.unblockedSet
            ),
        )

    def transformed_piece(self, piece: Piece):
        return piece.transform(self.transformsRemaining[piece][-1])

    def transformed_pieces(self):
        return [self.transformed_piece(piece) for piece in self.pieces]

    def occupied_points(self):
        points = set()
        for piece in self.transformed_pieces():
            points.update(piece.points)
        return points

    def check_gaps(self, piece: Piece):
        occupied = self.occupied_points()
        occupied.update(piece.points)
        seen = set()
        areas = []
        for point in self.unblocked:
            if point not in occupied and point not in seen:
                area = 0
                seen.add(point)
                unprocessed = [point]
                while unprocessed:
                    current = unprocessed.pop()
                    area += 1
                    for nbr in neighbors(*current):
                        if (
                            nbr in self.unblockedSet
                            and nbr not in occupied
                            and nbr not in seen
                        ):
                            seen.add(nbr)
                            unprocessed.append(nbr)
                areas.append(area)
                if areas.count(1) == 2 or areas.count(2) == 2:
                    return False
        return True

    def step(self):
        changed = False
        while not changed and self.state not in [self.State.SOLVED, self.State.EMPTY]:
            if self.state == self.State.ADDING:
                next_piece = max(
                    (piece for piece in PIECES if piece not in self.pieces),
                    key=lambda p: len(p.points),
                    default=None,
                )
                if next_piece is None:
                    self.state = self.State.SOLVED
                elif self.place(next_piece):
                    changed = True
                else:
                    self.state = self.State.MOVING if self.pieces else self.State.EMPTY
            elif self.state == self.State.MOVING:
                if self.move():
                    self.state = self.State.ADDING
                    changed = True
                else:
                    self.state = self.State.DISCARDING
            elif self.state == self.State.DISCARDING:
                self.discard()
                self.state = self.State.MOVING if self.pieces else self.State.EMPTY
                changed = True
        return self.state not in [self.State.SOLVED, self.State.EMPTY]

    def place(self, next_piece: Piece):
        remaining = self.filtered_transforms(next_piece)
        if not remaining:
            return False
        self.transformsRemaining[next_piece] = remaining
        self.pieces.append(next_piece)
        self.updateTransforms(self.transformed_piece(next_piece), removing=False)
        return True

    def move(self):
        if len(self.transformsRemaining[self.pieces[-1]]) == 1:
            return False
        previous = self.transformed_piece(self.pieces[-1])
        self.transformsRemaining[self.pieces[-1]].pop()
        next_transformed = self.transformed_piece(self.pieces[-1])
        self.updateTransforms(previous, removing=True)
        self.updateTransforms(next_transformed, removing=False)
        return True

    def discard(self):
        self.updateTransforms(self.transformed_piece(self.pieces.pop()), removing=True)

    def updateTransforms(self, piece: Piece, removing):
        for point in piece.points:
            for tf in self.transformsAtPoint[point]:
                tf.conflicts += -1 if removing else 1

    def resume(self):
        if self.state == self.State.EMPTY:
            return False
        assert self.state == self.State.SOLVED
        self.state = self.State.DISCARDING
        return True
