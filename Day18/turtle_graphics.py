import turtle
import random

screen = turtle.Screen()
screen.title("Day 18 – Turtle Graphics")
screen.bgcolor("black")
screen.setup(width=800, height=800)

t = turtle.Turtle()
t.speed(0)
t.width(2)


def draw_polygon(sides, size, color):
    angle = 360 / sides
    t.pencolor(color)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(sides):
        t.forward(size)
        t.right(angle)
    t.end_fill()


def draw_spirograph(circle_size, gap_angle):
    colors = ["red", "coral", "orange", "gold", "yellow",
              "lime", "cyan", "dodger blue", "blue violet", "magenta"]
    t.penup()
    t.goto(0, 0)
    t.pendown()
    for i in range(int(360 / gap_angle)):
        t.pencolor(colors[i % len(colors)])
        t.circle(circle_size)
        t.right(gap_angle)


def scatter_polygons(count=12):
    colors = ["red", "orange", "yellow", "green", "cyan",
              "blue", "magenta", "white", "pink", "lime"]
    for _ in range(count):
        t.penup()
        t.goto(random.randint(-350, 350), random.randint(-350, 350))
        t.pendown()
        draw_polygon(random.randint(3, 8), random.randint(20, 60), random.choice(colors))


scatter_polygons()
t.clear()
draw_spirograph(circle_size=100, gap_angle=10)
t.hideturtle()
screen.mainloop()
