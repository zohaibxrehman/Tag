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

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        self._players[player1].reverse_direction()
        self._players[player2].reverse_direction()
        if player1 == self._it:
            self._players[player2].increase_points(1)
            self._it = player2
        elif player2 == self._it:
            self._players[player1].increase_points(1)
            self._it = player1


    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet """
        winner_lst = []
        to_del_lst = []
        for player in self._players:
            if self._players[player].get_points() >= 1 and player != self._it:
                to_del_lst.append(player)
            else:
                winner_lst.append(player)
        for loser in to_del_lst:
            self.field.remove(self._players[loser])
            del self._players[loser]
        if len(winner_lst) >= 2 and self._it in winner_lst:
            winner_lst.remove(self._it)
        return winner_lst




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

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        self._players[player1].reverse_direction()
        self._players[player2].reverse_direction()
        if player1 in self._zombies and player2 in self._humans:
            self._zombies[player2] = self._humans[player2]
            self._zombies[player2].set_speed(1)
            del self._humans[player2]
        elif player2 in self._zombies and player1 in self._humans:
            self._zombies[player1] = self._humans[player1]
            self._zombies[player1].set_speed(1)
            del self._humans[player1]

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet """
        if len(self._humans) > 0:
            return 'humans'
        else:
            return 'zombie'

class EliminationTag(Game):
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]

    def __init__(self, n_players: int,
                       field_type: Union[QuadTree, TwoDTree],
                       max_speed: int,
                       max_vision: int) -> None:
        pass

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        if player1 in self._players[player2].get_enemies():
            self._players[player2].extend(self._players[player1].get_enemies())
            self._players[player2].ignore_enemy(player1)
            self._players[player2].increase_points(1)
        elif player2 in self._players[player1].get_enemies():
            self._players[player1].extend(self._players[player2].get_enemies())
            self._players[player1].ignore_enemy(player2)
            self._players[player1].increase_points(1)
        else:
            self._players[player1].reverse_direction()
            self._players[player2].reverse_direction()


    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet """
        max_lst = []
        max_val = 0
        for player in self._players:
            if self._players[player].get_points() == max_val:
                max_lst.append(player)
            elif self._players[player].get_points() > max_val:
                max_lst = [player]
                max_val = self._players[player].get_points()
            
        if len(max_lst) != 1:
            return None
        else:
            return max_lst[0]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['random', 'typing', 'players', 'trees']})

