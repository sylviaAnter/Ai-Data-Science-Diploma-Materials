import random
import curses

class Snake:
    def __init__(self, y, x):
        self.body = [[y, x],[y, x - 1],[y, x - 2]]
        self.direction = curses.KEY_RIGHT

    def change_direction(self, key):

        opposite = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT
        }

        if key != -1 and key != opposite[self.direction]:
            self.direction = key

    def move(self):

        head = self.body[0].copy()

        if self.direction == curses.KEY_UP:
            head[0] -= 1

        elif self.direction == curses.KEY_DOWN:
            head[0] += 1

        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1

        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1

        self.body.insert(0, head)

    def remove_tail(self):
        return self.body.pop()

    def draw(self, window):

        for y, x in self.body:
            window.addch(y,x,curses.ACS_BLOCK,curses.color_pair(1))

    def clash(self, height, width):

        head = self.body[0]

        if head[0] == 0 or head[0] == height - 1 or head[1] == 0 or head[1] == width - 1 :
            return True
        else : 
            return False



class Food:

    def __init__(self, height, width, snake):
        self.height = height
        self.width = width
        self.position = []
        self.generate(snake)

    def generate(self, snake):

        while True:
            food = [random.randint(1, self.height - 2),random.randint(1, self.width - 2)]
            if food not in snake.body:
                self.position = food
            break

    def draw(self, window):
        window.addch(self.position[0],self.position[1],curses.ACS_BLOCK,curses.color_pair(2))


class Game:

    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE,curses.COLOR_BLACK) 
        self.height, self.width = self.screen.getmaxyx()

        self.window = curses.newwin(
            self.height,
            self.width,
            0,
            0
        )
        self.window.bkgd(' ', curses.color_pair(3))

        self.window.keypad(True)
        self.window.timeout(50)

        self.snake = Snake(
            self.height // 2,
            self.width // 2
        )

        self.food = Food(
            self.height ,
            self.width,
            self.snake
        )

    def update(self):

        key = self.window.getch()

        self.snake.change_direction(key)

        self.snake.move()

        if self.snake.clash(self.height, self.width)==True:
            return False

        if self.snake.body[0] == self.food.position:

            self.food.generate(self.snake)

        else:

            tail = self.snake.remove_tail()
            self.window.addch(tail[0], tail[1], ' ')

        return True

    def draw(self):

        self.food.draw(self.window)
        self.snake.draw(self.window)

    

    def run(self):

        while True:

            if self.update()==False:
                break

            self.draw()

        curses.endwin()
        print("Game Over")



game = Game()
game.run()