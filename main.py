import pygame


def scroll_y(screen_surf, offset_y):
    width, height = screen_surf.get_size()
    copy_surf = screen_surf.copy()
    screen_surf.blit(copy_surf, (0, offset_y))
    if offset_y < 0:
        screen_surf.blit(copy_surf, (0, height + offset_y), (0, 0, width, -offset_y))
    else:
        screen_surf.blit(copy_surf, (0, 0), (0, height - offset_y, width, offset_y))


def game():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((900, 720))
    clock = pygame.time.Clock()
    running = True
    y = 0
    background = pygame.image.load('road.jpg')
    car = pygame.image.load('car.png')
    car = pygame.transform.smoothscale(car, (100, 200))
    car_coordinates = [screen.get_size()[0] / 2, screen.get_size()[1] - car.get_size()[1]]
    background = pygame.transform.smoothscale(background, screen.get_size())
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_coordinates[0] = car_coordinates[0] - 20
                elif event.key == pygame.K_RIGHT:
                    car_coordinates[0] = car_coordinates[0] + 20
                elif event.key == pygame.K_UP:
                    car_coordinates[1] = car_coordinates[1] - 20
                elif event.key == pygame.K_DOWN:
                    car_coordinates[1] = car_coordinates[1] + 20

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

        # RENDER YOUR GAME HERE
        screen.blit(background, (0, 0))
        scroll_y(screen, y)
        screen.blit(car, car_coordinates)
        y += 2
        if y >= screen.get_size()[1]:
            y = 0
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
