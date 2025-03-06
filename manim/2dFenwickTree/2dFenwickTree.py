from twoDBit import TwoDBIT
from manim import *

class TwoDFenwick(Scene):
    def construct(self):
        M2 = [
                [3,  4,  0],
                [8,  11, 10],
                [9,  7,  5],
            ]
        bit = TwoDBIT(M2, 3)
        bit.Create()
        bit.PrintBit()

        m1 = Matrix(M2)
        self.play(Create(m1))
        self.wait(2)
        self.play(Uncreate(m1))
        bitMobject = Matrix(bit.getBIT())
        self.play(Create(bitMobject))
        self.wait(2)