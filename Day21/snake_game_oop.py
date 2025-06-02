import turtle
import random

screen = turtle.Screen()
screen.title("Day 21 – Snake Game OOP")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)


class Snake:
    def __init__(self):
        self.segments = []
        self.direction = "stop"
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color("lime")
        self.head.penup()
        self.head.goto(0, 0)

    def add_segment(self):
        seg = turtle.Turtle()
        seg.shape("square")
        seg.color("white")
        seg.penup()
        self.segments.append(seg)

    def reset(self):
        for seg in self.segments:
            seg.goto(2000, 2000)
        self.segments.clear()
        self.head.goto(0, 0)
        self.direction = "stop"

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].goto(self.segments[i - 1].xcor(), self.segments[i - 1].ycor())
        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

        if self.direction == "up":
            self.head.sety(self.head.ycor() + 20)
        elif self.direction == "down":
            self.head.sety(self.head.ycor() - 20)
        elif self.direction == "left":
            self.head.setx(self.head.xcor() - 20)
        elif self.direction == "right":
            self.head.setx(self.head.xcor() + 20)

    def hit_wall(self):
        return abs(self.head.xcor()) > 290 or abs(self.head.ycor()) > 290

    def hit_tail(self):
        return any(seg.distance(self.head) < 20 for seg in self.segments)


class Food:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color("red")
        self.t.penup()
        self.refresh()

    def refresh(self):
        self.t.goto(random.randrange(-13, 13) * 20, random.randrange(-13, 13) * 20)


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.t = turtle.Turtle()
        self.t.color("white")
        self.t.penup()
        self.t.hideturtle()
        self.t.goto(0, 270)
        self.update()

    def update(self):
        self.t.clear()
        self.t.write(f"Score: {self.score}  High: {self.high_score}",
                     align="center", font=("Arial", 16, "normal"))

    def point(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self.update()

    def reset(self):
        self.score = 0
        self.update()


snake = Snake()
food = Food()
scoreboard = Scoreboard()


def go_up():
    if snake.direction != "down":
        snake.direction = "up"

def go_down():
    if snake.direction != "up":
        snake.direction = "down"

def go_left():
    if snake.direction != "right":
        snake.direction = "left"

def go_right():
    if snake.direction != "left":
        snake.direction = "right"


def game_loop():
    snake.move()
    screen.update()

    if snake.head.distance(food.t) < 20:
        food.refresh()
        snake.add_segment()
        scoreboard.point()

    if snake.hit_wall() or snake.hit_tail():
        snake.reset()
        scoreboard.reset()

    screen.ontimer(game_loop, 100)


screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

screen.ontimer(game_loop, 100)
screen.mainloop()
