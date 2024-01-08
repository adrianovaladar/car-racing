"""tests for game implementation"""
import unittest
from unittest.mock import MagicMock
from enum import Enum
import pygame
from main import Game, MOVE_STEP, SCORE_INCREMENT, NUMBER_OTHER_CARS

pygame.K_RIGHT = 0
pygame.K_LEFT = 1
pygame.K_UP = 2
pygame.K_DOWN = 3
pygame.K_p = 4

pygame.key.get_pressed = MagicMock(return_value=[0] * 10)


class Direction(Enum):
    """Enum for direction"""
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class TestGame(unittest.TestCase):
    """Tests for the game implementation"""

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.test_game=Game()

    def run_test_handle_pressed_keys(self, key, direction=Direction.NONE):
        """Main function for the tests of handle_pressed_keys"""
        key_states = pygame.key.get_pressed()
        if direction == Direction.NONE:
            self.test_game.car_coordinates = [self.test_game.screen.get_size()[0] / 2,
                                              self.test_game.screen.get_size()[1] / 2]
        elif direction == Direction.UP:
            self.test_game.car_coordinates = [self.test_game.screen.get_size()[0] / 2, 0]
        elif direction == Direction.DOWN:
            self.test_game.car_coordinates = [self.test_game.screen.get_size()[0] / 2,
                                              self.test_game.screen.get_size()[1]]
        elif direction == Direction.LEFT:
            self.test_game.car_coordinates = [0, self.test_game.screen.get_size()[1] / 2]
        elif direction == Direction.RIGHT:
            self.test_game.car_coordinates = [self.test_game.screen.get_size()[0],
                                              self.test_game.screen.get_size()[1] / 2]
        key_states[key] = 1
        car_coordinates_before = list(self.test_game.car_coordinates)
        self.test_game.handle_pressed_keys(self.test_game.car, self.test_game.car_coordinates,
                                           self.test_game.screen)
        car_coordinates_after = self.test_game.car_coordinates
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

    def test_handle_pressed_keys_right(self):
        """Tests if the car moves right"""
        self.run_test_handle_pressed_keys(pygame.K_RIGHT)

    def test_handle_pressed_keys_left(self):
        """Tests if the car moves left"""
        self.run_test_handle_pressed_keys(pygame.K_LEFT)

    def test_handle_pressed_keys_up(self):
        """Tests if the car moves up"""
        self.run_test_handle_pressed_keys(pygame.K_UP)

    def test_handle_pressed_keys_down(self):
        """Tests if the car moves down"""
        self.run_test_handle_pressed_keys(pygame.K_DOWN)

    def test_handle_pressed_keys_right_limit(self):
        """Tests if the car does not move when it is in the right limit"""
        self.run_test_handle_pressed_keys(pygame.K_RIGHT, Direction.RIGHT)

    def test_handle_pressed_keys_left_limit(self):
        """Tests if the car does not move when it is in the left limit"""
        self.run_test_handle_pressed_keys(pygame.K_LEFT, Direction.LEFT)

    def test_handle_pressed_keys_up_limit(self):
        """Tests if the car does not move when it is in the upper limit"""
        self.run_test_handle_pressed_keys(pygame.K_UP, Direction.UP)

    def test_handle_pressed_keys_down_limit(self):
        """Tests if the car does not move when it is in the lower limit"""
        self.run_test_handle_pressed_keys(pygame.K_DOWN, Direction.DOWN)

    def test_is_game_over(self):
        """Test for the case of game over equals true"""
        self.test_game.car_coordinates = [2, 2]
        other_car_coordinates = [2, 2]
        self.test_game.other_cars_coordinates[0] = other_car_coordinates

        assert self.test_game.is_game_over()

    def test_is_not__game_over(self):
        """Test for the case of game over equals true"""
        self.test_game.car_coordinates = [2, 2]
        other_car_coordinates = [self.test_game.car.get_size()[0] + 100,
                                 self.test_game.car.get_size()[1] + 100]
        self.test_game.other_cars_coordinates[0] = other_car_coordinates
        for index in range(1, NUMBER_OTHER_CARS):
            self.test_game.other_cars_coordinates[index] = [-100, -100]
        assert not self.test_game.is_game_over()

    def test_increase_speed(self):
        """Test if the speed increases when the score is equal to SCORE_INCREMENT"""
        fps_before = self.test_game.fps
        self.test_game.score = SCORE_INCREMENT
        self.test_game.update_fps()
        fps_after = self.test_game.fps
        assert fps_after > fps_before

    def test_increase_speed_below_score_increment(self):
        """Test if the speed increases when the score is equal to SCORE_INCREMENT - 1"""
        fps_before = self.test_game.fps
        self.test_game.score = SCORE_INCREMENT - 1
        self.test_game.update_fps()
        fps_after = self.test_game.fps
        assert fps_after == fps_before

    def test_is_position_not_valid_car(self):
        """Test if the position is valid when it is equal to the main car position"""
        self.test_game.other_cars_coordinates[0] = self.test_game.car_coordinates
        assert not self.test_game.is_position_valid(self.test_game.other_cars_coordinates[0])

    def test_is_position_not_valid_other_car(self):
        """Test if the position is valid when it is equal to other car position"""
        self.test_game.other_cars_coordinates[0] = self.test_game.other_cars_coordinates[1]
        assert not self.test_game.is_position_valid(self.test_game.other_cars_coordinates[0])
