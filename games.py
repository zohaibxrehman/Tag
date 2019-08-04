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

    def __init__(self, n_players: int, field_type: Union[QuadTree, TwoDTree],
                 duration: int, max_speed: int, max_vision: int) -> None:

        player_list = list(range(n_players))
        location_lst = []
        while len(location_lst) == 0 or any(location_lst.count(x) > 1 for x in location_lst):
            p = 0
            location_lst = []
            while p < n_players:
                if isinstance(field_type, QuadTree):
                    pass
                # location_lst.append( (random.randint(0, 2*getattr(self.field, _centre))
                #                       random.randint(0, 100)))
                else:
                    pass

        self._players = {}
        self.field = field_type
        self._it = str(random.choice(player_list))
        self._duration = duration
        create_it = Player(self._it, random.randint(0, max_vision),
                           random.randint(1, max_speed), self, 'purple',
                           location_lst[player_list.index(int(self._it))])
        self._players[self._it] = create_it
        self.field.insert(self._it, location_lst[player_list.index(int(self._it)
                                                                   )])

        for player in range(len(player_list)):
            player_name = str(player_list[player])
            if str(player) != self._it:
                create_player = Player(player_name,
                                       random.randint(0, max_vision),
                                       random.randint(1, max_speed), self,
                                       'green', location_lst[player])

                create_player.select_enemy(self._it)
                self._players[self._it].select_target(player_name)

                self._players[player_name] = create_player
                self.field.insert(player_name, location_lst[player])

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        self._players[player1].reverse_direction()
        self._players[player2].reverse_direction()
        if player1 == self._it:
            self._players[player2].increase_points(1)
            self._players[player2].ignore_enemy(player1)
            self._players[player1].ignore_target(player2)

            self._players[player1].select_enemy(player2)
            self._players[player2].select_target(player1)
            for player in self._players[player1].get_targets():
                self._players[player1].ignore_target(player)
                self._players[player2].select_target(player)

            self._it = player2
        elif player2 == self._it:
            self._players[player1].increase_points(1)
            self._players[player1].ignore_enemy(player2)
            self._players[player2].ignore_target(player1)

            self._players[player2].select_enemy(player1)
            self._players[player1].select_target(player2)
            for player in self._players[player2].get_targets():
                self._players[player2].ignore_target(player)
                self._players[player1].select_target(player)

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
            self.field.remove(loser)
            del self._players[loser]
        if isinstance(self.field, TwoDTree):
            self.field.balance()
        if len(winner_lst) >= 2 and self._it in winner_lst:
            winner_lst.remove(self._it)
        return winner_lst


class ZombieTag(Game):
    _humans: Dict[str, Player]
    _zombies: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _duration: int

    def __init__(self, n_players: int, field_type: Union[QuadTree, TwoDTree],
                 duration: int, max_speed: int, max_vision: int) -> None:

        player_list = list(range(n_players))
        location_lst = []
        while len(location_lst) == 0 or any(
                location_lst.count(x) > 1 for x in location_lst):
            p = 0
            location_lst = []
            while p < n_players + 1:
                if isinstance(field_type, QuadTree):
                    pass
                # location_lst.append( (random.randint(0, 2*getattr(self.field, _centre))
                #                       random.randint(0, 100)))
                else:
                    pass

        self._humans = {}
        self._zombies = {}
        self.field = field_type
        self._duration = duration

        zombie = Player('first zombie', max_vision, max_speed, self, 'purple',
                        location_lst[n_players])
        self._zombies['first zombie'] = zombie
        self.field.insert('first zombie', location_lst[n_players])

        for player in range(len(player_list)):
            player_name = player_list[player]
            create_player = Player(player_name, random.randint(0, max_vision),
                                   random.randint(0, max_speed), self, 'green',
                                   location_lst[player])

            create_player.select_enemy('first zombie')
            zombie.select_target(player_name)

            self._humans[player_name] = create_player
            self.field.insert(player_name, location_lst[player])

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """

        if player1 in self._humans and player2 in self._humans:
            self._humans[player1].reverse_direction()
            self._humans[player2].reverse_direction()
        elif player1 in self._zombies and player2 in self._humans:
            self._zombies[player1].reverse_direction()
            self._humans[player2].reverse_direction()

            self._zombies[player2] = self._humans[player2]
            self._zombies[player2].set_speed(1)
            self._humans.pop(player2)

            self._zombies[player2].ignore_enemy(player1)
            self._zombies[player1].ignore_target(player2)

            for target in self._zombies[player1].get_targets():
                self._zombies[player2].select_target(target)
        elif player2 in self._zombies and player1 in self._humans:
            self._humans[player1].reverse_direction()
            self._zombies[player2].reverse_direction()

            self._zombies[player1] = self._humans[player1]
            self._zombies[player1].set_speed(1)
            self._humans.pop(player1)

            self._zombies[player1].ignore_enemy(player2)
            self._zombies[player2].ignore_target(player1)

            for target in self._zombies[player2].get_targets():
                self._zombies[player1].select_target(target)
        else:
            self._zombies[player1].reverse_direction()
            self._zombies[player2].reverse_direction()

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

    def __init__(self, n_players: int, field_type: Union[QuadTree, TwoDTree],
                 max_speed: int, max_vision: int) -> None:

        player_list = list(range(n_players))
        location_lst = []
        while len(location_lst) == 0 or any(
                location_lst.count(x) > 1 for x in location_lst):
            p = 0
            location_lst = []
            while p < n_players:
                if isinstance(field_type, QuadTree):
                    pass
                # location_lst.append( (random.randint(0, 2*getattr(self.field, _centre))
                #                       random.randint(0, 100)))
                else:
                    pass

        self._players = {}
        self.field = field_type
        for p in range(len(player_list)):
            create_player = Player(str(player_list[p]), random.randint(0, max_vision),
                                   random.randint(1, max_speed), self, 'random',
                                   location_lst[p])
            if p == len(player_list) - 1:
                create_player.select_target(str(player_list[0]))
            else:
                create_player.select_target(str(player_list[p + 1]))

            if p == 0:
                create_player.select_enemy(str(player_list[len(player_list) -
                                                             1]))
            else:
                create_player.select_enemy(str(player_list[p - 1]))

            self._players[str(player_list[p])] = create_player
            self.field.insert(str(player_list[p]), location_lst[p])

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide """
        if player1 in self._players[player2].get_targets():
            self._players[player2].ignore_target(player1)
            for targets in self._players[player1].get_targets():
                self._players[player2].select_target(targets)
            del self._players[player1]
            self._players[player2].increase_points(1)
        elif player2 in self._players[player1].get_targets():
            self._players[player1].ignore_target(player2)
            for targets in self._players[player2].get_targets():
                self._players[player1].select_target(targets)
            del self._players[player2]
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

        if len(max_lst) == 1:
            return max_lst[0]
        else:
            return None


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['random', 'typing', 'players',
                                                  'trees']})

