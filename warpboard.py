#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

class Peg(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WarpBoard(object):
    OUTER_WIDTH = 689
    RAIL_THICKNESS = 22
    XBAR_PEGS_SEP = 110
    RAIL_PEGS_SEP = 95
    XBAR_RAIL_PEG_SEP = 45

    @classmethod
    def _init(cls):
        assert not hasattr(cls, "PEGS")
        cls.PEGS = []
        x, y = cls.XBAR_PEGS_SEP*1.5, 0
        for i in range(4):
            cls._add_peg(x, y)
            x -= cls.XBAR_PEGS_SEP
        x = (cls.OUTER_WIDTH - cls.RAIL_THICKNESS)/2
        y = cls.XBAR_RAIL_PEG_SEP
        for i in range(5):
            cls._add_peg(x, y)
            cls._add_peg(-x, y)
            y += cls.RAIL_PEGS_SEP

    @classmethod
    def _add_peg(cls, *args):
        print("peg %2d: %s" % (len(cls.PEGS), args))
        cls.PEGS.append(Peg(*args))

WarpBoard._init()

def main():
    pass

if __name__ == "__main__":
    if "sys" not in locals():
        import sys
    assert sys.version_info >= (3,)
    main()
