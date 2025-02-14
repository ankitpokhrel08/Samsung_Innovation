import turtle

# Create screen
screen = turtle.Screen()
screen.title("Interactive Turtle")
screen.bgcolor("lightblue")

# Create turtle
t = turtle.Turtle()
t.shape("turtle")
t.speed(3)

# Define movement functions
def move_forward():
    t.forward(20)

def move_backward():
    t.backward(20)

def turn_left():
    t.left(15)

def turn_right():
    t.right(15)

def clear_screen():
    t.clear()  # Clears the drawings

# Listen for keyboard events
screen.listen()
screen.onkey(move_forward, "Up")       # Move forward on Up arrow key
screen.onkey(move_backward, "Down")     # Move backward on Down arrow key
screen.onkey(turn_left, "Left")         # Turn left on Left arrow key
screen.onkey(turn_right, "Right")       # Turn right on Right arrow key
screen.onkey(clear_screen, "c")         # Clear screen on 'c' key

# Keep the window open
screen.mainloop()