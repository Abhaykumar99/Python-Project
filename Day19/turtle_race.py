import turtle
import random

screen = turtle.Screen()
screen.title("Day 19 – Turtle Race")
screen.setup(width=500, height=400)

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

bet = screen.textinput("Make your bet", f"Which turtle will win? {colors}")

turtles = []
y_positions = [-100, -60, -20, 20, 60, 100]

for i, color in enumerate(colors):
    t = turtle.Turtle(shape="turtle")
    t.color(color)
    t.penup()
    t.goto(-230, y_positions[i])
    turtles.append(t)

race_on = False
if bet:
    race_on = True

winner = None
while race_on:
    for t in turtles:
        t.forward(random.randint(1, 10))
        if t.xcor() >= 230:
            race_on = False
            winner = t.pencolor()
            break

if winner:
    if bet.lower() == winner:
        print(f"You won! The {winner} turtle won the race!")
    else:
        print(f"You lost! The {winner} turtle won the race!")

screen.exitonclick()
