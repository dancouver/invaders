import random
from constants import *

def create_stars(canvas):
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
    for star in stars:
        x, y = star
        canvas.create_text(x, y, text="*", fill=COLOR, font=("Arial", 10), tag="star")

def animate_stars(canvas, root):
    for star in canvas.find_withtag("star"):
        x, y = canvas.coords(star)
        canvas.move(star, 0, 1)
        if y > HEIGHT:
            canvas.coords(star, x, 0)
    root.after(50, animate_stars, canvas, root)
