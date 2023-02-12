import math

class Peg:
    def __init__(self, x, y, key=None):
        self.x = x
        self.y = y
        self.key = key

    def __str__(self):
        return "Peg((%s, %s), key=%s)" % (self.x, self.y, self.key)

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
    OUTER_WIDTH = 689
    RAIL_THICKNESS = 22
    XBAR_PEGS_SEP = 110
    RAIL_PEGS_SEP = 95
    XBAR_RAIL_PEG_SEP = 45
    PEG_RADIUS = 6

    def __init__(self):
        self.pegs = {}
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
        key = "%x" % len(self.pegs)
        print("peg %s: %s" % (key, args))
        self.pegs[key] = Peg(*args, key=key)

    def path_length(self, *path):
        if len(path) == 1 and type(path[0]) == type(""):
            path = tuple(path[0])
        result = 0
        path = [self.pegs[i] for i in path]
        for abc in zip(path[:-1], path[1:], path[2:] + [path[-2]]):
            a, b, c = abc
            print(a.key, "->", b.key, "->", c.key, end="; ")
            result += b.distance_from(a)
            #print("result =", result)
            angle = b.angle_around(a, c)
            #print("angle = %.0fdeg" % (angle*180/math.pi))
            result += self.PEG_RADIUS*angle
            print("result =", result)
        return result

#  3 2 1 0
# 5       4
# 7       6
# 9       8
# b       a
# d       c

def main():
    b = WarpBoard()
    #print("total =", b.path_length("01236587a9cbd"))   # 5.72m -> 5.89m
    #print("total =", b.path_length("01236789abc"))     # 4.87m -> 5.01m
    print("total =", b.path_length("012356789abc"))     # 5.20m -> 5.35m
    #print("total =", b.path_length("0123547698badc"))  # 6.53m -> 6.72m

if __name__ == "__main__":
    main()
