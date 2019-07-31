from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
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
            #  use in

        # if self._ne is None and self._nw is None and self._se is None and \
        #         self._sw is None: # use all()
        #     if self._name is None:  # remove is None
        #         return False
        #     else:
        #         return self._name == name
        # else:
        #     return (self._ne is not None and self._ne.__contains__(name))\
        #            or (self._nw is not None and self._nw.__contains__(name))\
        #            or (self._se is not None and self._se.__contains__(name))\
        #            or (self._sw is not None and self._sw.__contains__(name))
        #     #  use in

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._point == point
        else:
            if point[0] <= self._centre[0]:  # WEST
                if point[1] <= self._centre[1]:  # NW
                    return self._nw.contains_point(point) if self._nw is not None else False
                else:  # SW
                    return self._sw.contains_point(point) if self._sw is not None else False
            else:  # EAST
                if point[1] <= self._centre[1]:  # NE
                    return self._ne.contains_point(point) if self._ne is not None else False
                else:  # SE
                    return self._se.contains_point(point) if self._se is not None else False

        # if self._ne is None and self._nw is None and self._se is None and \
        #         self._sw is None: # use all()
        #     if self._point is None:  # remove is None
        #         return False
        #     else:
        #         return self._point == point
        # else:  # confirm once more the directions
        #     if point[0] <= self._point[0]:  # WEST
        #         if point[1] <= self._point[1]:  # NW
        #             return self._nw.contains_point(point)
        #         else:  # SW
        #             return self._sw.contains_point(point)
        #     else: # EAST
        #         if point[1] <= self._point[1]:  # NE
        #             return self._ne.contains_point(point)
        #         else:  # SE
        #             return self._se.contains_point(point)

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        if not (point[0] <= 2 * self._centre[0] and point[1] <= 2 *
                self._centre[1]) \
                or self.contains_point(point):
            raise OutOfBoundsError
        elif self.is_empty():
            self._name = name
            self._point = point
        elif self.is_leaf():
            # maybe calc this once and store in var to re-use
            if self._find_region(self._point) == self._find_region(point):
                # copying
                demoted_tree = QuadTree(self._find_centre(self._centre))
                demoted_tree._name = self._name
                demoted_tree._point = self._point

                # emptying
                self._name = None
                self._point = None
                demoted_tree.insert(name, point)  # recursion

                # sex
                self._insert_region(demoted_tree)
            else:
                old_tree = QuadTree(self._find_centre(self._centre))
                old_tree._name = self._name
                old_tree._point = self._point

                self._name = None
                self._point = None

                new_tree = QuadTree(self._find_centre(point))
                new_tree._name = name
                new_tree._point = point

                self._insert_region(old_tree)
                self._insert_region(new_tree)
        else:
            if point[0] <= self._centre[0]:  # WEST
                if point[1] <= self._centre[1]:  # NW
                    if self._nw is None:
                        self._nw = QuadTree(self._find_centre(point))
                    self._nw.insert(name, point)
                else:  # SW
                    if self._sw is None:
                        self._sw = QuadTree(self._find_centre(point))
                    self._sw.insert(name, point)
            else:  # EAST
                if point[1] <= self._centre[1]:  # NE
                    if self._ne is None:
                        self._ne = QuadTree(self._find_centre(point))
                    self._ne.insert(name, point)
                else:  # SE
                    if self._se is None:
                        self._se = QuadTree(self._find_centre(point))
                    self._se.insert(name, point)

    def _find_region(self, point: Tuple[int, int]) -> str:
        pass

    def _insert_region(self, tree: QuadTree) -> None:
        pass

    def _find_centre(self, point) -> Tuple[int, int]:
        pass

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
        else:
            # if self._nw is not None and self.is_leaf() and self._nw._name == name:
            #     pass
            if self._nw is not None and name in self._nw:
                # REMOVE FROM NW -> IF NW EMPTY THEN RID OF IT
                #                -> IF ONLY ONE GOOD ITEM LEFT THEN CLEAN THEN PROMOTE
                #                -> MULTIPLE GOOD ITEMS THEN LEAVE AS IS
                #                GOOD ITEM == NOT EMPTY, NOT NONE
                #                BAD ITEM == EMPTY(MUST BE CLEANED) OR NONE
                self._nw.remove(name)
                if self._nw.is_empty():
                    self._nw = None
                else:
                    # CLEAN UP
                    if self._nw._nw.is_empty():
                        self._nw._nw = None
                    if self._nw._ne.is_empty():
                        self._nw._ne = None
                    if self._nw._sw.is_empty():
                        self._nw._sw = None
                    if self._nw._se.is_empty():
                        self._nw._se = None
                    amount = [self._nw._nw, self._nw._ne, self._nw._sw, self._nw._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._nw = amount[0] # PUSHING IT UP
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
                    # CLEAN UP
                    if self._ne._nw.is_empty():
                        self._ne._nw = None
                    if self._ne._ne.is_empty():
                        self._ne._ne = None
                    if self._ne._sw.is_empty():
                        self._ne._sw = None
                    if self._ne._se.is_empty():
                        self._ne._se = None
                    amount = [self._ne._nw, self._ne._ne, self._ne._sw,
                              self._ne._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._ne = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._ne._nw = None
                        self._ne._ne = None
                        self._ne._sw = None
                        self._ne._se = None

            elif self._sw is not None and name in self._sw:
                self._sw.remove(name)
                if self._sw.is_empty():
                    self._sw = None
                else:
                    # CLEAN UP
                    if self._sw._nw.is_empty():
                        self._sw._nw = None
                    if self._sw._ne.is_empty():
                        self._sw._ne = None
                    if self._sw._sw.is_empty():
                        self._sw._sw = None
                    if self._sw._se.is_empty():
                        self._sw._se = None
                    amount = [self._sw._nw, self._sw._ne, self._sw._sw,
                              self._sw._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._nw = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._sw._nw = None
                        self._sw._ne = None
                        self._sw._sw = None
                        self._sw._se = None
            elif self._se is not None and name in self._se:
                self._se.remove(name)
                if self._se.is_empty():
                    self._se = None
                else:
                    # CLEAN UP
                    if self._se._nw.is_empty():
                        self._se._nw = None
                    if self._se._ne.is_empty():
                        self._se._ne = None
                    if self._se._sw.is_empty():
                        self._se._sw = None
                    if self._se._se.is_empty():
                        self._se._se = None
                    amount = [self._se._nw, self._se._ne, self._se._sw,
                              self._se._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._se = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
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
        else:
            # if self._name == name:
            #     self._name = None
            #     self._point = None
            #     self._nw = None
            #     self._ne = None
            #     self._sw = None
            #     self._se = None
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:  # NW
                self._nw.remove_point(point)
                if self._nw.is_empty():
                    self._nw = None
                else:
                    # CLEAN UP
                    if self._nw._nw.is_empty():
                        self._nw._nw = None
                    if self._nw._ne.is_empty():
                        self._nw._ne = None
                    if self._nw._sw.is_empty():
                        self._nw._sw = None
                    if self._nw._se.is_empty():
                        self._nw._se = None
                    amount = [self._nw._nw, self._nw._ne, self._nw._sw,
                              self._nw._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._nw = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._nw._nw = None
                        self._nw._ne = None
                        self._nw._sw = None
                        self._nw._se = None
            elif point[0] <= self._centre[0] and point[1] > self._centre[1]:  # SW
                self._sw.remove_point(point)
                if self._sw.is_empty():
                    self._sw = None
                else:
                    # CLEAN UP
                    if self._sw._nw.is_empty():
                        self._sw._nw = None
                    if self._sw._ne.is_empty():
                        self._sw._ne = None
                    if self._sw._sw.is_empty():
                        self._sw._sw = None
                    if self._sw._se.is_empty():
                        self._sw._se = None
                    amount = [self._sw._nw, self._sw._ne, self._sw._sw,
                              self._sw._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._nw = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._sw._nw = None
                        self._sw._ne = None
                        self._sw._sw = None
                        self._sw._se = None
            elif point[0] > self._centre[0] and point[1] <= self._centre[1]:  # NE
                self._ne.remove(name)
                if self._ne.is_empty():
                    self._ne = None
                else:
                    # CLEAN UP
                    if self._ne._nw.is_empty():
                        self._ne._nw = None
                    if self._ne._ne.is_empty():
                        self._ne._ne = None
                    if self._ne._sw.is_empty():
                        self._ne._sw = None
                    if self._ne._se.is_empty():
                        self._ne._se = None
                    amount = [self._ne._nw, self._ne._ne, self._ne._sw,
                              self._ne._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._ne = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._ne._nw = None
                        self._ne._ne = None
                        self._ne._sw = None
                        self._ne._se = None
            elif point[0] > self._centre[0] and point[1] > self._centre[1]:  # SE
                self._se.remove_point(point)
                if self._se.is_empty():
                    self._se = None
                else:
                    # CLEAN UP
                    if self._se._nw.is_empty():
                        self._se._nw = None
                    if self._se._ne.is_empty():
                        self._se._ne = None
                    if self._se._sw.is_empty():
                        self._se._sw = None
                    if self._se._se.is_empty():
                        self._se._se = None
                    amount = [self._se._nw, self._se._ne, self._se._sw,
                              self._se._se]
                    while None in amount:
                        amount.remove(None)
                    # PROMOTION
                    if len(amount) == 1:
                        self._se = amount[0]  # PUSHING IT UP
                        # DELETING FOR PROMOTION
                        self._se._nw = None
                        self._se._ne = None
                        self._se._sw = None
                        self._se._se = None

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
                point = self._point
                if direction == 'N':
                    point = point[0], point[1] - steps
                elif direction == 'S':
                    point = point[0], point[1] + steps
                elif direction == 'W':
                    point = point[0] - steps, point[1]
                else:
                    point = point[0] + steps, point[1]

                if (not (point[0] <= 2 * self._centre[0] and
                         point[1] <= 2 * self._centre[1])) or \
                        self.contains_point(point):
                    raise OutOfBoundsError
                else:
                    self._point = point
                    return self._point
        else:
            if self._nw is not None and name in self._nw:
                point = self.move(name, direction, steps)
                self._nw.remove_point(point)
                self.insert(name, point)
                return point
            elif self._ne:
                pass
            elif self._sw:
                pass
            elif self._se:
                pass


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
        pass

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
            if direction == 'NW':
                final = point[0] - distance, point[1] - distance
            elif direction == 'NE':
                final = point[0] + distance, point[1] - distance
            elif direction == 'SW':
                final = point[0] - distance, point[1] + distance
            else:
                final = point[0] + distance, point[1] + distance
            x_range = [point[0], final[0]]
            y_range = [point[1], final[1]]
            if ((min(x_range) <= self._point[0] <= max(x_range) and
                 min(y_range) <= self._point[1] <= max(y_range))):
                return [self._name]
            else:
                return []
        else:
            subtrees = [self._ne, self._nw, self._se, self._sw]
            while None in subtrees:
                subtrees.remove(None)
            players = []
            for tree in subtrees:
                players.extend(tree.names_in_range(point, direction, distance))
            return players

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        if self.is_empty():
            return 1  # FIXME
        elif self.is_leaf():
            return 1
        else:
            return 1\
                   + (self._ne.size() if self._ne is not None else 0)\
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
            return 1  # FIXME
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
        #  COULD BE 2D
        #  NAME COMPARISON
        #  START = 0 OR 1 ?
        #  is tree literally the tree
        #  ask about repetitive recursion. more runtime but same bound.
        if not isinstance(tree, QuadTree):
            return None
        elif self.is_empty() or self.is_leaf():
            return 1 if self is tree else None
        else:
            if tree._centre[0] <= self._point[0]:  # WEST
                if tree._centre[1] <= self._point[1]:  # NW
                    nw_depth = self._nw.depth(
                        tree) if self._nw is not None else None
                    depth = (1 + nw_depth) if nw_depth is not None else None
                    return depth
                else:  # SW
                    sw_depth = self._sw.depth(
                        tree) if self._sw is not None else None
                    depth = (1 + sw_depth) if sw_depth is not None else None
                    return depth
            else:  # EAST
                if tree._centre[1] <= self._point[1]:  # NE
                    ne_depth = self._ne.depth(
                        tree) if self._nw is not None else None
                    depth = (1 + ne_depth) if ne_depth is not None else None
                    return depth
                else:  # SE
                    se_depth = self._se.depth(
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


class TwoDTree(Tree):
    """

    """
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Tuple[int, int]
    _se: Tuple[int, int]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Tuple[int, int], se: Tuple[int, int]) -> None:
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
        pass

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif self.is_leaf():
            return self._name == name
        else:
            return (self._lt is not None and self._lt.__contains__(name)) \
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
            if (self._split_type == 'x' and point[0] <= self._point[0]) or \
                    (self._split_type == 'y' and point[1] <= self._point[1]):
                self._lt.contains_point(point) if self._lt is not None else False
            else:
                self._gt.contains_point(point) if self._gt is not None else False

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
        elif self.is_empty():
            self._name = name
            self._point = point
        elif self.is_leaf():
            if self._split_type == 'x' and point[0] <= self._point[0]:  # LX
                self._lt = TwoDTree(self._nw, (self._point[0], self._se[1]))
                self._lt._name = name
                self._lt._point = point
            elif self._split_type == 'x':           # RX
                self._gt = TwoDTree((self._point[0], self._nw[1]), self._se)
                self._gt._name = name
                self._gt._point = point
            elif self._split_type == 'y' and point[1] <= self._point[1]:  # LU
                self._lt = TwoDTree(self._nw, (self._se[0], self._point[1]))
                self._lt._name = name
                self._lt._point = point
            else:                                              # LD
                self._gt = TwoDTree((self._nw[0], self._point[1]), self._se)
                self._gt._name = name
                self._gt._point = point
        else:
            if (self._split_type == 'x' and point[0] <= self._point[0]) or \
                    (self._split_type == 'y' and point[1] <= self._point[1]):
                self._lt.insert(name, point)
            else:
                self._gt.insert(name, point)

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        # if self._name == name:
        #     s
        # elif self._lt is not None and name in self._lt:
        #
        # elif name in self._gt:
        #     pass
        if self.is_empty():
            pass
        elif self.is_leaf():
            if self._name == name:
                self._name = None
                self._point = None
        else:
            if self._name == name:
                self.remove_root(name)
            elif self._lt is not None and self._lt.is_leaf() and self._lt._name == name:
                self._lt = None
            elif self._gt is not None and self._gt.is_leaf() and self._gt == name:
                self._gt = None
            elif self._lt is not None and name in self._lt:
                self._lt.remove(name)
            elif self._gt is not None and name in self._gt:
                self._gt.remove(name)







                # LEAF CASE
                # if self._lt._lt is not None and self._lt._lt.is_empty():
                #     self._lt._lt = None
                # elif self._lt._lt is not None:
                #     if self.
                # if self._gt._gt is not None and self._gt._gt.is_empty():
                #     self._gt._gt = None
                # elif self._gt._gt is not None:
                #     pass








                # if self._lt._lt.is_empty():
                #     self._lt._lt = None
                # if self._gt._gt.is_empty():
                #     self._gt._gt = None
                # if self._lt._lt._name == name:
                #     pass
                # elif self._lt._gt._name == name:
                #     pass
            # elif self._gt is not None and name in self._gt:
            #     self._gt.remove(name)

    def _remove_root(self, name):
        pass

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        pass

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
        pass

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
        pass

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
        pass

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        if self.is_empty():
            return 1  # FIXME
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
            return 1  # FIXME
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
        pass

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
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing']})
