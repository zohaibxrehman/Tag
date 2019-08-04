from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    """
    INSERT
    """
    pass


class Tree:
    """

    """

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str, distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


class QuadTree(Tree):
    """

    """
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize a new Tree instance

        Runtime: O(1)
        """
        self._centre = centre
        self._name = None
        self._point = None
        self._ne = None
        self._nw = None
        self._se = None
        self._sw = None

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._name == name
        else:
            return (self._ne is not None and self._ne.__contains__(name)) \
                   or (self._nw is not None and self._nw.__contains__(name)) \
                   or (self._se is not None and self._se.__contains__(name)) \
                   or (self._sw is not None and self._sw.__contains__(name))

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._point == point
        else:
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
                return self._nw.contains_point(point) \
                    if self._nw is not None else False
            elif point[0] <= self._centre[0]:  # SW
                return self._sw.contains_point(point) \
                    if self._sw is not None else False
            elif point[1] <= self._centre[1]:  # NE
                return self._ne.contains_point(point) \
                    if self._ne is not None else False
            else:  # SE
                return self._se.contains_point(point) \
                    if self._se is not None else False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        if not (point[0] <= 2 * self._centre[0] and point[1] <= 2 *
                self._centre[1]) or self.contains_point(point):
            raise OutOfBoundsError
        else:
            self._insert_helper(name, point)

    def _insert_helper(self, name, point):
        if self.is_empty():
            self._name = name
            self._point = point
        elif self.is_leaf():
            if self._find_region(self._point) == self._find_region(point):
                # copying
                demoted_tree = QuadTree(self._find_centre(self._point))
                demoted_tree._name = self._name
                demoted_tree._point = self._point

                # emptying
                self._name = None
                self._point = None
                demoted_tree._insert_helper(name, point)  # recursion

                # combine
                self._insert_region(demoted_tree)
            else:  # REGIONAL BASE CASE
                demoted_tree = QuadTree(self._find_centre(self._point))
                demoted_tree._name = self._name
                demoted_tree._point = self._point

                self._name = None
                self._point = None

                new_tree = QuadTree(self._find_centre(point))
                new_tree._name = name
                new_tree._point = point

                self._insert_region(demoted_tree)
                self._insert_region(new_tree)
        elif point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            if self._nw is None:
                self._nw = QuadTree(self._find_centre(point))
            self._nw._insert_helper(name, point)
        elif point[0] <= self._centre[0]:  # SW
            if self._sw is None:
                self._sw = QuadTree(self._find_centre(point))
            self._sw._insert_helper(name, point)
        elif point[1] <= self._centre[1]:  # NE
            if self._ne is None:
                self._ne = QuadTree(self._find_centre(point))
            self._ne._insert_helper(name, point)
        else:  # SE
            if self._se is None:
                self._se = QuadTree(self._find_centre(point))
            self._se._insert_helper(name, point)

    def _find_region(self, point: Tuple[int, int]) -> str:
        if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            return 'NW'
        elif point[0] <= self._centre[0]:  # SW
            return 'SW'
        elif point[1] <= self._centre[1]:  # NE
            return 'NE'
        else:  # SE
            return 'SE'

    def _insert_region(self, tree: QuadTree) -> None:
        if tree._point[0] <= self._centre[0] and tree._point[1] <= self._centre[1]:  # NW
            self._nw = tree
        elif tree._point[0] <= self._centre[0]:  # SW
            self._sw = tree
        elif tree._point[1] <= self._centre[1]:  # NE
            self._ne = tree
        else:  # SE
            self._se = tree

    def _find_centre(self, point) -> Tuple[int, int]:
        if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            return int(self._centre[0] - self._centre[0] / 2), \
                   int(self._centre[1] - self._centre[1] / 2)
        elif point[0] <= self._centre[0]:  # SW
            return int(self._centre[0] - self._centre[0] / 2), \
                   int(self._centre[1] + self._centre[1] / 2)
        elif point[1] <= self._centre[1]:  # NE
            return int(self._centre[0] + self._centre[0] / 2), \
                   int(self._centre[1] - self._centre[1] / 2)
        else:  # SE
            return int(self._centre[0] + self._centre[0] / 2), \
                   int(self._centre[1] + self._centre[1] / 2)

    def remove(self, name: str) -> None:
        """Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                self._name = None
                self._point = None
        elif self._nw is not None and self._nw.is_leaf() and \
                self._nw._name == name:
            self._nw = None
        elif self._ne is not None and self._ne.is_leaf() and \
                self._ne._name == name:
            self._ne = None
        elif self._sw is not None and self._sw.is_leaf() and \
                self._sw._name == name:
            self._sw = None
        elif self._se is not None and self._se.is_leaf() and \
                self._se._name == name:
            self._se = None
        elif self._nw is not None and name in self._nw:
            # REMOVE FROM NW -> IF NW EMPTY THEN RID OF IT
            #                -> IF ONLY ONE SUBTREE LEFT THEN CLEAN THEN PROMOTE
            #                -> MULTIPLE SUBTREES THEN LEAVE AS IS
            self._nw.remove(name)
            if self._nw.is_empty():
                self._nw = None
            else:
                subtrees = [self._nw._nw, self._nw._ne, self._nw._sw,
                            self._nw._se]
                while None in subtrees:
                    subtrees.remove(None)
                # PROMOTION
                if len(subtrees) == 1:
                    self._nw = subtrees[0]  # PUSHING IT UP
                    # DELETING FOR PROMOTION
                    self._nw._nw = None
                    self._nw._ne = None
                    self._nw._sw = None
                    self._nw._se = None
        elif self._ne is not None and name in self._ne:
            self._ne.remove(name)
            if self._ne.is_empty():
                self._ne = None
            else:
                subtrees = [self._ne._nw, self._ne._ne, self._ne._sw,
                            self._ne._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._ne = subtrees[0]
                    self._ne._nw = None
                    self._ne._ne = None
                    self._ne._sw = None
                    self._ne._se = None
        elif self._sw is not None and name in self._sw:
            self._sw.remove(name)
            if self._sw.is_empty():
                self._sw = None
            else:
                subtrees = [self._sw._nw, self._sw._ne, self._sw._sw,
                            self._sw._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._nw = subtrees[0]
                    self._sw._nw = None
                    self._sw._ne = None
                    self._sw._sw = None
                    self._sw._se = None
        elif self._se is not None and name in self._se:
            self._se.remove(name)
            if self._se.is_empty():
                self._se = None
            else:
                subtrees = [self._se._nw, self._se._ne, self._se._sw,
                            self._se._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._se = subtrees[0]
                    self._se._nw = None
                    self._se._ne = None
                    self._se._sw = None
                    self._se._se = None

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                self._name = None
                self._point = None
        elif self._nw is not None and self._nw.is_leaf() and \
                self._nw._point == point:
            self._nw = None
        elif self._ne is not None and self._ne.is_leaf() and \
                self._ne._point == point:
            self._ne = None
        elif self._sw is not None and self._sw.is_leaf() and \
                self._sw._point == point:
            self._sw = None
        elif self._se is not None and self._se.is_leaf() and \
                self._se._point == point:
            self._se = None
        elif point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            self._nw.remove_point(point)
            if self._nw.is_empty():
                self._nw = None
            else:
                subtrees = [self._nw._nw, self._nw._ne, self._nw._sw,
                            self._nw._se]
                while None in subtrees:
                    subtrees.remove(None)
                # PROMOTION
                if len(subtrees) == 1:
                    self._nw = subtrees[0]  # PUSHING IT UP
                    # DELETING FOR PROMOTION
                    self._nw._nw = None
                    self._nw._ne = None
                    self._nw._sw = None
                    self._nw._se = None
        elif point[0] <= self._centre[0]:  # SW
            self._sw.remove_point(point)
            if self._sw.is_empty():
                self._sw = None
            else:
                subtrees = [self._sw._nw, self._sw._ne, self._sw._sw,
                            self._sw._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._nw = subtrees[0]
                    self._sw._nw = None
                    self._sw._ne = None
                    self._sw._sw = None
                    self._sw._se = None
        elif point[1] <= self._centre[1]:  # NE
            self._ne.remove_point(point)
            if self._ne.is_empty():
                self._ne = None
            else:
                subtrees = [self._ne._nw, self._ne._ne, self._ne._sw,
                            self._ne._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._ne = subtrees[0]
                    self._ne._nw = None
                    self._ne._ne = None
                    self._ne._sw = None
                    self._ne._se = None
        elif point[1] > self._centre[1]:  # SE
            self._se.remove_point(point)
            if self._se.is_empty():
                self._se = None
            else:
                subtrees = [self._se._nw, self._se._ne, self._se._sw,
                            self._se._se]
                while None in subtrees:
                    subtrees.remove(None)
                if len(subtrees) == 1:
                    self._se = subtrees[0]
                    self._se._nw = None
                    self._se._ne = None
                    self._se._sw = None
                    self._se._se = None

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                new_point = _calc_point(self._point, direction, steps)
                if not (new_point[0] <= 2 * self._centre[0] and
                        new_point[1] <= 2 * self._centre[1]) \
                        or self.contains_point(new_point):
                    raise OutOfBoundsError
                else:
                    self._point = new_point
                    return self._point
        else:
            point = self._find_point(name)  # Proper None ?
            if point is not None:
                new_point = _calc_point(point, direction, steps)
                if not (new_point[0] <= 2 * self._centre[0] and
                        new_point[1] <= 2 * self._centre[1]) \
                        or self.contains_point(new_point):
                    raise OutOfBoundsError
                self.remove_point(point)
                self.insert(name, new_point)
            return point

    def _find_point(self, name):
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                return self._point
            else:
                return
        else:
            if self._nw is not None and name in self._nw:
                return self._nw._find_point(name)
            elif self._ne is not None and name in self._ne:
                return self._ne._find_point(name)
            elif self._sw is not None and name in self._sw:
                return self._sw._find_point(name)
            elif self._se is not None and name in self._se:
                return self._se._find_point(name)
            else:
                return

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                new_point = _calc_point(self._point, direction, steps)
                if (not (new_point[0] <= 2 * self._centre[0] and
                         new_point[1] <= 2 * self._centre[1])) or \
                        self.contains_point(new_point):
                    raise OutOfBoundsError
                else:
                    self._point = new_point
                    return self._point
        elif self.contains_point(point):
            new_point = _calc_point(point, direction, steps)
            if not (new_point[0] <= 2 * self._centre[0] and
                    new_point[1] <= 2 * self._centre[1]) \
                    or self.contains_point(new_point):
                raise OutOfBoundsError
            name = self._find_name(point)
            if name is not None:
                self.remove_point(point)
                self.insert(name, new_point)
                return new_point
            else:
                return

    def _find_name(self, point):
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                return self._name
            else:
                return
        else:
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
                return self._nw._find_name(point) # IF NONE ? NOT POSSIBLE ?
            elif point[0] <= self._centre[0]:  # SW
                return self._sw._find_name(point)
            elif point[1] <= self._centre[1]:  # NE
                return self._ne._find_name(point)
            elif point[1] > self._centre[1]:  # SE
                return self._se._find_name(point)
            else:
                return

    def names_in_range(self, point: Tuple[int, int], direction: str, distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        if self.is_empty():
            return []
        elif self.is_leaf():
            x_range, y_range = _find_xy_range(point, direction, distance)
            if ((min(x_range) <= self._point[0] <= max(x_range) and
                 min(y_range) <= self._point[1] <= max(y_range))):
                return [self._name]
            else:
                return []
        else:
            players = []
            x_range, y_range = _find_xy_range(point, direction, distance)

            nw = (min(x_range), min(y_range))
            ne = (max(x_range), min(y_range))
            sw = (min(x_range), max(y_range))
            se = (max(x_range), max(y_range))

            if self._nw is not None and \
                    nw[0] <= self._centre[0] and nw[1] <= self._centre[1]:  # NW
                players.extend(self._nw.names_in_range(point,
                                                       direction, distance))
            if self._sw is not None and \
                    sw[0] <= self._centre[0] and sw[1] > self._centre[1]:  # SW
                players.extend(self._sw.names_in_range(point,
                                                       direction, distance))
            if self._ne is not None and \
                    ne[0] > self._centre[0] and ne[1] <= self._centre[1]:  # NE
                players.extend(self._ne.names_in_range(point,
                                                       direction, distance))
            if self._se is not None and \
                    se[1] > self._centre[0] and se[1] > self._centre[1]:  # SE
                players.extend(self._se.names_in_range(point,
                                                       direction, distance))
            return players

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + (self._ne.size() if self._ne is not None else 0)\
                   + (self._nw.size() if self._nw is not None else 0)\
                   + (self._se.size() if self._se is not None else 0)\
                   + (self._sw.size() if self._sw is not None else 0)

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + max([self._ne.height() if self._ne is not None else 0,
                            self._nw.height() if self._nw is not None else 0,
                            self._se.height() if self._se is not None else 0,
                            self._sw.height() if self._se is not None else 0])

    def depth(self, tree: Tree) -> Optional[int]:
        """Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        #  ask about repetitive recursion. more runtime but same bound.
        if not isinstance(tree, QuadTree):
            return None
        elif self.is_empty() or self.is_leaf():
            return None
        elif tree is self:
            return None
        else:
            return self._depth_helper(tree)

    def _depth_helper(self, tree: QuadTree):
        if self.is_empty() or self.is_leaf():
            if tree is self:
                return 1
            else:
                return
        elif tree is self:
            return 1
        elif tree._centre[0] <= self._centre[0]:  # WEST
            if tree._centre[1] <= self._centre[1]:  # NW
                nw_depth = self._nw._depth_helper(
                    tree) if self._nw is not None else None
                depth = (1 + nw_depth) if nw_depth is not None else None
                return depth
            else:  # SW
                sw_depth = self._sw._depth_helper(
                    tree) if self._sw is not None else None
                depth = (1 + sw_depth) if sw_depth is not None else None
                return depth
        else:  # EAST
            if tree._centre[1] <= self._centre[1]:  # NE
                ne_depth = self._ne._depth_helper(
                    tree) if self._nw is not None else None
                depth = (1 + ne_depth) if ne_depth is not None else None
                return depth
            else:  # SE
                se_depth = self._se._depth_helper(
                    tree) if self._se is not None else None
                depth = (1 + se_depth) if se_depth is not None else None
                return depth

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        return (self._ne is None
                and self._nw is None
                and self._se is None
                and self._sw is None)
        #  use all. remove is none.

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        return self._name is None and self.is_empty()


def _calc_point(point, direction, steps) -> Tuple[int, int]:
    if direction == 'N':
        return point[0], point[1] - steps
    elif direction == 'S':
        return point[0], point[1] + steps
    elif direction == 'W':
        return point[0] - steps, point[1]
    else:
        return point[0] + steps, point[1]


def _find_xy_range(point, direction, distance):
    if direction == 'NW':
        final = point[0] - distance, point[1] - distance
    elif direction == 'NE':
        final = point[0] + distance, point[1] - distance
    elif direction == 'SW':
        final = point[0] - distance, point[1] + distance
    else:
        final = point[0] + distance, point[1] + distance
    return (point[0], final[0]), (point[1], final[1])


class TwoDTree(Tree):
    """

    """
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Optional[Tuple[int, int]]
    _se: Optional[Tuple[int, int]]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Optional[Tuple[int, int]] = None, se: Optional[Tuple[int, int]] = None) -> None:
        """Initialize a new Tree instance

        Runtime: O(1)
        """
        self._name = None
        self._point = None
        self._nw = nw
        self._se = se
        self._lt = None
        self._gt = None
        self._split_type = 'x'

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between the
        size of the _lt subtree and the size of the _gt subtree for all trees in
        <self>.
        """
        lt_size = self._lt.size() if self._lt is not None else 0
        gt_size = self._gt.size() if self._gt is not None else 0

        while not(abs(lt_size - gt_size) == 0 or abs(lt_size - gt_size) == 1):
            name = self._name
            point = self._point
            if lt_size > gt_size:
                self._remove_root_request('promote_left')
            else:
                self._remove_root_request('promote_right')
            self.insert(name, point)

            lt_size = self._lt.size() if self._lt is not None else 0
            gt_size = self._gt.size() if self._gt is not None else 0

    def _remove_root_request(self, request):
        if request == 'promote_left':
            replacement_info = self._lt._find_info('big_x')
            self.remove_point(replacement_info[1])
            self._name = replacement_info[0]
            self._point = replacement_info[1]
        else:
            replacement_info = self._gt._find_info('small_x')
            self.remove_point(replacement_info[1])
            self._name = replacement_info[0]
            self._point = replacement_info[1]

    # def _fix_values(self):
    #     if self.is_empty():
    #         pass
    #     elif self.is_leaf():
    #         pass
    #     else:
    #         if self._lt is not None:
    #             if self._split_type == 'x':  # LX
    #                 self._lt._split_type = 'y'
    #                 self._lt._nw = self._nw
    #                 self._lt._se = self._point[0], self._se[1]
    #             else:  # LU
    #                 self._split_type = 'x'
    #                 self._lt._nw = self._nw
    #                 self._lt._se = self._se[0], self._point[1]
    #             self._lt._fix_values()
    #         if self._gt is not None:
    #             if self._split_type == 'x':  # RX
    #                 self._lt._split_type = 'y'
    #                 self._lt._nw = self._point[0], self._nw[1]
    #                 self._lt._se = self._se
    #             else:  # LD
    #                 self._split_type = 'x'
    #                 self._lt._nw = self._nw[0], self._point[1]
    #                 self._lt._se = self._se
    #             self._gt._fix_values()

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._name == name
        else:
            return self._name == name \
                   or (self._lt is not None and self._lt.__contains__(name)) \
                   or (self._gt is not None and self._gt.__contains__(name))

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._point == point
        else:
            if self._point == point:
                return True
            elif (self._split_type == 'x' and point[0] <= self._point[0]) or \
                    (self._split_type == 'y' and point[1] <= self._point[1]):
                return self._lt.contains_point(point) \
                    if self._lt is not None else False
            else:
                return self._gt.contains_point(point) \
                    if self._gt is not None else False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        if not (self._nw[0] <= point[0] <= self._se[0] and
                self._nw[1] <= point[1] <= self._se[1]) or \
                self.contains_point(point):
            raise OutOfBoundsError
        else:
            self._insert_helper(name, point)

    def _insert_helper(self, name: str, point: Tuple[int, int]) -> None:
        if self.is_empty():
            self._name = name
            self._point = point
        elif self.is_leaf():  # LEAF BASE CASE
            self._insert_node_helper(name, point)
        else:
            if (self._split_type == 'x' and point[0] <= self._point[0]) or \
                    (self._split_type == 'y' and point[1] <= self._point[1]):
                if self._lt is not None:
                    self._lt._insert_helper(name, point)
                else:
                    self._insert_node_helper(name, point)  # HALF LEAF BASE CASE
            else:
                if self._gt is not None:
                    self._gt._insert_helper(name, point)
                else:
                    self._insert_node_helper(name, point)  # HALF LEAF BASE CASE

    def _insert_node_helper(self, name, point):
        if (self._split_type == 'x' and point[0] <= self._point[0]) or\
                (self._split_type == 'y' and point[1] <= self._point[1]):  # LX
            self._lt = TwoDTree()
            self._lt._name = name
            self._lt._point = point
        else:  # LD
            self._gt = TwoDTree()
            self._gt._name = name
            self._gt._point = point

    # self._nw, (self._point[0], self._se[1])
    # (self._point[0], self._nw[1]), self._se
    # self._nw, (self._se[0], self._point[1])
    # (self._nw[0], self._point[1]), self._se

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                self._name = None
                self._point = None
        elif self._name == name:
            self._remove_root()
        elif self._lt is not None and \
                self._lt.is_leaf() and self._lt._name == name:
            self._lt = None
        elif self._gt is not None and \
                self._gt.is_leaf() and self._gt._name == name:
            self._gt = None
        elif self._lt is not None and name in self._lt:
            self._lt.remove(name)
        elif self._gt is not None and name in self._gt:
            self._gt.remove(name)

    def _remove_root(self):
        if self._split_type == 'x':
            if self._lt is not None:
                replacement_info = self._lt._find_info('big_x')
                self.remove_point(replacement_info[1])
                self._name = replacement_info[0]
                self._point = replacement_info[1]
            else:
                replacement_info = self._gt._find_info('small_x')
                self.remove_point(replacement_info[1])
                self._name = replacement_info[0]
                self._point = replacement_info[1]
        else:
            if self._lt is not None:
                replacement_info = self._lt._find_info('big_y')
                self.remove_point(replacement_info[1])
                self._name = replacement_info[0]
                self._point = replacement_info[1]
            else:
                replacement_info = self._gt._find_info('small_y')
                self.remove_point(replacement_info[1])
                self._name = replacement_info[0]
                self._point = replacement_info[1]

    def _find_info(self, request: str) -> Tuple[str, Tuple[int, int]]:
        nodes = self._collect_all_nodes_info()
        if request == 'big_x':
            request_points = [node[1][0] for node in nodes]
            request_point = max(request_points)
        elif request == 'small_x':
            request_points = [node[1][0] for node in nodes]
            request_point = min(request_points)
        elif request == 'big_y':
            request_points = [node[1][1] for node in nodes]
            request_point = max(request_points)
        else:
            request_points = [node[1][1] for node in nodes]
            request_point = min(request_points)
        return nodes[request_points.index(request_point)]

    def _collect_all_nodes_info(self):
        if self.is_leaf():
            return [(self._name, self._point)]
        elif self._lt is not None and self._gt is not None:
            return [(self._name, self._point)] + \
                   self._lt._collect_all_nodes_info() + \
                   self._gt._collect_all_nodes_info()
        elif self._lt is not None:
            return [(self._name, self._point)] + \
                   self._lt._collect_all_nodes_info()
        elif self._gt is not None:
            return [(self._name, self._point)] + \
                   self._gt._collect_all_nodes_info()

    # def _remove_root(self):
    #     # if self.is_leaf():
    #     #     pass
    #     if self._lt is None and self._gt is not None:
    #         self._name, self._point, self._lt, self._gt = \
    #             self._gt._name, self._gt._point, self._gt._lt, self._gt._gt
    #     elif self._gt is None and self._lt is not None:
    #         self._name, self._point, self._lt, self._gt = \
    #             self._lt._name, self._lt._point, self._lt._lt, self._lt._gt
    #     else:
    #         promoted_tree_info = self._extract_max_info() # TRY ALL THE REMOVAL WORK HERE
    #         self.remove_point(promoted_tree_info[1]) # may fail silently if promotion took place in previous step
    #         # OR safer self.remove(promoted_tree_info[0])
    #         self._name, self._point = \
    #             promoted_tree_info[0], promoted_tree_info[1]

    # def _extract_max_info(self) -> tuple:
    #     # make return type more specific
    #     # [str, Tuple[int, int]]
    #     # issue: python thinks Optional[str] from type annotation
    #     if self._gt is not None:
    #         return self._gt._extract_max_info()
    #     else:
    #         info = self._name, self._point
    #         if self._lt is not None:
    #             self._name, self._point, self._lt, self._gt = \
    #                 self._lt._name, self._lt._point, self._lt._lt, self._lt._gt
    #         return info

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                self._name = None
                self._point = None
        else:
            if self._point == point:
                self._remove_root()  # O(n) !!!
            elif (self._split_type == 'x' and point[0] <= self._point[0]) or \
                    (self._split_type == 'y' and point[1] <= self._point[1]):
                if self._lt is not None and self._lt.is_leaf() and \
                        self._lt._point == point:
                    self._lt = None
                elif self._lt is not None:
                    self._lt.remove_point(point)
            else:
                if self._gt is not None and self._gt.is_leaf() and \
                        self._gt._point == point:
                    self._gt = None
                elif self._gt is not None:
                    self._gt.remove_point(point)

    def move(self, name: str, direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                new_point = _calc_point(self._point, direction, steps)
                if not (self._nw[0] <= new_point[0] <= self._se[0] and
                        self._nw[1] <= new_point[1] <= self._se[1]) or \
                        self.contains_point(new_point):
                    raise OutOfBoundsError
                else:
                    self._point = new_point
                    return self._point
        else:
            point = self._find_point(name)  # Proper None ?
            if point is not None:
                new_point = _calc_point(point, direction, steps)
                if not (self._nw[0] <= new_point[0] <= self._se[0] and
                        self._nw[1] <= new_point[1] <= self._se[1]) or \
                        self.contains_point(new_point):
                    raise OutOfBoundsError
                self.remove_point(point)
                self.insert(name, new_point)
            return point

    def _find_point(self, name):
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                return self._point
            else:
                return
        else:
            if self._name == name:
                return self._point
            elif self._lt is not None and name in self._lt:
                return self._lt._find_point(name)
            elif self._gt is not None and name in self._gt:
                return self._gt._find_point(name)
            else:
                return

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                new_point = _calc_point(self._point, direction, steps)
                if not (self._nw[0] <= new_point[0] <= self._se[0] and
                        self._nw[1] <= new_point[1] <= self._se[1]) or \
                        self.contains_point(new_point):
                    raise OutOfBoundsError
                else:
                    self._point = new_point
                    return self._point
        elif self.contains_point(point):
            new_point = _calc_point(point, direction, steps)
            if not (self._nw[0] <= new_point[0] <= self._se[0] and
                    self._nw[1] <= new_point[1] <= self._se[1]) or \
                    self.contains_point(new_point):
                raise OutOfBoundsError
            name = self._find_name(point)
            if name is not None:
                self.remove_point(point)
                self.insert(name, new_point)
                return new_point
            else:
                return

    def _find_name(self, point):
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                return self._name
            else:
                return
        elif self._point == point:
                return self._name
        elif (self._split_type == 'x' and point[0] <= self._point[0]) or \
                (self._split_type == 'y' and point[1] <= self._point[1]):
            return self._lt._find_name(point) \
                if self._lt is not None else None
        else:
            return self._gt._find_name(point) \
                if self._gt is not None else None

    def names_in_range(self, point: Tuple[int, int], direction: str, distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        if self.is_empty():
            return []
        elif self.is_leaf():
            x_range, y_range = _find_xy_range(point, direction, distance)
            if ((min(x_range) <= self._point[0] <= max(x_range) and
                 min(y_range) <= self._point[1] <= max(y_range))):
                return [self._name]
            else:
                return []
        else:
            players = []
            x_range, y_range = _find_xy_range(point, direction, distance)

            nw = (min(x_range), min(y_range))
            ne = (max(x_range), min(y_range))
            sw = (min(x_range), max(y_range))

            x_range, y_range = _find_xy_range(point, direction, distance)
            if ((min(x_range) <= self._point[0] <= max(x_range) and
                 min(y_range) <= self._point[1] <= max(y_range))):
                players.append(self._name)

            if self._split_type == 'x':
                if self._lt is not None and nw[0] <= self._point[0]:
                    players.extend(self._lt.names_in_range(point,
                                                           direction, distance))
                if self._gt is not None and ne[0] >= self._point[0]:
                    players.extend(self._gt.names_in_range(point,
                                                           direction, distance))
            else:
                if self._lt is not None and nw[1] <= self._point[1]:
                    players.extend(self._lt.names_in_range(point,
                                                           direction, distance))
                if self._gt is not None and sw[1] >= self._point[1]:
                    players.extend(self._gt.names_in_range(point,
                                                           direction, distance))
            return players

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + (self._lt.size() if self._lt is not None else 0) \
                   + (self._gt.size() if self._gt is not None else 0)

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + max([self._lt.height() if self._lt is not None else 0,
                            self._gt.height() if self._gt is not None else 0])

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        if not isinstance(tree, TwoDTree):
            return None
        elif self.is_empty() or self.is_leaf():
            return None
        elif tree is self:
            return None
        else:
            return self._depth_helper(tree)

    def _depth_helper(self, tree: TwoDTree):
        if self.is_empty() or self.is_leaf():
            if tree is self:
                return 1
            else:
                return
        elif tree is self:
            return 1
        elif (self._split_type == 'x' and tree._point[0] <= self._point[0]) or \
                (self._split_type == 'y' and tree._point[1] <= self._point[1]):
            lt_depth = self._lt._depth_helper(tree) \
                if self._lt is not None else None
            depth = (1 + lt_depth) if lt_depth is not None else None
            return depth
        else:
            gt_depth = self._gt._depth_helper(tree) \
                if self._gt is not None else None
            depth = (1 + gt_depth) if gt_depth is not None else None
            return depth

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        return self._lt is None and self._gt is None

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        return self._name is None and self.is_leaf()


if __name__ == '__main__':
    t = TwoDTree((0, 0), (200, 200))
    t.insert('a', (30, 100))
    t.insert('b', (150, 80))
    t.insert('c', (150, 20))
    t.insert('d', (20, 20))
    t.insert('e', (140, 100))


    # import python_ta
    # python_ta.check_all(config={'extra-imports': ['typing']})
