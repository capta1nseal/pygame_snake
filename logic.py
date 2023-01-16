from random import sample

class Logic:
    '''handle snake movement and game behaviour'''
    def __init__(self, game_dimensions: tuple[int, int] = (24, 15)) -> None:
        self.game_dimensions = game_dimensions

        self.points = 0
        self.length = 1
        self.grow = 3
        self.grow_per_apple = 3
        self.direction = [0] # 0,1,2,3 -> up, right, down, left
        self.max_move_queue = 2

        self.apple = (0, 0)

        self.snake = [(self.game_dimensions[0] // 4, self.game_dimensions[1] // 2)]
        self.spawn_apple()

        self.running = False
        self.started = False

    def spawn_apple(self) -> None:
        '''makes the apple appear in an unoccupied location'''
        candidates = [
            (x, y)
            for y in range(0, self.game_dimensions[1])
            for x in range(0, self.game_dimensions[0])]
        for square in self.snake:
            candidates.remove(square)

        self.apple = sample(candidates, 1)[0]

    def get_dimensions(self) -> tuple[int, int]:
        '''get dimensions of game area'''
        return self.game_dimensions

    def get_snake(self) -> list[tuple[int, int]]:
        '''get list of coordinates that compose the snake'''
        return self.snake

    def get_apple(self) -> tuple[int, int]:
        '''get coordinates of the apple'''
        return self.apple

    def set_new_direction(self, direction: int) -> None:
        '''change direction of snake'''
        if not self.started:
            self.started = True
            self.direction[0] = direction
        elif self.direction[-1] != (direction + 2) % 4 and len(self.direction) <= self.max_move_queue:
            self.direction.append(direction)

    def tick(self) -> None:
        '''move the state of the game forwards'''
        if len(self.direction) > 1:
            self.direction.pop(0)
        if self.grow:
            self.length += 1
            self.grow -= 1
        else:
            self.snake.pop(-1)
        new_position = (0, 0)
        if self.direction[0] == 0:
            new_position = (self.snake[0][0], self.snake[0][1] - 1)
        elif self.direction[0] == 1:
            new_position = (self.snake[0][0] + 1, self.snake[0][1])
        elif self.direction[0] == 2:
            new_position = (self.snake[0][0], self.snake[0][1] + 1)
        elif self.direction[0] == 3:
            new_position = (self.snake[0][0] - 1, self.snake[0][1])
        if new_position[0] < 0 or new_position[1] < 0 or \
                new_position[0] > self.game_dimensions[0] - 1 or \
                new_position[1] > self.game_dimensions[1] - 1 or \
                new_position in self.snake:
            self.stop()
        else:
            self.snake.insert(0, new_position)
        if self.apple in self.snake:
            self.points += 1
            self.grow += self.grow_per_apple
            self.spawn_apple()
            print(self.points)

    def stop(self) -> None:
        '''quit game'''
        self.running = False
