from dice import *
from puzzle import *

COMBINATIONS = len(list(rolls()))


def main():
    stars = 0
    for i, result in enumerate(rolls(), 1):
        print(f"Roll {i} of {COMBINATIONS} ({' '.join(map(str, result))}): ", end="")
        puzzle = Puzzle(result)
        while puzzle.step():
            pass
        if puzzle.state == puzzle.State.SOLVED:
            print("STAR")
            stars += 1
        else:
            print("no star")
    print(f"GOLDEN STARS: {stars} of {COMBINATIONS}")


if __name__ == "__main__":
    main()
