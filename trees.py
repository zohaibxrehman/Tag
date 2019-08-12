"""CSC148 Assignment 2 - Tag You’re It!
=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto
=== Module Description ===
This <trees.py> file contains the Tree abstract class and two concrete
implementations of this abstract class. The two implementations are QuadTree and
TwoDTree which is a kd-tree of dimension 2.
"""

from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    """
    OutOfBoundsError exception raised when the a point is not in bounds of the
    Tree or if the node is being inserted at a coordinate where another node
    already exists.
    """
    pass


class Tree:
    """
    An abstract Tree class.
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

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

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

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at:
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

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the
        location of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


class QuadTree(Tree):
    """
    A QuadTree. Concrete implementation of Tree.

    === Private Attributes ===
    _centre: centre of the tree
    _name: name of the tree
    _point: point of the tree
    _ne: the north-east subtree of the tree
    _nw: the north-west subtree of the tree
    _se: the south-east subtree of the tree
    _sw: the south-west subtree of the tree

    === Representation Invariant ===
    - only leaf nodes can have a non-None _name attribute
    - every leaf node must have a non-None _name attribute unless it also has no
     parents
    - only leaf nodes can have a non-None _point attribute
    - every leaf node must have a non-None _point attribute unless it also has
    no parents
    - every non-None _point attribute must contain only positive integers or
    zero
    - every _centre attribute must contain only positive integers or zero
    - every _centre attribute describes a point that is the exact centre of the
     rectangle (if the exact centre is not an integer, the values in _centre
     should be rounded down to the nearest integer).
    - if _point is not None, then _point[0] <= 2*_centre[0] for the root node
    - if _point is not None, then _point[1] <= 2*_centre[1] for the root node
    - if d._point is not None for some descendant d of p, then:
    - d must be in the _nw or _sw subtrees if d._point[0] <= p._centre[0] and in
     one of the other subtrees otherwise.
    - d must be in the _nw or _ne subtrees if d._point[1] <= p._centre[1] and in
     one of the other subtrees otherwise.
    """
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize a new Tree instance with centre <centre>.

        Runtime: O(1)

        >>> q1 = QuadTree((50, 50))
        >>> q2 = QuadTree((100, 100))
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

        >>> q = QuadTree((50, 50))
        >>> q._name = 'a'
        >>> q._point = (25, 25)
        >>> 'a' in q
        True
        >>> q.__contains__('b')
        False
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

        >>> q = QuadTree((50, 50))
        >>> q._name = 'a'
        >>> q._point = (25, 25)
        >>> q.contains_point((25, 25))
        True
        >>> q.contains_point((50, 50))
        False
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._point == point
        else:
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:
                # NW
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

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Runtime: O(log(n))

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> 'a' in q
        True
        >>> q.insert('b', (75, 75))
        >>> 'b' in q
        True
        """
        if not (point[0] <= 2 * self._centre[0] and point[1] <= 2 *
                self._centre[1]) or self.contains_point(point):
            raise OutOfBoundsError
        else:
            self._insert_helper(name, point, {'NW': (0, 0),
                                              'NE': (2 * self._centre[0], 0),
                                              'SW': (0, 2 * self._centre[1]),
                                              'SE': (2 * self._centre[0],
                                                     2 * self._centre[1])})

    def _insert_helper(self, name: str, point: Tuple[int, int],
                       corners: Dict[str, Tuple[int, int]]) -> None:
        """
        Helper method for insert using the parameters <name> and <point>
        """
        if self.is_empty():
            self._name = name
            self._point = point
        elif self.is_leaf():
            if self._find_region(self._point) == self._find_region(point):
                # copying
                demoted_tree = QuadTree(self._find_centre(self._point, corners))
                demoted_tree._name = self._name
                demoted_tree._point = self._point

                # combine
                self._insert_region(demoted_tree)
                # emptying
                self._name = None
                self._point = None
                self._corner_helper(self._find_region(point), corners)
                demoted_tree._insert_helper(name, point, corners)  # recursion
            else:  # REGIONAL BASE CASE
                demoted_tree = QuadTree(self._find_centre(self._point, corners))
                demoted_tree._name = self._name
                demoted_tree._point = self._point

                self._name = None
                self._point = None

                new_tree = QuadTree(self._find_centre(point, corners))
                new_tree._name = name
                new_tree._point = point

                self._insert_region(demoted_tree)
                self._insert_region(new_tree)
        elif point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            if self._nw is None:
                self._nw = QuadTree(self._find_centre(point, corners))
            self._corner_helper('NW', corners)
            self._nw._insert_helper(name, point, corners)
        elif point[0] <= self._centre[0]:  # SW
            if self._sw is None:
                self._sw = QuadTree(self._find_centre(point, corners))
            self._corner_helper('SW', corners)
            self._sw._insert_helper(name, point, corners)
        elif point[1] <= self._centre[1]:  # NE
            if self._ne is None:
                self._ne = QuadTree(self._find_centre(point, corners))
            self._corner_helper('NE', corners)
            self._ne._insert_helper(name, point, corners)
        else:  # SE
            if self._se is None:
                self._se = QuadTree(self._find_centre(point, corners))
            self._corner_helper('SE', corners)
            self._se._insert_helper(name, point, corners)

    def _corner_helper(self, direction: str,
                       corners: Dict[str, Tuple[int, int]]) -> None:
        if direction == 'NW':  # NW
            corners['NE'] = int((corners['NW'][0] + corners['NE'][0]) / 2), int(
                (corners['NW'][1] + corners['NE'][1]) / 2)
            corners['SW'] = int((corners['SW'][0] + corners['NW'][0]) / 2), int(
                (corners['SW'][1] + corners['NW'][1]) / 2)
            corners['SE'] = self._centre
        elif direction == 'SW':  # SW
            corners['NE'] = self._centre
            corners['NW'] = int((corners['SW'][0] + corners['NW'][0]) / 2), int(
                (corners['SW'][1] + corners['NW'][1]) / 2)
            corners['SE'] = int((corners['SW'][0] + corners['SE'][0]) / 2), int(
                (corners['SW'][1] + corners['SE'][1]) / 2)
        elif direction == 'NE':  # NE
            corners['SW'] = self._centre
            corners['NW'] = int((corners['NE'][0] + corners['NW'][0]) / 2), int(
                (corners['NE'][1] + corners['NW'][1]) / 2)
            corners['SE'] = int((corners['SE'][0] + corners['NE'][0]) / 2), int(
                (corners['SE'][1] + corners['NE'][1]) / 2)
        else:  # SE
            corners['NW'] = self._centre
            corners['NE'] = int((corners['SE'][0] + corners['NE'][0]) / 2), int(
                (corners['SE'][1] + corners['NE'][1]) / 2)
            corners['SW'] = int((corners['SW'][0] + corners['SE'][0]) / 2), int(
                (corners['SE'][1] + corners['SW'][1]) / 2)

    def _find_region(self, point: Tuple[int, int]) -> str:
        """
        Return region of <point>.
        """
        if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            return 'NW'
        elif point[0] <= self._centre[0]:  # SW
            return 'SW'
        elif point[1] <= self._centre[1]:  # NE
            return 'NE'
        else:  # SE
            return 'SE'

    def _insert_region(self, tree: QuadTree) -> None:
        """
        Insert <tree> in its respective region.
        """
        if tree._point[0] <= self._centre[0] and \
                tree._point[1] <= self._centre[1]:  # NW
            self._nw = tree
        elif tree._point[0] <= self._centre[0]:  # SW
            self._sw = tree
        elif tree._point[1] <= self._centre[1]:  # NE
            self._ne = tree
        else:  # SE
            self._se = tree

    def _find_centre(self, point: Tuple[int, int],
                     corners: Dict[str, Tuple[int, int]]) -> Tuple[int, int]:
        """
        Return the centre of <point> with respect to self's centre.
        """
        if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            return int((corners['NW'][0] + self._centre[0]) / 2),\
                   int((corners['NW'][1] + self._centre[1]) / 2)
        elif point[0] <= self._centre[0]:  # SW
            return int((corners['SW'][0] + self._centre[0]) / 2), \
                   int((corners['SW'][1] + self._centre[1]) / 2)
        elif point[1] <= self._centre[1]:  # NE
            return int((corners['NE'][0] + self._centre[0]) / 2), \
                   int((corners['NE'][1] + self._centre[1]) / 2)
        else:  # SE
            return int((corners['SE'][0] + self._centre[0]) / 2), \
                   int((corners['SE'][1] + self._centre[1]) / 2)

    def remove(self, name: str) -> None:
        """Remove information about a player named <name> from this tree.

        Runtime: O(n)

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.remove('a')
        >>> 'a' in q
        False
        >>> 'b' in q
        True
        >>> q.remove('b')
        >>> 'b' in q
        False
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
            self._remove_promoter()
        elif self._ne is not None and self._ne.is_leaf() and \
                self._ne._name == name:
            self._ne = None
            self._remove_promoter()
        elif self._sw is not None and self._sw.is_leaf() and \
                self._sw._name == name:
            self._sw = None
            self._remove_promoter()
        elif self._se is not None and self._se.is_leaf() and \
                self._se._name == name:
            self._se = None
            self._remove_promoter()
        else:
            self._remove_helper(name)
            if self.is_empty():
                pass
            else:
                self._remove_promoter()

    def _remove_helper(self, name: str) -> None:
        """
        Helper method for remove with parameter name.
        """
        if self._nw is not None and name in self._nw:
            self._nw.remove(name)
            if self._nw.is_empty():
                self._nw = None
            else:
                self._nw._remove_promoter()
        elif self._ne is not None and name in self._ne:
            self._ne.remove(name)
            if self._ne.is_empty():
                self._ne = None
            else:
                self._ne._remove_promoter()
        elif self._sw is not None and name in self._sw:
            self._sw.remove(name)
            if self._sw.is_empty():
                self._sw = None
            else:
                self._sw._remove_promoter()
        elif self._se is not None and name in self._se:
            self._se.remove(name)
            if self._se.is_empty():
                self._se = None
            else:
                self._se._remove_promoter()

    def _remove_promoter(self) -> None:
        """
        Helper method for promoting when removing from a tree with single
        subtree.
        """
        subtrees = [self._nw, self._ne, self._sw, self._se]
        while None in subtrees:
            subtrees.remove(None)
        if len(subtrees) == 1 and subtrees[0].is_leaf():
            self._name = subtrees[0]._name
            self._point = subtrees[0]._point
            self._nw = None
            self._ne = None
            self._sw = None
            self._se = None

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.remove_point((25, 25))
        >>> q.contains_point((25, 25))
        False
        >>> q.remove_point((75, 75))
        >>> q.contains_point((75, 75))
        False
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
            self._remove_promoter()
        elif self._ne is not None and self._ne.is_leaf() and \
                self._ne._point == point:
            self._ne = None
            self._remove_promoter()
        elif self._sw is not None and self._sw.is_leaf() and \
                self._sw._point == point:
            self._sw = None
            self._remove_promoter()
        elif self._se is not None and self._se.is_leaf() and \
                self._se._point == point:
            self._se = None
            self._remove_promoter()
        else:
            self._remove_point_helper(point)
            if self.is_empty():
                pass
            else:
                self._remove_promoter()

    def _remove_point_helper(self, point: Tuple[int, int]) -> None:
        """
        Helper method for remove_point with parameter point.
        """
        if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
            self._nw.remove_point(point)
            if self._nw.is_empty():
                self._nw = None
            else:
                self._nw._remove_promoter()
        elif point[0] <= self._centre[0]:  # SW
            self._sw.remove_point(point)
            if self._sw.is_empty():
                self._sw = None
            else:
                self._sw._remove_promoter()
        elif point[1] <= self._centre[1]:  # NE
            self._ne.remove_point(point)
            if self._ne.is_empty():
                self._ne = None
            else:
                self._ne._remove_promoter()
        elif point[1] > self._centre[1]:  # SE
            self._se.remove_point(point)
            if self._se.is_empty():
                self._se = None
            else:
                self._se._remove_promoter()

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.move('a', 'S', 10)
        (25, 35)
        >>> q.contains_point((25, 35))
        True
        >>> q.contains_point((25, 25))
        False
        """
        if self.is_empty():
            return None
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
            return None
        else:
            point = self._find_point(name)
            if point is not None:
                new_point = _calc_point(point, direction, steps)
                if not (new_point[0] <= 2 * self._centre[0] and
                        new_point[1] <= 2 * self._centre[1]) \
                        or self.contains_point(new_point):
                    raise OutOfBoundsError
                self.remove_point(point)
                self.insert(name, new_point)
                return new_point
            return None

    def _find_point(self, name: str) -> Optional[Tuple[int, int]]:
        """
        Return the coordinates of the <name> in self.
        """
        if self.is_empty():
            return None
        elif self.is_leaf():
            if self._name == name:
                return self._point
            else:
                return None
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
                return None

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.move('a', 'S', 10)
        (25, 35)
        >>> q.contains_point((25, 35))
        True
        >>> q.contains_point((25, 25))
        False
        """
        if self.is_empty():
            return None
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
            return None
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
                return None
        else:
            return None

    def _find_name(self, point: Tuple[int, int]) -> Optional[str]:
        """
        Return the point at <point>.
        """
        if self.is_empty():
            return None
        elif self.is_leaf():
            if self._point == point:
                return self._name
            else:
                return None
        else:
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:
                # NW
                return self._nw._find_name(point)
            elif point[0] <= self._centre[0]:  # SW
                return self._sw._find_name(point)
            elif point[1] <= self._centre[1]:  # NE
                return self._ne._find_name(point)
            elif point[1] > self._centre[1]:  # SE
                return self._se._find_name(point)
            else:
                return None

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.names_in_range((40, 40), 'NW', 20)
        ['a']
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

        >>> q = QuadTree((50, 50))
        >>> q.size()
        1
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.size()
        3
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

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)

        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> q.insert('b', (75, 75))
        >>> q.height()
        2
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + max([self._ne.height() if self._ne is not None else 0,
                            self._nw.height() if self._nw is not None else 0,
                            self._se.height() if self._se is not None else 0,
                            self._sw.height() if self._sw is not None else 0])

    def depth(self, tree: Tree) -> Optional[int]:
        """Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        >>> q = QuadTree((50, 50))
        >>> q.insert('a', (25, 25))
        >>> b = QuadTree((75, 75))
        >>> b._name = 'b'
        >>> b._point = (75, 75)
        >>> q._se = b
        >>> q.depth(b)
        1
        >>> q.depth(q)
        """
        if not isinstance(tree, QuadTree):
            return None
        elif self.is_empty() or self.is_leaf():
            return None
        elif tree is self:
            return None
        else:
            return self._depth_helper(tree)

    def _depth_helper(self, tree: QuadTree) -> Optional[int]:
        """
        Helper method for depth using the parameter tree.
        """
        if self.is_empty() or self.is_leaf():
            if tree is self:
                return 0
            else:
                return None
        elif tree is self:
            return 0
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

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the
        location of any players.

        Runtime: O(1)
        """
        return self._name is None and self.is_leaf()


