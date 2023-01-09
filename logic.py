from random import sample

class Logic:
    def __init__(self, game_dimensions: tuple[int, int] = (50, 30)) -> None:
        self.game_dimensions = game_dimensions
        
        self.create_game_state()

        self.points = 0
        self.length = 1
        self.grow = 3
        
        self.running = False
        self.started = False
    
    def create_game_state(self) -> None:
        '''create objects for game start'''
        self.snake = [(self.game_dimensions[0] // 4, self.game_dimensions[1] // 2)]
        self.direction = 1 # 0,1,2,3 -> up, right, down, left
        self.new_direction = 1
        self.spawn_apple()

    def spawn_apple(self) -> None:
        '''makes the apple appear in an unoccupied location'''
        candidates = [(x, y) for y in range(0, self.game_dimensions[1]) for x in range(0, self.game_dimensions[0])]
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
        if not self.started:
            self.started = True
            self.new_direction = direction
        elif direction in (0, 1, 2, 3):
            if self.direction != (direction + 2) % 4:
                self.new_direction = direction

    def tick(self) -> None:
        if self.new_direction != self.direction:
            self.direction = self.new_direction
        if self.grow:
            self.length += 1
            self.grow -= 1
        else:
            self.snake.pop(-1)
        if self.direction == 0:
            new_position = (self.snake[0][0], self.snake[0][1] - 1)
        elif self.direction == 1:
            new_position = (self.snake[0][0] + 1, self.snake[0][1])
        elif self.direction == 2:
            new_position = (self.snake[0][0], self.snake[0][1] + 1)
        elif self.direction == 3:
            new_position = (self.snake[0][0] - 1, self.snake[0][1])
        if new_position[0] < 0 or new_position[1] < 0 or new_position[0] > self.game_dimensions[0] - 1 or new_position[1] > self.game_dimensions[1] - 1 or new_position in self.snake:
            self.stop()
        else:
            self.snake.insert(0, new_position)
        if self.apple in self.snake:
            self.points += 1
            self.grow += 1
            self.spawn_apple()
            print(self.points)

    def stop(self) -> None:
        '''quit game'''
        self.running = False