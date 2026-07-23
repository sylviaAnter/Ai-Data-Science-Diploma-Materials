import random
import curses

# Initialize screen
screen = curses.initscr()
curses.curs_set(0)

# Get screen size
height, width = screen.getmaxyx()

# Create window
window = curses.newwin(height, width, 0, 0)
window.keypad(True)
window.timeout(125)
window.border(0)

# Snake initial position
snake_x = width // 2
snake_y = height // 2

snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Draw snake
for y, x in snake:
    window.addch(y, x, curses.ACS_CKBOARD)

# Food position (y, x)
food = [height // 2, width // 4]
window.addch(food[0], food[1], curses.ACS_PI)

key = curses.KEY_RIGHT

while True:

    # Read keyboard
    next_key = window.getch()

    if next_key != -1:
        key = next_key

    # Current head
    new_head = [snake[0][0], snake[0][1]]

    # Move
    if key == curses.KEY_UP:
        new_head[0] -= 1

    elif key == curses.KEY_DOWN:
        new_head[0] += 1

    elif key == curses.KEY_LEFT:
        new_head[1] -= 1

    elif key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Collision
    if (
        new_head[0] == 0
        or new_head[0] == height - 1
        or new_head[1] == 0
        or new_head[1] == width - 1
        or new_head in snake
    ):
        curses.endwin()
        print("Game Over!")
        quit()

    # Insert new head
    snake.insert(0, new_head)

    # Food eaten
    if snake[0] == food:

        while True:
            food = [
                random.randint(1, height - 2),
                random.randint(1, width - 2)
            ]

            if food not in snake:
                break

        window.addch(food[0], food[1], curses.ACS_PI)

    else:
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    # Draw head
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    # Draw border
    window.border(0)




# curses.COLOR_BLACK
# curses.COLOR_WHITE
# curses.COLOR_RED
# curses.COLOR_GREEN
# curses.COLOR_BLUE
# curses.COLOR_YELLOW
# curses.COLOR_CYAN
# curses.COLOR_MAGENTA