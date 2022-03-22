#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math

class Peg(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Peg(%s, %s)" % (self.x, self.y)

    def distance_from(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

class WarpBoard(object):
    OUTER_WIDTH = 689
    RAIL_THICKNESS = 22
    XBAR_PEGS_SEP = 110
    RAIL_PEGS_SEP = 95
    XBAR_RAIL_PEG_SEP = 45

    def __init__(self):
        self.pegs = []
        x, y = self.XBAR_PEGS_SEP*1.5, 0
        for i in range(4):
            self._add_peg(x, y)
            x -= self.XBAR_PEGS_SEP
        x = (self.OUTER_WIDTH - self.RAIL_THICKNESS)/2
        y = self.XBAR_RAIL_PEG_SEP
        for i in range(5):
            self._add_peg(x, y)
            self._add_peg(-x, y)
            y += self.RAIL_PEGS_SEP

    def _add_peg(self, *args):
        print("peg %2d: %s" % (len(self.pegs), args))
        self.pegs.append(Peg(*args))

    def path_length(self, *path):
        if len(path) == 1 and type(path[0]) == type(""):
            path = tuple(int(c, 16) for c in path[0])
        result = 0
        path = [self.pegs[i] for i in path]
        for ab in zip(path[:-1], path[1:]):
            a, b = ab
            result += b.distance_from(a)
            print("result =", result)
        return result

def main():
    b = WarpBoard()
    #print("total =", b.path_length("01236587a9cbd"))   # 5.72m
    print("total =", b.path_length("01236789abc"))      # 4.87m
    #print("total =", b.path_length("0123547698badc"))  # 6.53m

if __name__ == "__main__" or True:
    if "sys" not in locals():
        import sys
    assert sys.version_info >= (3,)
    main()
