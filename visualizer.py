#  COPY PASTE IN QUAD TREE CLASS ----------------------------------------
def __str__(self) -> str:
    """Return a string representation of this tree.

    For each node, its item is printed before any of its
    descendants' items. The output is nicely indented.

    You may find this method helpful for debugging.
    """
    return self._str_indented()


def _str_indented(self, depth: int = 0, subtree: str = '') -> str:
    """Return an indented string representation of this tree.

    The indentation level is specified by the <depth> parameter.
    """
    if self.is_empty():
        return ''
    else:
        name = self._name + '->' if self._name is not None else '<O>'
        point = str(self._point) if self._point is not None else '  '
        s = '    ' * depth + subtree + name + point + '\n'
        if self._nw is not None:
            s += self._nw._str_indented(depth + 1, 'NW: ')
        if self._ne is not None:
            s += self._ne._str_indented(depth + 1, 'NE: ')
        if self._sw is not None:
            s += self._sw._str_indented(depth + 1, 'SW: ')
        if self._se is not None:
            s += self._se._str_indented(depth + 1, 'SE: ')
        return s
#  ----------------------------------------------------------------------

#  COPY PASTE IN TWO-D TREE CLASS ---------------------------------------
def __str__(self) -> str:
    """Return a string representation of this tree.

    For each node, its item is printed before any of its
    descendants' items. The output is nicely indented.

    You may find this method helpful for debugging.
    """
    return self._str_indented()


def _str_indented(self, depth: int = 0, subtree: str = '') -> str:
    """Return an indented string representation of this tree.

    The indentation level is specified by the <depth> parameter.
    """
    if self.is_empty():
        return ''
    else:
        s = '      ' * depth + subtree + str(f'<{self._split_type}> ') + \
            self._name + '->' + str(self._point) + '\n'
        if self._lt is not None:
            s += self._lt._str_indented(depth + 1, 'lt: ')
        if self._gt is not None:
            s += self._gt._str_indented(depth + 1, 'gt: ')
        return s

#  ------------------------------------------------------------------------

    # t = TwoDTree((0, 0), (500, 500))
    # t.insert('a', (200, 300))
    # t.insert('b', (250, 260))
    # t.insert('c', (400, 400))
    # t.insert('d', (450, 450))
    # t.insert('e', (425, 425))
    # t.insert('f', (475, 475))
    # t.insert('g', (150, 150))
    # t.insert('h', (125, 125))
    # t.insert('i', (150, 375))
    # t.balance()
    # print(t)

    # q = QuadTree((250, 250))
    # q.insert('a', (175, 175))
    # q.insert('b',  (175, 176))
    # q.insert('c', (300, 160))
    # q.insert('d', (320, 350))
    # q.insert('e', (100, 300))
    # q.remove('a')
    # q.insert('a', (175, 175))
    # q.insert('f', (120, 180))
    # print(q)
