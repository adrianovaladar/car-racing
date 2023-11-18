"""tests for game implementation"""

from unittest.mock import MagicMock
from enum import Enum
import pygame
from main import Game, handle_pressed_keys, MOVE_STEP


pygame.K_RIGHT = 0
pygame.K_LEFT = 1
pygame.K_UP = 2
pygame.K_DOWN = 3


pygame.key.get_pressed = MagicMock(return_value=[0] * 10)


class Direction(Enum):
    """Enum for direction"""
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


def run_test_handle_pressed_keys(key, direction=Direction.NONE):
    """Main function for the tests of handle_pressed_keys"""
    test_game = Game()
    key_states = pygame.key.get_pressed()
    if direction == Direction.NONE:
        test_game.car_coordinates = [test_game.screen.get_size()[0] / 2,
                                     test_game.screen.get_size()[1] / 2]
    elif direction == Direction.UP:
        test_game.car_coordinates = [test_game.screen.get_size()[0] / 2, 0]
    elif direction == Direction.DOWN:
        test_game.car_coordinates = [test_game.screen.get_size()[0] / 2,
                                     test_game.screen.get_size()[1]]
    elif direction == Direction.LEFT:
        test_game.car_coordinates = [0, test_game.screen.get_size()[1] / 2]
    elif direction == Direction.RIGHT:
        test_game.car_coordinates = [test_game.screen.get_size()[0],
                                     test_game.screen.get_size()[1] / 2]
    key_states[key] = 1
    car_coordinates_before = list(test_game.car_coordinates)
    handle_pressed_keys(test_game.car, test_game.car_coordinates, test_game.screen)
    car_coordinates_after = test_game.car_coordinates
    if direction == Direction.NONE:
        if key == pygame.K_RIGHT:
            assert car_coordinates_before[0] + MOVE_STEP == car_coordinates_after[0]
        elif key == pygame.K_LEFT:
            assert car_coordinates_before[0] - MOVE_STEP == car_coordinates_after[0]
        if key == pygame.K_DOWN:
            assert car_coordinates_before[1] + MOVE_STEP == car_coordinates_after[1]
        elif key == pygame.K_UP:
            assert car_coordinates_before[1] - MOVE_STEP == car_coordinates_after[1]
    else:
        assert car_coordinates_before == car_coordinates_after
    key_states[key] = 0


def test_handle_pressed_keys_right():
    """Tests if the car moves right"""
    run_test_handle_pressed_keys(pygame.K_RIGHT)


def test_handle_pressed_keys_left():
    """Tests if the car moves left"""
    run_test_handle_pressed_keys(pygame.K_LEFT)


def test_handle_pressed_keys_up():
    """Tests if the car moves up"""
    run_test_handle_pressed_keys(pygame.K_UP)


def test_handle_pressed_keys_down():
    """Tests if the car moves down"""
    run_test_handle_pressed_keys(pygame.K_DOWN)


def test_handle_pressed_keys_right_limit():
    """Tests if the car does not move when it is in the right limit"""
    run_test_handle_pressed_keys(pygame.K_RIGHT, Direction.RIGHT)


def test_handle_pressed_keys_left_limit():
    """Tests if the car does not move when it is in the left limit"""
    run_test_handle_pressed_keys(pygame.K_LEFT, Direction.LEFT)


def test_handle_pressed_keys_up_limit():
    """Tests if the car does not move when it is in the upper limit"""
    run_test_handle_pressed_keys(pygame.K_UP, Direction.UP)


def test_handle_pressed_keys_down_limit():
    """Tests if the car does not move when it is in the lower limit"""
    run_test_handle_pressed_keys(pygame.K_DOWN, Direction.DOWN)


def test_is_game_over():
    """Test for the case of game over equals true"""
    test_game = Game()
    test_game.car_coordinates = [2, 2]
    test_game.other_car_coordinates = [2,2]
    assert test_game.is_game_over()


def test_is_not__game_over():
    """Test for the case of game over equals true"""
    test_game = Game()
    test_game.car_coordinates = [2,2]
    test_game.other_car_coordinates = [test_game.car.get_size()[0] + 100,
                                       test_game.car.get_size()[1] + 100]
    assert not test_game.is_game_over()
    