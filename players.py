from __future__ import annotations
import random
from typing import List, Tuple, Optional, Set
from games import Game
from trees import OutOfBoundsError


class Player:
    """A Player playing in a game.

    === Private Attributes ===
    _name : the name of the player
    _location: 	a tuple of x-coordinates and y-coordinates holding the current
    location of the player on the field

    _colour: the colour used to draw the player object
    _vision: the distance a player can see in any direction
    _speed: the number of steps a player can move in a single turn
    _game: a reference to an instance of a Game class
    _points: the number of points the player has
    _targets: a list of player names that this player should move towards
    _enemies: a list of player names that this player should avoid
    _direction: a string indicating the direction the player is currently moving

    === Representation Invariants ===
    - The _location of a player must fall within the boundaries set by the
     _game.field attribute
    - _vision, _points and _speed must be positive or zero
    - the _colour attribute must be one of purple, green, or random
    - _points should be zero immediately after the class is initialized
    - no string that appears in _targets should also appear in _enemies
    - no string that appears in _enemies should also appear in _targets
    - _direction should be one of ('N', 'S', 'E', 'W')

    """
    _name: str
    _location: Tuple[int, int]
    _colour: str
    _vision: int
    _speed: int
    _game: Game
    _points: int
    _targets: List[str]
    _enemies: List[str]
    _direction: str

    def __init__(self, name: str, vision: int, speed: int, game: Game,
                 colour: str, location: Tuple[int, int]) -> None:
        """Initialize a new Player containing name, vision, speed game, colour
        and location. """
        self._name = name
        self._location = location
        self._colour = colour
        self._vision = vision
        self._speed = speed
        self._game = game
        self._points = 0
        self._targets = []
        self._enemies = []
        self._direction = ''

    def set_colour(self, colour: str) -> None:
        """ Change the colour of self
        """
        colour_lst = ['purple', 'green', 'random']
        if colour in colour_lst:
            self._colour = colour

    def increase_points(self, points: int) -> None:
        """ Increase <self>'s points by <points> """
        new_val = self._points + points
        if new_val >= 0:
            self._points = new_val

    def get_points(self) -> int:
        """ Return the number of points <self> currently has """
        return self._points

    def select_target(self, name: str) -> None:
        """ Add a target to <self>'s target list """
        if name not in self._targets and name not in self._enemies:
            self._targets.append(name)

    def ignore_target(self, name: str) -> None:
        """ Remove a target from <self>'s target list """
        if name in self._targets:
            self._targets.remove(name)

    def get_targets(self) -> List[str]:
        """ Return a copy of the list of target names """
        return self._targets.copy()

    def select_enemy(self, name: str) -> None:
        """ Add an enemy to <self>'s target list """
        if name not in self._targets and name not in self._enemies:
            self._enemies.append(name)

    def ignore_enemy(self, name: str) -> None:
        """ Remove an enemy from <self>'s enemy list """
        if name in self._enemies:
            self._enemies.remove(name)

    def get_enemies(self) -> List[str]:
        """ Return a copy of the list of enemy names """
        return self.get_enemies().copy()

    def reverse_direction(self) -> None:
        """ Update the direction so that <self> will move in the opposite
        direction """
        if self._direction == 'N':
            self._direction = 'S'
        elif self._direction == 'S':
            self._direction = 'N'
        elif self._direction == 'E':
            self._direction = 'W'
        else:
            self._direction = 'E'

    def set_speed(self, speed: int) -> None:
        """ Update <self>'s speed to <speed> """
        if speed >= 0:
            self._speed = speed

    def next_direction(self) -> Set[str]:
        """ Update the direction to move the next time self.move is called.

        This direction should be determined by the relative number of visible
        targets and enemies.

        Return a set of all equally good directions to move towards.

        This method should call the names_in_range Tree method exactly twice.

        This method should set self._direction to a subset of: ('N', 'S', 'E',
        'W')
        """
        direction_lst = random.shuffle(['NW', 'NE', 'SE', 'SW'])[:2]
        d_to_player_dict = {'N': [0], 'S': [0], 'E': [0], 'W': [0]}
        for direction in direction_lst:
<<<<<<< HEAD
            d_1 = direction[0]
            d_2 = direction[1]
            player_lst = self._game.field.names_in_range(self._points, direction
                                                         , self._vision)

=======
            d_dict[direction] = [[], []]
            player_lst = self._game.field.names_in_range(self._points, direction
                                                         , self._vision)
>>>>>>> 4b8cb44fcad4d4b1c12432fda94f0f24cbb3f37f
            for player in player_lst:
                if player in self._targets:
                    d_to_player_dict[d_1] += 1
                    d_to_player_dict[d_2] += 1
                elif player in self._enemies:
<<<<<<< HEAD
                    d_to_player_dict[_reverse(d_1)] += 1
                    d_to_player_dict[_reverse(d_2)] += 1

        max_val = 0
        max_lst = []
        for direction in d_to_player_dict:
            val = d_to_player_dict[direction]
            if val > max_val:
                max_val = val
                max_lst = [direction]
            elif val == max_val:
                max_lst.append(direction)
        self._direction = random.choice(max_lst)
        return set(max_lst)
=======
                    d_dict[direction][1].append(player)

        t_1 = len(d_dict[direction_lst[0]][0])
        e_1 = len(d_dict[direction_lst[0]][1])
        t_2 = len(d_dict[direction_lst[1]][0])
        e_2 = len(d_dict[direction_lst[1]][1])

        next_directions = list(set(_helper_next_direction(direction_lst, t_1,
                                                          e_1, t_2, e_2)))

        if len(next_directions) == 1:
            self._direction = next_directions[0]
        else:
            self._direction = random.choice(next_directions)
        return set(next_directions)
>>>>>>> 4b8cb44fcad4d4b1c12432fda94f0f24cbb3f37f

    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the
        number of steps described by self._speed. Make sure to keep track of the
        updated location of self.

        If the movement would move self out of bounds, move self in the opposite
        direction instead. self should continue to move in this new direction
        until next_direction is called again.
        """
        try:
            new_location = self._game.field.move(self._name, self._direction,
                                                 self._speed)
            if new_location is not None:
                self._location = new_location
        except OutOfBoundsError:
            self.reverse_direction()
<<<<<<< HEAD


def _reverse(direction: str)-> str:
    if direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'N'
    elif direction == 'E':
        return 'W'
    else:
        return 'E'
=======
            new_location = self._game.field.move(self._name, self._direction,
                                                 self._speed)
            if new_location is not None:
                self._location = new_location


def _helper_next_direction(direction_lst, t_1, e_1, t_2, e_2)-> List[str]:
    if (t_1 - e_1) == (t_2 - e_2):
        return [direction_lst[0][0], direction_lst[0][1],
                direction_lst[1][0], direction_lst[1][1]]
    elif (t_1 - e_1) > (t_2 - e_2):
        if direction_lst[0][0] == direction_lst[1][0]:
            return [direction_lst[0][1]]
        elif direction_lst[0][1] == direction_lst[1][1]:
            return [direction_lst[0][0]]
        else:
            return [direction_lst[0][0], direction_lst[0][1]]
    else:
        if direction_lst[0][0] == direction_lst[1][0]:
            return [direction_lst[1][1]]
        elif direction_lst[0][1] == direction_lst[1][1]:
            return [direction_lst[1][0]]
        else:
            return [direction_lst[1][0], direction_lst[1][1]]
>>>>>>> 4b8cb44fcad4d4b1c12432fda94f0f24cbb3f37f


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing']})
