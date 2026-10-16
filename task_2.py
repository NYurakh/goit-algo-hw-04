import turtle


def koch_curve(t, length, level):
    if level == 0:
        t.forward(length)
        return

    length /= 3

    koch_curve(t, length, level - 1)
    t.left(60)

    koch_curve(t, length, level - 1)
    t.right(120)

    koch_curve(t, length, level - 1)
    t.left(60)

    koch_curve(t, length, level - 1)


def draw_koch_snowflake(level):
    screen = turtle.Screen()
    screen.title(f"Koch Snowflake - Level {level}")
    screen.setup(width=900, height=700)
    screen.tracer(0)
    screen.bgcolor("black")

    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    t.color("white")

    t.penup()
    t.goto(-200, 120)
    t.pendown()

    for _ in range(3):
        koch_curve(t, 400, level)
        t.right(120)

    t.hideturtle()
    screen.update()
    turtle.done()


def main():
    try:
        level = int(
            input("Enter recursion level (0-6): ")
        )  # ? more is possible, but it will take a long time to render and can crash the program

        if not 0 <= level <= 6:
            raise ValueError("Level must be between 0 and 6.")

        draw_koch_snowflake(level)
    except ValueError:
        print("Invalid input. Please enter a non-negative integer.")


if __name__ == "__main__":
    main()
