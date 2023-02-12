import logging
import math

logger = logging.getLogger(__name__)

class Peg:
    def __init__(self, x, y, key=None):
        self.x = x
        self.y = y
        self.key = key

    def __str__(self):
        return f"Peg(({self.x}, {self.y}), key={self.key!r})"

    @property
    def _length(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    @property
    def _unit(self):
        scale = 1 / self._length
        return Peg(self.x * scale, self.y * scale)

    def _dot(self, other):
        return self.x*other.x + self.y*other.y

    def distance_from(self, other):
        ab = Peg(self.x - other.x, self.y - other.y)
        return ab._length

    def angle_around(self, a, c):
        ab = Peg(self.x - a.x, self.y - a.y)
        bc = Peg(c.x - self.x, c.y - self.y)
        return math.acos(ab._unit._dot(bc._unit))

class WarpBoard:
    def __init__(self):
        self.pegs = {}

    def _add_peg(self, *args):
        key = f"{len(self.pegs):x}"
        peg = self.pegs[key] = Peg(*args, key=key)
        logger.debug(f"{self.__class__.__name__}: peg {key}: {peg}")

    def path_length(self, *path):
        if len(path) == 1 and type(path[0]) == type(""):
            path = tuple(path[0])
        result = 0
        path = [self.pegs[i] for i in path]
        for abc in zip(path[:-1], path[1:], path[2:] + [path[-2]]):
            a, b, c = abc
            logmsg = [f"{a.key} -> {b.key} -> {c.key}; result = {result:.0f}"]
            result += b.distance_from(a)
            logmsg.append(f"-> {result:.0f}")
            angle = b.angle_around(a, c)
            result += self.PEG_RADIUS*angle
            logmsg.append(f"-> {result:.0f}")
            logger.debug(" ".join(logmsg))
        logger.debug(f"total warp length = {result}mm")
        return result

class Ashford60cmRHLWB(WarpBoard):
    """The warping board you get with pegs in the holes in the bottom of
    an Ashford 60cm rigid heddle loom.  Peg locations are as follows:

       3 2 1 0
      5       4
      7       6
      9       8
      b       a
      d       c

    The booklet that came with the loom, "Learn to weave on the Rigid
    Heddle Loom," indicates peg 0 to be the starting peg, but peg 3 is
    likely more natural if you're right-handed. """

    OUTER_WIDTH = 689
    RAIL_THICKNESS = 22
    XBAR_PEGS_SEP = 110
    RAIL_PEGS_SEP = 95
    XBAR_RAIL_PEG_SEP = 45
    PEG_RADIUS = 6

    def __init__(self):
        super().__init__()
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

def main():
    #logging.basicConfig(level=logging.DEBUG)
    b = Ashford60cmRHLWB()
    #print("total =", b.path_length("01236587a9cbd"))   # 5.72m -> 5.89m
    #print("total =", b.path_length("01236789abc"))     # 4.87m -> 5.01m
    print("total =", b.path_length("012356789abc"))     # 5.20m -> 5.35m
    #print("total =", b.path_length("0123547698badc"))  # 6.53m -> 6.72m

if __name__ == "__main__":
    main()
