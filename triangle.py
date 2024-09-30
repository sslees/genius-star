# https://www.boristhebrave.com/2021/05/23/triangle-grids/
# https://github.com/BorisTheBrave/grids/blob/main/src/updown_tri.py

SQRT3 = 3**0.5


def valid(a, b, c):
    return a + b + c in [1, 2]


def center(a, b, c):
    return a / 2 - c / 2, b * SQRT3 / 3 - a * SQRT3 / 6 - c * SQRT3 / 6


def upward(a, b, c):
    return a + b + c == 2


def corners(a, b, c):
    if upward(a, b, c):
        return [center(a + 1, b, c), center(a, b + 1, c), center(a, b, c + 1)]
    else:
        return [center(a - 1, b, c), center(a, b - 1, c), center(a, b, c - 1)]


def neighbors(a, b, c):
    if upward(a, b, c):
        return [(a - 1, b, c), (a, b - 1, c), (a, b, c - 1)]
    else:
        return [(a + 1, b, c), (a, b + 1, c), (a, b, c + 1)]


def rotate(a, b, c, deg):
    assert deg % 60 == 0
    deg = (deg % 360 + 360) % 360
    if deg == 60:
        return 1 - b, 1 - c, 1 - a
    if deg == 120:
        return c, a, b
    if deg == 180:
        return 1 - a, 1 - b, 1 - c
    if deg == 240:
        return b, c, a
    if deg == 300:
        return 1 - c, 1 - a, 1 - b
    return a, b, c


def reflect(a, b, c):
    return 1 - c, 1 - b, 1 - a
