from tkinter import *
import random

BOARD_WIDTH = 800
BOARD_HEIGHT = 800
SPEED = 80
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#42e6f5'
FOOD_COLOR = '#ff0000'
BACKGROUND_COLOR = '#42f542'


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
            self.squares.append(square)


class Food:
    def __init__(self):
        # placing food randomly
        x = random.randint(0, int((BOARD_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((BOARD_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag='food')


def next_frame(snake, food):
    # unpacking coordinates of the snake's head
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    # checking if the snake's head is on the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f'Score: {score}')
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_frame, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'down' and direction != 'up':
        direction = new_direction

    elif new_direction == 'up' and direction != 'down':
        direction = new_direction

    elif new_direction == 'left' and direction != 'right':
        direction = new_direction

    elif new_direction == 'right' and direction != 'left':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    # checking if the snake's head hit the edge of the board or the snake's body
    if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
        return True
    return any(
        x == body_part[0] and y == body_part[1]
        for body_part in snake.coordinates[1:]
    )


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('times new roman', 100),
                       text='GAME OVER',
                       fill='red')


window = Tk()
window.title('Snake game')
window.resizable(False, False)

score = 0
direction = 'right'

label = Label(window, text=f"Score: {score}", font=('times new roman', 50))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=BOARD_HEIGHT, width=BOARD_WIDTH)
canvas.pack()
window.update()

# centering window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# binding keys
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Left>', lambda event: change_direction('left'))

snake = Snake()
food = Food()
next_frame(snake, food)
window.mainloop()
