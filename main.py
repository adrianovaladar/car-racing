"""car racing game implementation"""
import pygame


def scroll_y(screen_surf, offset_y):
    """function to scroll the road"""
    width, height = screen_surf.get_size()
    copy_surf = screen_surf.copy()
    screen_surf.blit(copy_surf, (0, offset_y))
    if offset_y < 0:
        screen_surf.blit(copy_surf, (0, height + offset_y), (0, 0, width, -offset_y))
    else:
        screen_surf.blit(copy_surf, (0, 0), (0, height - offset_y, width, offset_y))


def handle_pressed_keys(car, car_coordinates, screen):
    """function to handle pressed keys"""
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT] and car_coordinates[0] - 5 >= 0:
        car_coordinates[0] = car_coordinates[0] - 5
    if pressed_keys[pygame.K_RIGHT] and car_coordinates[0] + 5 <= screen.get_size()[0] - car.get_size()[0]:
        car_coordinates[0] = car_coordinates[0] + 5
    if pressed_keys[pygame.K_UP] and car_coordinates[1] - 5 >= 0:
        car_coordinates[1] = car_coordinates[1] - 5
    if pressed_keys[pygame.K_DOWN] and car_coordinates[1] + 5 <= screen.get_size()[1] - car.get_size()[1]:
        car_coordinates[1] = car_coordinates[1] + 5


def game():
    """game logic"""
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((900, 720))
    clock = pygame.time.Clock()
    running = True
    background_scroll_offset = 0
    background = pygame.image.load('road.jpg')
    car = pygame.image.load('car.png')
    car = pygame.transform.smoothscale(car, (100, 200))
    car_coordinates = [(screen.get_size()[0] / 2) - (car.get_size()[0] / 2), screen.get_size()[1] - car.get_size()[1]]
    background = pygame.transform.smoothscale(background, screen.get_size())
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        handle_pressed_keys(car, car_coordinates, screen)
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

        # RENDER YOUR GAME HERE
        screen.blit(background, (0, 0))
        scroll_y(screen, background_scroll_offset)
        screen.blit(car, car_coordinates)
        background_scroll_offset += 2
        if background_scroll_offset >= screen.get_size()[1]:
            background_scroll_offset = 0
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    game()