def _calc_point(point: Tuple[int, int], direction: str, steps: int) -> \
        Tuple[int, int]:
    """
    Return the coordinate <steps> away from <point> in <direction>.
    """
    if direction == 'N':
        return point[0], point[1] - steps
    elif direction == 'S':
        return point[0], point[1] + steps
    elif direction == 'W':
        return point[0] - steps, point[1]
    else:
        return point[0] + steps, point[1]


def _find_xy_range(point: Tuple[int, int], direction: str, distance: int) -> \
        Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Return the range within <distance> away from <point> in <direction>.
    """
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
    A TwoDTree. Concrete implementation of Tree.

    === Private Attributes ===
    _name: name of the tree
    _point: point of the tree
    _nw: the x/y coordinates of the north west corner of the rectangle
    described by this tree
    _se: the x/y coordinates of the south east corner of the rectangle described
     by this tree
    _lt: a 2D-tree that represents the either the north-most or west-most
    section of the rectangle
    _gt: a 2D-tree that represents the either the south-most or east-most
    section of the rectangle
    _split_type: a string indicating whether this rectangle should be split
    vertically or horizontally

    === Representation Invariants ===
    - all nodes must have _name and _point attributes unless they have no
    descendants and no parents.
    - a node with no parents must have a _split_type == 'x'
    - a non-root node should have a value of None for both its _nw and _se
    attributes.
    - a root node should not have a value of None for its _nw and _se
    attributes.
    - a node with _split_type == 'x' must not have a parent or any children with
     _split_type == 'x'
    - a node with _split_type == 'y' must not have a parent or any children with
     _split_type == 'y'
    - all descendants of a given node p must have a _point that falls in the
    rectangle described by _nw and _se
    - for a given node p, if _split_type == 'x' then:
    - all descendants d of p must be in p._lt if d._point[0] <= p._point[0] and
    be in p._gt otherwise
    - for a given node p, if _split_type == 'y' then:
    - all descendants d of p must be in p._lt if d._point[1] <= p._point[1] and
    be in p._gt otherwise
    """
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Optional[Tuple[int, int]]
    _se: Optional[Tuple[int, int]]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Optional[Tuple[int, int]],
                 se: Optional[Tuple[int, int]]) -> None:
        """Initialize a new Tree instance with <nw> and <se>.

        Runtime: O(1)

        >>> t1 = TwoDTree((0, 0), (100, 100))
        >>> t2 = TwoDTree((0, 0), (200, 200))
        """
        self._name = None
        self._point = None
        self._nw = nw
        self._se = se
        self._lt = None
        self._gt = None
        self._split_type = 'x'

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between
        the size of the _lt subtree and the size of the _gt subtree for all
        trees in <self>.

        === Precondition ===
        It is possible to balance this tree

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.balance()
        """
        lt_size = self._lt.size() if self._lt is not None else 0
        gt_size = self._gt.size() if self._gt is not None else 0

        while abs(lt_size - gt_size) > 1:
            name = self._name
            point = self._point
            if lt_size > gt_size:
                self._remove_root_request('promote_left')
            else:
                self._remove_root_request('promote_right')
            self.insert(name, point)

            lt_size = self._lt.size() if self._lt is not None else 0
            gt_size = self._gt.size() if self._gt is not None else 0

        if self._lt is not None:
            self._lt.balance()
        if self._gt is not None:
            self._gt.balance()

    def _remove_root_request(self, request: str) -> None:
        """
        Helper for balance.
        """
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

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> 'a' in t
        True
        >>> 'b' in t
        True
        >>> 'c' in t
        False
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

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> t.contains_point((25, 25))
        True
        >>> t.contains_point((75, 75))
        True
        >>> t.contains_point((50, 50))
        False
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

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Runtime: O(log(n))

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (50, 50))
        >>> 'a' in t
        True
        """
        if not (self._nw[0] <= point[0] <= self._se[0] and
                self._nw[1] <= point[1] <= self._se[1]) or \
                self.contains_point(point):
            raise OutOfBoundsError
        else:
            self._insert_helper(name, point)

    def _insert_helper(self, name: str, point: Tuple[int, int]) -> None:
        """
        Helper method for insert using parameters name and point.
        """
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

    def _insert_node_helper(self, name: str, point: Tuple[int, int]) -> None:
        """
        Helper method for inserting node at the right subtree attribute with
        parameters name and point
        """
        if (self._split_type == 'x' and point[0] <= self._point[0]) or\
                (self._split_type == 'y' and point[1] <= self._point[1]):  # LX
            self._lt = TwoDTree(None, None)
            self._lt._name = name
            self._lt._point = point
            self._lt._split_type = 'y' if self._split_type == 'x' else 'x'
        else:  # LD
            self._gt = TwoDTree(None, None)
            self._gt._name = name
            self._gt._point = point
            self._gt._split_type = 'y' if self._split_type == 'x' else 'x'

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> t.remove('a')
        >>> 'a' in t
        False
        >>> t.remove('b')
        >>> t.is_empty()
        True
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

    def _remove_root(self) -> None:
        """
        Helper method for removing the root.
        """
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
        """
        Helper method returning name and point of the requested tree.
        """
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

    def _collect_all_nodes_info(self) -> List[tuple]:
        """
        Helper method for remove.
        Return the name and point of all the nodes in the tree.
        """
        if self.is_leaf():
            return [(self._name, self._point)]
        elif self._lt is not None and self._gt is not None:
            return [(self._name, self._point)] + \
                   self._lt._collect_all_nodes_info() + \
                   self._gt._collect_all_nodes_info()
        elif self._lt is not None:
            return [(self._name, self._point)] + \
                   self._lt._collect_all_nodes_info()
        else:  # gt is not None
            return [(self._name, self._point)] + \
                   self._gt._collect_all_nodes_info()

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> t.remove_point((25, 25))
        >>> t.contains_point((25, 25))
        False
        >>> t.remove_point((75, 75))
        >>> t.is_empty()
        True
        """
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._point == point:
                self._name = None
                self._point = None
        else:
            if self._point == point:
                self._remove_root()
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

    def move(self, name: str, direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (75, 75))
        >>> t.move('a', 'N', 10)
        (75, 65)
        >>> t.contains_point((75, 65))
        True
        >>> t.contains_point((75, 75))
        False
        """
        if self.is_empty():
            return None
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
                return None
        else:
            point = self._find_point(name)
            if point is not None:
                new_point = _calc_point(point, direction, steps)
                if not (self._nw[0] <= new_point[0] <= self._se[0] and
                        self._nw[1] <= new_point[1] <= self._se[1]) or \
                        self.contains_point(new_point):
                    raise OutOfBoundsError
                self.remove_point(point)
                self.insert(name, new_point)
                return new_point
            return None

    def _find_point(self, name: str) -> Optional[Tuple[int, int]]:
        """
        Helper method for finding the name associated to a point in the tree.
        """
        if self.is_empty():
            return None
        elif self.is_leaf():
            if self._name == name:
                return self._point
            else:
                return None
        else:
            if self._name == name:
                return self._point
            elif self._lt is not None and name in self._lt:
                return self._lt._find_point(name)
            elif self._gt is not None and name in self._gt:
                return self._gt._find_point(name)
            else:
                return None

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree
        (before moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (75, 75))
        >>> t.move_point((75, 75), 'N', 10)
        (75, 65)
        >>> t.contains_point((75, 65))
        True
        >>> t.contains_point((75, 75))
        False
        """
        if self.is_empty():
            return None
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
            else:
                return None
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
                return None
        else:
            return None

    def _find_name(self, point: Tuple[int, int]) -> Optional[str]:
        """
        Helper method for finding the name corresponding to a point in the tree.
        """
        if self.is_empty():
            return None
        elif self.is_leaf():
            if self._point == point:
                return self._name
            else:
                return None
        elif self._point == point:
            return self._name
        elif (self._split_type == 'x' and point[0] <= self._point[0]) or \
                (self._split_type == 'y' and point[1] <= self._point[1]):
            return self._lt._find_name(point) \
                if self._lt is not None else None
        else:
            return self._gt._find_name(point) \
                if self._gt is not None else None

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at: (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> t.names_in_range((40, 40), 'NW', 20)
        ['a']
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

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.size()
        1
        >>> t.insert('a', (25, 25))
        >>> t.size()
        1
        >>> t.insert('b', (75, 75))
        >>> t.size()
        2
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

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.height()
        1
        >>> t.insert('a', (25, 25))
        >>> t.height()
        1
        >>> t.insert('b', (75, 75))
        >>> t.height()
        2
        >>> t.insert('c', (50, 50))
        >>> t.height()
        3
        """
        if self.is_empty():
            return 1
        elif self.is_leaf():
            return 1
        else:
            return 1 + max([self._lt.height() if self._lt is not None else 0,
                            self._gt.height() if self._gt is not None else 0])

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>.
        Return None if <tree> is not a descendant of <self>

        Runtime: O(log(n))

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert('a', (25, 25))
        >>> t.insert('b', (75, 75))
        >>> a = t._gt
        >>> t.depth(a)
        1
        >>> t.depth(t)
        """
        if not isinstance(tree, TwoDTree):
            return None
        elif self.is_empty() or self.is_leaf():
            return None
        elif tree is self:
            return None
        else:
            return self._depth_helper(tree)

    def _depth_helper(self, tree: TwoDTree) -> Optional[int]:
        """
        Helper method for depth using parameter tree.
        """
        if self.is_empty() or self.is_leaf():
            if tree is self:
                return 0
            else:
                return None
        elif tree is self:
            return 0
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

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.is_leaf()
        True
        >>> t.insert('a', (75, 75))
        >>> t.is_leaf()
        True
        >>> t.insert('b', (50, 50))
        >>> t.is_leaf()
        False
        """
        return self._lt is None and self._gt is None

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the
        location of any players.

        Runtime: O(1)

        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.is_empty()
        True
        >>> t.insert('a', (75, 75))
        >>> t.is_empty()
        False
        """
        return self._name is None and self.is_leaf()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing'],
                                'disable': ['R0913', 'R0902', 'W0611', 'R1710',
                                            'R1702']})
