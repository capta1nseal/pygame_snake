from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame
from logic import Logic

class UI:
    def __init__(self, logic: Logic, window_size: tuple[int, int] = (800, 600)) -> None:
        pygame.init()

        self.logic = logic
        self.window_constants = {
            "window_size": window_size,
            "scaled_game_size": (0, 0),
            "inset_game_position": (0, 0)
        }
        self.colours = {
            "background": 0x000000,
            "grid_dark": 0x444444,
            "grid_light": 0x666666,
            "snake_head": 0x119911,
            "snake_tail": 0x22CC22,
            "apple": 0xF11919,
            "font": 0xFFFFFF
        }

        self.screen = pygame.display.set_mode(
            self.window_constants["window_size"],
            pygame.RESIZABLE)
        self.screen.fill(self.colours["background"])

        self.calculate_scaling()

        self.small_surface = pygame.Surface(self.logic.get_dimensions())
        self.pxgrid = pygame.PixelArray(self.small_surface)

        self.fullscreen = False

    def calculate_scaling(self) -> None:
        '''
        calculate constants required for drawing the game
        at the right scale in the right position in the window
        '''
        game_dimensions = self.logic.get_dimensions()
        window_size = self.window_constants["window_size"]
        if window_size[0] / game_dimensions[0] <= \
                window_size[1] / game_dimensions[1]:
            self.window_constants["scaled_game_size"] = (
                window_size[0],
                window_size[0] * game_dimensions[1] / game_dimensions[0])
        else:
            self.window_constants["scaled_game_size"] = (
                window_size[1] * game_dimensions[0] / game_dimensions[1],
                window_size[1])

        self.window_constants["inset_game_position"] = (
            window_size[0] / 2 - self.window_constants["scaled_game_size"][0] / 2,
            window_size[1] / 2 - self.window_constants["scaled_game_size"][1] / 2)

    def toggle_fullscreen(self) -> None:
        '''change between fullscreen and windowed display modes'''
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (640, 480), pygame.RESIZABLE)
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode(
                (0, 0), pygame.RESIZABLE | pygame.FULLSCREEN)
            self.fullscreen = True

        self.window_constants["window_size"] = self.screen.get_size()
        self.calculate_scaling()

        self.screen.fill(self.colours["background"])
        pygame.display.update()

    def handle_events(self) -> None:
        '''
        handle pygame events
        such as key presses, window resizing and clicks
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logic.stop()

            elif event.type == pygame.VIDEORESIZE:
                self.window_constants["window_size"] = event.size
                self.calculate_scaling()

                if self.fullscreen:
                    self.screen = pygame.display.set_mode(
                        self.window_constants["window_size"], pygame.RESIZABLE | pygame.FULLSCREEN)

                else:
                    self.screen = pygame.display.set_mode(
                        self.window_constants["window_size"], pygame.RESIZABLE)
                self.screen.fill(self.colours["background"])
                pygame.display.update()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.logic.stop()
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.logic.set_new_direction(0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.logic.set_new_direction(1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.logic.set_new_direction(2)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.logic.set_new_direction(3)

    def draw(self) -> None:
        '''draw game to pygame screen surface and display'''
        snake = self.logic.get_snake()
        apple = self.logic.get_apple()
        self.small_surface.fill(self.colours["grid_dark"])
        for x in range(0, self.logic.get_dimensions()[0]):
            for y in range(0, self.logic.get_dimensions()[1]):
                if (x, y) == apple:
                    self.pxgrid[x, y] = self.colours["apple"] #type: ignore
                elif (not (x, y) in snake) and ((x + y) % 2):
                    self.pxgrid[x, y] = self.colours["grid_light"] #type: ignore

        self.pxgrid[snake[0][0], snake[0][1]] = self.colours["snake_head"] #type: ignore
        for x, y in snake[1:]:
            self.pxgrid[x, y] = self.colours["snake_tail"] #type: ignore

        scaled_game_size = self.window_constants["scaled_game_size"]
        inset_game_position = self.window_constants["inset_game_position"]

        self.screen.blit(pygame.transform.scale(
            self.small_surface,
            (int(scaled_game_size[0]), int(scaled_game_size[1]))),
            (int(inset_game_position[0]), int(inset_game_position[1])))

        pygame.display.update()
