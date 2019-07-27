from __future__ import annotations
import random
from typing import Dict, Union, Optional
from players import Player
from trees import QuadTree, TwoDTree
    
class Game:

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have 
        won the game, or None if no player has won yet """
        raise NotImplementedError

class Tag(Game):
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _it: str
    _duration: int
    
    def __init__(self, n_players: int, 
                       field_type: Union[QuadTree, TwoDTree],
                       duration: int,
                       max_speed: int,
                       max_vision: int) -> None:
        pass

class ZombieTag(Game):
    _humans: Dict[str, Player]
    _zombies: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _duration: int

    def __init__(self, n_players: int, 
                       field_type: Union[QuadTree, TwoDTree],
                       duration: int,
                       max_speed: int,
                       max_vision: int) -> None:
        pass

class EliminationTag(Game):
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]   

    def __init__(self, n_players: int, 
                       field_type: Union[QuadTree, TwoDTree],
                       max_speed: int,
                       max_vision: int) -> None:
        pass

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['random', 'typing', 'players', 'trees']})

