import turtle
import random

# Create screen
screen = turtle.Screen()
screen.bgcolor("black")  # Set background color

# Create turtle
t = turtle.Turtle()
t.speed(1000)  # Set maximum speed
turtle.colormode(255)  # Use RGB colors

# Function to generate random colors
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Draw circular pattern
for i in range(10000):
    t.pencolor(random_color())  # Set random color
    t.circle(100)  # Draw a circle
    t.left(10)  # Rotate slightly for next circle

# Keep window open
turtle.done()