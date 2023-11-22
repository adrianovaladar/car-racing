"""car racing game implementation"""
from enum import Enum
import random
import pygame


class GameStatus(Enum):
    """Enum for game status"""
    MENU = 1
    GAME = 2
    QUIT = 3
    GAME_OVER = 4
    PAUSE = 5


class OptionSelected(Enum):
    """Enum for option selected in menu"""
    START = 1
    QUIT = 2


white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 128, 0)
FONT = "Retro.ttf"
MOVE_STEP = 5

WIDTH = HEIGHT = 720


def text_format(message, text_font, text_size, text_color):
    """Format text for menu"""
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, 0, text_color)
    return new_text


def scroll_y(screen_surf, offset_y):
    """function to scroll the road"""
    width, height = screen_surf.get_size()
    copy_surf = screen_surf.copy()
    screen_surf.blit(copy_surf, (0, offset_y))
    if offset_y < 0:
        screen_surf.blit(copy_surf, (0, height + offset_y), (0, 0, width, -offset_y))
    else:
        screen_surf.blit(copy_surf, (0, 0), (0, height - offset_y, width, offset_y))


class Game:
    """Game class"""

    # pylint: disable=too-many-instance-attributes
    # The number of attributes is reasonable in this case.
    def __init__(self):
        self.background_scroll_offset = 0
        # pygame setup
        self.game_status = GameStatus.MENU
        pygame.init()
        pygame.display.set_caption('Car Racing Game')
        self.screen = pygame.display.set_mode((720, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load('images/road.jpg')
        self.car = pygame.image.load('images/car.png')
        self.car = pygame.transform.smoothscale(self.car, (100, 200))
        self.car_coordinates = [(self.screen.get_size()[0] / 2) - (self.car.get_size()[0] / 2),
                                self.screen.get_size()[1] - self.car.get_size()[1]]
        self.other_car = pygame.image.load('images/other_car.png')
        self.other_car = pygame.transform.smoothscale(self.other_car, (100, 200))
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
        self.option_selected = OptionSelected.START
        self.other_car_coordinates = [random.randrange(0, self.screen.get_size()[0]
                                                       - self.other_car.get_size()[0]), -300]

    def handle_pressed_keys(self, car, car_coordinates, screen):
        """function to handle pressed keys"""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and car_coordinates[0] - MOVE_STEP >= 0:
            car_coordinates[0] = car_coordinates[0] - MOVE_STEP
        if (pressed_keys[pygame.K_RIGHT]
                and car_coordinates[0] + MOVE_STEP <= screen.get_size()[0] - car.get_size()[0]):
            car_coordinates[0] = car_coordinates[0] + MOVE_STEP
        if pressed_keys[pygame.K_UP] and car_coordinates[1] - MOVE_STEP >= 0:
            car_coordinates[1] = car_coordinates[1] - MOVE_STEP
        if (pressed_keys[pygame.K_DOWN]
                and car_coordinates[1] + MOVE_STEP <= screen.get_size()[1] - car.get_size()[1]):
            car_coordinates[1] = car_coordinates[1] + MOVE_STEP
        if pressed_keys[pygame.K_p]:
            self.game_status = GameStatus.PAUSE

    def restart_game(self):
        """This function restarts the position of the cars
        in order to play again from the same position"""
        self.car_coordinates = [(self.screen.get_size()[0] / 2) - (self.car.get_size()[0] / 2),
                                self.screen.get_size()[1] - self.car.get_size()[1]]
        self.other_car_coordinates = [random.randrange(0, self.screen.get_size()[0]
                                                       - self.other_car.get_size()[0]), -300]

    def main_menu(self):
        """Main menu function"""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.option_selected != OptionSelected.START:
            self.option_selected = OptionSelected.START
        elif pressed_keys[pygame.K_DOWN] and self.option_selected != OptionSelected.QUIT:
            self.option_selected = OptionSelected.QUIT
        if pressed_keys[pygame.K_RETURN]:
            if self.option_selected == OptionSelected.START:
                self.game_status = GameStatus.GAME
            if self.option_selected == OptionSelected.QUIT:
                self.game_status = GameStatus.QUIT
        self.screen.fill(gray)
        # title = text_format('Car Racing Game', FONT, 90, orange)
        if self.option_selected == OptionSelected.START:
            text_start = text_format("START", FONT, 75, yellow)
        else:
            text_start = text_format("START", FONT, 75, black)
        if self.option_selected == OptionSelected.QUIT:
            text_quit = text_format("QUIT", FONT, 75, yellow)
        else:
            text_quit = text_format("QUIT", FONT, 75, black)

        # title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        self.screen.blit(text_start, (self.screen.get_size()[0] / 2 - (start_rect[2] / 2), 300))
        self.screen.blit(text_quit, (self.screen.get_size()[0] / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        # clock.tick(FPS)

    def screen_game_over(self):
        """Function to show the game over screen"""
        text_game_over = text_format("GAME OVER", FONT, 75, yellow)
        text_try_again = text_format("PRESS ANY KEY", FONT, 75, yellow)
        rect_game_over = text_game_over.get_rect()
        rect_try_again = text_try_again.get_rect()
        self.screen.blit(text_game_over, ((self.screen.get_size()[0] / 2) -
                                          (rect_game_over[2] / 2), 200))
        self.screen.blit(text_try_again, ((self.screen.get_size()[0] / 2) -
                                          (rect_try_again[2] / 2), 260))
        # self.screen.blit(self.screen_game_over, (0, 0))
        pygame.display.update()

    def is_game_over(self):
        """Logic for game over"""
        if (self.other_car_coordinates[0] <= self.car_coordinates[0] <=
                self.other_car.get_size()[0] + self.other_car_coordinates[0] and
                self.other_car_coordinates[1] <= self.car_coordinates[1]
                <= self.other_car.get_size()[1] + self.other_car_coordinates[1] or
                self.other_car_coordinates[0] <= self.car_coordinates[0] + self.car.get_size()[0] <=
                self.other_car.get_size()[0] + self.other_car_coordinates[0] and
                self.other_car_coordinates[1] <= self.car_coordinates[1] + self.car.get_size()[1]
                <= self.other_car.get_size()[1] + self.other_car_coordinates[1]):
            return True
        return False

    def screen_pause(self):
        """Function to show the pause screen"""
        text_pause = text_format("PAUSE", FONT, 75, yellow)
        text_resume = text_format("PRESS R TO RESUME", FONT, 75, yellow)
        rect_pause = text_pause.get_rect()
        rect_resume = text_resume.get_rect()
        self.screen.blit(text_pause, ((self.screen.get_size()[0] / 2) -
                                      (rect_pause[2] / 2), 200))
        self.screen.blit(text_resume, ((self.screen.get_size()[0] / 2) -
                                       (rect_resume[2] / 2), 260))
        pygame.display.update()

    def run_game(self):
        """Function for running the game"""
        # RENDER YOUR GAME HERE
        self.screen.blit(self.background, (0, 0))
        scroll_y(self.screen, self.background_scroll_offset)
        self.screen.blit(self.car, self.car_coordinates)
        self.screen.blit(self.other_car, self.other_car_coordinates)
        self.background_scroll_offset += 2
        if self.background_scroll_offset >= self.screen.get_size()[1]:
            self.background_scroll_offset = 0
        # flip() the display to put your work on screen
        pygame.display.flip()
        self.handle_pressed_keys(self.car, self.car_coordinates, self.screen)
        self.other_car_coordinates[1] += 2
        if self.other_car_coordinates[1] == 30 + self.screen.get_size()[1]:
            self.other_car_coordinates = [random.randrange(0, self.screen.get_size()[0]
                                                           - self.other_car.get_size()[0]), -200]

    def run(self):
        """game logic"""
        self.screen.fill("gray")
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # fill the screen with a color to wipe away anything from last frame
            if self.game_status == GameStatus.MENU:
                self.main_menu()
            elif self.game_status == GameStatus.GAME:
                self.run_game()
                if self.is_game_over():
                    self.game_status = GameStatus.GAME_OVER
            if self.game_status == GameStatus.PAUSE:
                self.screen_pause()
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_r]:
                    self.game_status = GameStatus.GAME
            if self.game_status == GameStatus.GAME_OVER:
                self.screen_game_over()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.game_status = GameStatus.MENU
                        self.restart_game()
            elif self.game_status == GameStatus.QUIT:
                self.running = False

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
