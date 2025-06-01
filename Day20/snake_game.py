import turtle
import random

screen = turtle.Screen()
screen.title("Day 20 – Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

score = 0
high_score = 0
segments = []
running = True

head = turtle.Turtle()
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randrange(-13, 13) * 20, random.randrange(-13, 13) * 20)

scoreboard = turtle.Turtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 270)


def update_score():
    scoreboard.clear()
    scoreboard.write(f"Score: {score}  High Score: {high_score}",
                     align="center", font=("Arial", 16, "normal"))


def add_segment():
    seg = turtle.Turtle()
    seg.shape("square")
    seg.color("white")
    seg.penup()
    segments.append(seg)


def reset():
    global score
    for seg in segments:
        seg.hideturtle()
        seg.goto(2000, 2000)
    segments.clear()
    head.goto(0, 0)
    head.direction = "stop"
    score = 0
    update_score()


def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"


def game_loop():
    global score, high_score, running

    if not running:
        return

    # Move body segments
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    # Move head
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

    screen.update()

    # Food collision
    if head.distance(food) < 20:
        food.goto(random.randrange(-13, 13) * 20, random.randrange(-13, 13) * 20)
        add_segment()
        score += 10
        if score > high_score:
            high_score = score
        update_score()

    # Wall collision
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        reset()

    # Self collision
    for seg in segments:
        if seg.distance(head) < 20:
            reset()
            break

    screen.ontimer(game_loop, 100)


update_score()

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

screen.ontimer(game_loop, 100)
screen.mainloop()
