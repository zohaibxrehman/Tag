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
        pass

    def set_colour(self, colour: str) -> None:
        """ Change the colour of self """
        pass

    def increase_points(self, points: int) -> None:
        """ Increase <self>'s points by <points> """
        pass

    def get_points(self) -> int:
        """ Return the number of points <self> currently has """
        pass

    def select_target(self, name: str) -> None:
        """ Add a target to <self>'s target list """
        pass

    def ignore_target(self, name: str) -> None:
        """ Remove a target from <self>'s target list """
        pass

    def get_targets(self) -> List[str]:
        """ Return a copy of the list of target names """
        pass

    def select_enemy(self, name: str) -> None:
        """ Add an enemy to <self>'s target list """
        pass

    def ignore_enemy(self, name: str) -> None:
        """ Remove an enemy from <self>'s enemy list """
        pass

    def get_enemies(self) -> List[str]:
        """ Return a copy of the list of enemy names """
        pass

    def reverse_direction(self) -> None:
        """ Update the direction so that <self> will move in the opposite direction """
        pass

    def set_speed(self, speed: int) -> None:
        """ Update <self>'s speed to <speed> """
        pass

    def next_direction(self) -> Set[str]:
        """ Update the direction to move the next time self.move is called. This direction should be
        determined by the relative number of visible targets and enemies.

        Return a set of all equally good directions to move towards.

        This method should call the names_in_range Tree method exactly twice.

        This method should set self._direction to a subset of: ('N', 'S', 'E', 'W')
        """
        pass

    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the number of steps
        described by self._speed. Make sure to keep track of the updated location of self. 
        
        If the movement would move self out of bounds, move self in the opposite direction instead.
        self should continue to move in this new direction until next_direction is called again.
        """
        pass

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing']})
    