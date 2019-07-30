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
        if self.is_empty():
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
                self._name = None
                self._point = None
                new_tree = QuadTree(self._find_centre(point))
                new_tree._name = name
                new_tree._point = point
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


            # demoted_tree = QuadTree(self._calc_centre(self._point))
            # demoted_tree._name = self._name
            # demoted_tree._point = self._point
            # new_tree = QuadTree(self._calc_centre(point))
            # new_tree._name = name
            # new_tree._point = point
            # if demoted_tree._find_quad() == new_tree._find_quad():
            #     self._name = None
            #     self._point = None
            #     split_quad = QuadTree(self._calc_centre(new_tree._centre))
            #     split_quad.insert(new_tree)
            #     split_quad.insert(demoted_tree)
            #     self.insert(split_quad)
            #
            # else:
            #     self._name = None
            #     self._point = None
            #     self._insert_quad(demoted_tree, demoted_tree._region())
            #     self._insert_quad(new_tree, new_tree._region())

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
            # if self._name == name:
            #     self._name = None
            #     self._point = None
            #     self._nw = None
            #     self._ne = None
            #     self._sw = None
            #     self._se = None
            if self._nw is not None and name in self._nw:
                # MAKE HELPER LMAO
                self._nw.remove(name)
                if self._nw.is_leaf():
                    self._nw = None
                    if self._ne is None and self._sw is None and self._se is None:
                        self._name = None
                        self._point = None
                else:
                    # amount = [self._nw._nw, self._nw._ne, self._nw._sw, self._nw._se]
                    # while None in amount:
                    #     amount.remove(None)
                    # if len(amount) == 1:
                    #     self._nw = amount[0]  # promotion
                    #     self._nw._nw = None
                    #     self._nw._ne = None
                    #     self._nw._sw = None  # lol change this part
                    #     self._nw._se = None  # deleting for promotion
                    # elif len(amount) == 2 and amount[1].is_empty()
                    #     self._set_to_none(amount[1])
                    #     or
                    #          ((amount[0].is_empty()))):
                    




            elif self._ne is not None and name in self._ne:
                self._ne.remove(name)
                if self._ne.is_leaf():
                    self._ne = None
                    if self._nw is None and self._sw is None and self._se is None:
                        self._name = None
                        self._point = None
                else:
                    amount = [self._ne._nw, self._ne._ne, self._ne._sw,
                              self._ne._se]
                    while None in amount:
                        amount.remove(None)
                    if len(amount) == 1:
                        self._ne = amount[0]  # promotion
                        self._ne._nw = None
                        self._ne._ne = None
                        self._ne._sw = None  # lol change this part
                        self._ne._se = None  # deleting for promotion


            elif self._sw is not None and name in self._sw:
                self._sw.remove(name)
                if self._sw.is_leaf():
                    self._sw = None
                    if self._ne is None and self._nw is None and self._se is None:
                        self._name = None
                        self._point = None
                else:
                    amount = [self._sw._nw, self._sw._ne, self._sw._sw,
                              self._sw._se]
                    while None in amount:
                        amount.remove(None)
                    if len(amount) == 1:
                        self._sw = amount[0]  # promotion
                        self._sw._nw = None
                        self._sw._ne = None
                        self._sw._sw = None  # lol change this part
                        self._sw._se = None  # deleting for promotion


            elif self._se is not None and name in self._se:
                self._se.remove(name)
                if self._se.is_leaf():
                    self._se = None
                    if self._ne is None and self._sw is None and self._nw is None:
                        self._name = None
                        self._point = None
                else:
                    amount = [self._se._nw, self._se._ne, self._se._sw,
                              self._se._se]
                    while None in amount:
                        amount.remove(None)
                    if len(amount) == 1:
                        self._se = amount[0]  # promotion
                        self._se._nw = None
                        self._se._ne = None
                        self._se._sw = None  # lol change this part
                        self._se._se = None  # deleting for promotion

    def _remove_helper(self, tree: QuadTree, subtree: QuadTree):


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
                pass
            elif point[0] <= self._centre[0] and point[1] > self._centre[1]:  # SW
                pass
            elif point[0] > self._centre[0] and point[1] <= self._centre[1]:  # EAST
                pass
            elif point[0] > self._centre[0] and point[1] > self._centre[1]:  # SE
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



            # self._ne.depth(tree._ne) == 1 and self._nw.depth(tree._nw) and
            # ne_depth = self._ne
            # nw_depth =
            # se_depth
            # sw_depth



        # if not isinstance(tree, QuadTree):
        #     return False
        # elif self.is_empty():
        #     return tree.is_empty()
        # elif self.is_leaf():
        #     return self._name == tree._name
        # else:
        #     if not (self._ne == tree._ne and self._nw == tree._nw and
        #             self._se == tree._se and self._sw == tree._sw):
        #         return False
        #     else:
        #         pass


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
