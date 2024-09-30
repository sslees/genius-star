from tkinter import Canvas, Tk

from dice import *
from puzzle import *
from triangle import *

SCALE = 100
LABELS = {point: i for i, point in enumerate(BOUNDS, 1)}


def triangle(canvas: Canvas, point, color):
    x0 = (canvas.winfo_width() - 2) // 2
    y0 = (canvas.winfo_height() - 2) // 2
    canvas.create_polygon(
        [(x0 + x * SCALE, y0 - y * SCALE) for x, y in corners(*point)],
        outline="black",
        fill=color,
        width=4,
    )
    cx, cy = center(*point)
    canvas.create_text(
        x0 + cx * SCALE,
        y0 - cy * SCALE,
        text=LABELS[point],
        anchor="center",
        font=("Arial", 18, "bold"),
    )


def update(canvas: Canvas, puzzle: Puzzle):
    canvas.delete("all")
    for p in BOUNDS:
        if p in puzzle.blockers:
            triangle(canvas, p, "dimgrey")
        else:
            triangle(canvas, p, "white")
    for piece in puzzle.transformed_pieces():
        for p in piece.points:
            triangle(canvas, p, piece.color)
    if puzzle.step():
        canvas.master.after(10, update, canvas, puzzle)
    else:
        canvas.master.after(1000, update, canvas, Puzzle(roll()))


def main():
    root = Tk()
    canvas = Canvas(root, width=1000, height=800)
    canvas.pack()
    root.update_idletasks()
    update(canvas, Puzzle(roll()))
    root.mainloop()


if __name__ == "__main__":
    main()
