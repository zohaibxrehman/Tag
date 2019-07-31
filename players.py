from __future__ import annotations
from typing import List, Tuple, Optional, Set

class Player:
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
        """ Change the colour of self """
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
        """ Update the direction so that <self> will move in the opposite direction """
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
        """ Update the direction to move the next time self.move is called. This direction should be
        determined by the relative number of visible targets and enemies.

        Return a set of all equally good directions to move towards.

        This method should call the names_in_range Tree method exactly twice.

        This method should set self._direction to a subset of: ('N', 'S', 'E', 'W')
        """
        d_dict = {}
        direction_lst = self._game.random.shuffle(['NW', 'NE', 'SE', 'SW'])[:2]
        for direction in direction_lst:
            d_dict[direction] = [[], []]
            player_lst = self._game.field.names_in_range(self._points, direction,
                                                         self._vision)
            for player in player_lst:
                if player in self._targets:
                    d_dict[direction][0].append(player)
                elif player in self._enemies:
                    d_dict[direction][1].append(player)

        t_1 = len(d_dict[direction_lst[0]][0])
        e_1 = len(d_dict[direction_lst[0]][1])
        t_2 = len(d_dict[direction_lst[0]][0])
        e_2 = len(d_dict[direction_lst[0]][1])

        return self._helper_next_direction(direction_lst, t_1, e_1, t_2, e_2)


    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the number of steps
        described by self._speed. Make sure to keep track of the updated location of self.

        If the movement would move self out of bounds, move self in the opposite direction instead.
        self should continue to move in this new direction until next_direction is called again.
        """
        try:
            self._game.field.move(self._name, self._direction, self._speed)
        except Exception:
            self.reverse_direction()
            self._game.field.move(self._name, self._direction, self._speed)


def _helper_next_direction(direction_lst, t_1, e_1, t_2, e_2)-> Set[str]:

    if (t_1 - e_1) == (t_2 - e_2):
        sample_lst = [direction_lst[0][0], direction_lst[0][1],
                      direction_lst[1][0], direction_lst[1][1]]
        return set(sample_lst)
    elif (t_1 - e_1) > (t_2 - e_2):
        if direction_lst[0][0] == direction_lst[1][0]:
            return set(direction_lst[0][1])
        elif direction_lst[0][1] == direction_lst[1][1]:
            return set(direction_lst[0][0])
        else:
            sample_lst = direction_lst[0][0], direction_lst[0][1]
            return set(sample_lst)
    else:
        if direction_lst[0][0] == direction_lst[1][0]:
            return set(direction_lst[1][1])
        elif direction_lst[0][1] == direction_lst[1][1]:
            return set(direction_lst[1][0])
        else:
            sample_lst = direction_lst[1][0], direction_lst[1][1]
            return set(sample_lst)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing']})
