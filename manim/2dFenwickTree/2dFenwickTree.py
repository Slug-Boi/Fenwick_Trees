from twoDBit import TwoDBIT
from manim import *
from box_tree import *
from fenwick_tree import FenwickTree

class TwoDFenwick(Scene):
    def construct(self):
        M2 = [
                [3,  4,  0],
                [8,  11, 10],
                [9,  7,  5],
            ]
        bit = TwoDBIT(M2, 3)
        operations = bit.CreatePositions()
        bit.PrintBit()

        test = [2, 1, 4, 1, 0, 8, 10, 2]

        treeStyle = {
            "rect": {
                "height": 0.5,
                "width": 0.5,
                "color": BLUE,
            },
            "value": {},
            "buffer": 0,
            "uplevel": 0.5,
        }

        tempTree = BoxTree(test)
        self.play(Create(tempTree))
        self.play(*tempTree.create())
        self.wait(2)

        # m1 = Matrix(M2)
        # self.play(Create(m1))
        # self.wait(2)
        # self.play(Uncreate(m1))
        # bitMobject = Matrix(bit.getBIT())
        # self.play(Create(bitMobject))
        # self.wait(2)