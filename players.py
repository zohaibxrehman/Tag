"""CSC148 Assignment 2 - Players File

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains classes that describe players that play in one of the games.

As discussed in the handout, you may not change any of the public behaviour
(attributes, methods) given in the starter code, but you can definitely add
new attributes, functions, classes and methods to complete your work here.
"""

from __future__ import annotations
import random
from typing import List, Tuple, Optional, Set
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
    _game: 'Game'
    _points: int
    _targets: List[str]
    _enemies: List[str]
    _direction: str

    def __init__(self, name: str, vision: int, speed: int, game: 'Game',
                 colour: str, location: Tuple[int, int]) -> None:
        """Initialize a new Player containing name, vision, speed game, colour
        and location.

        >>> player = Player('4', 1, 1, 'Game', 'green', (67,89))
        """
        self._name = name
        self._location = location
        self._colour = colour
        self._vision = vision
        self._speed = speed
        self._game = game
        self._points = 0
        self._targets = []
        self._enemies = []
        self._direction = random.choice(['N', 'S', 'E', 'W'])

    def set_colour(self, colour: str) -> None:
        """ Change the colour of self

        >>> player = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player._colour
        'green'
        >>> player.set_colour('random')
        >>> player._colour
        'random'
        """
        colour_lst = ['purple', 'green', 'random']
        if colour in colour_lst:
            self._colour = colour

    def increase_points(self, points: int) -> None:
        """ Increase <self>'s points by <points>

        >>> player = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player.increase_points(1)
        >>> player._points
        1
        """
        new_val = self._points + points
        if new_val >= 0:
            self._points = new_val

    def get_points(self) -> int:
        """ Return the number of points <self> currently has

        >>> player = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player.increase_points(1)
        >>> player.get_points()
        1
        """
        return self._points

    def select_target(self, name: str) -> None:
        """ Add a target to <self>'s target list

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_target(player2._name)
        >>> player1._targets
        ['5']
        """
        if name not in self._targets and name not in self._enemies:
            self._targets.append(name)

    def ignore_target(self, name: str) -> None:
        """ Remove a target from <self>'s target list

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_target(player2._name)
        >>> player1._targets
        ['5']
        >>> player1.ignore_target(player2._name)
        >>> player1._targets
        []
        """
        if name in self._targets:
            self._targets.remove(name)

    def get_targets(self) -> List[str]:
        """ Return a copy of the list of target names

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_target(player2._name)
        >>> player1.get_targets()
        ['5']
        """
        return self._targets.copy()

    def select_enemy(self, name: str) -> None:
        """ Add an enemy to <self>'s target list

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_enemy(player2._name)
        >>> player1._enemies
        ['5']
        """
        if name not in self._targets and name not in self._enemies:
            self._enemies.append(name)

    def ignore_enemy(self, name: str) -> None:
        """ Remove an enemy from <self>'s enemy list

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_enemy(player2._name)
        >>> player1._enemies
        ['5']
        >>> player1.ignore_enemy(player2._name)
        >>> player1._enemies
        []
        """
        if name in self._enemies:
            self._enemies.remove(name)

    def get_enemies(self) -> List[str]:
        """ Return a copy of the list of enemy names

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (47,29))
        >>> player1.select_enemy(player2._name)
        >>> player1.get_enemies()
        ['5']
        """
        return self._enemies.copy()

    def reverse_direction(self) -> None:
        """ Update the direction so that <self> will move in the opposite
        direction

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> old_direction = player1._direction
        >>> player1.reverse_direction()
        >>> _reverse(old_direction) == player1._direction
        True
        """
        self._direction = _reverse(self._direction)

    def set_speed(self, speed: int) -> None:
        """ Update <self>'s speed to <speed>

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player1.set_speed(2)
        >>> player1._speed
        2
        """
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

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player2 = Player('5', 1, 1, 'Game', 'green', (40,29))
        >>> player3 = Player('6', 1, 1, 'Game', 'green', (63,29))
        >>> player4 = Player('7', 1, 1, 'Game', 'green', (27,79))
        >>> player = Player('1', 1, 1, 'Game', 'purple', (50,50))
        >>> player.select_target(player1._name)
        >>> player.select_target(player2._name)
        >>> player.select_target(player3._name)
        >>> player.select_target(player4._name)
        >>> player.next_direction() in {'N', 'S', 'W', 'E'}
        True
        """
        d_lst = ['NW', 'NE', 'SE', 'SW']
        random.shuffle(d_lst)
        direction_lst = d_lst[:2]
        d_to_player_dict = {'N': 0, 'S': 0, 'E': 0, 'W': 0}
        for direction in direction_lst:
            d_1 = direction[0]
            d_2 = direction[1]
            player_lst = self._game.field.names_in_range(self._location,
                                                         direction, self._vision
                                                         )

            for player in player_lst:
                if player in self._targets:
                    d_to_player_dict[d_1] += 1
                    d_to_player_dict[d_2] += 1
                elif player in self._enemies:
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

    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the
        number of steps described by self._speed. Make sure to keep track of the
        updated location of self.

        If the movement would move self out of bounds, move self in the opposite
        direction instead. self should continue to move in this new direction
        until next_direction is called again.

        >>> player1 = Player('4', 1, 1, 'Game', 'green', (67,89))
        >>> player1.move()
        >>> loc_lst = [(68,89), (67, 90), (66, 89), (67, 88), (67,89)]
        >>> player1._location in loc_lst
        True
        """
        try:
            self._location = self._game.field.move(self._name, self._direction,
                                                   self._speed)

        except OutOfBoundsError:
            self.reverse_direction()


def _reverse(direction: str)-> Optional[str]:
    """ Return a string of opposite direction to < direction >.

    >>> _reverse('N')
    'S'
    >>> _reverse('W')
    'E'
    """
    if direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'N'
    elif direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    else:
        return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={'extra-imports': ['typing', 'random', 'games', 'trees'],
                'disable': ['R0913', 'R0902', 'W0611', 'R1710', 'R1702']})
