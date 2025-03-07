from manim import *
from math import log2
from fenwick_tree import FenwickTree

class TreeElement(VGroup):
    def __init__(self, rect, value):
        super().__init__()
        self.rect = rect
        self.value = value.move_to(self.rect)
        self += self.rect
        self += self.value

class BoxTree(VGroup):
    def __init__(self, array, rectHeight=0.5, uplevel=None, buffer=0):
        super().__init__()
        self.buffer = buffer
        self.array = array
        self.rectHeight = rectHeight
        if uplevel:
            self.uplevel = uplevel
        else:
            self.uplevel = rectHeight
        for v in self.array:
            self += TreeElement(Rectangle(height=rectHeight, width=rectHeight, color=BLUE), Text(str(v), weight=SEMIBOLD).scale(0.4))
        self.arrange(buff=self.buffer)
        self.move_to(ORIGIN)
    
    @staticmethod
    def _tree_level(index) -> int:
        lsb = index & -index
        return int(log2(lsb))

    def create(self):
        tree = FenwickTree(self.array)
        animations = []
        for i, elf in enumerate(self.array):
            level = self._tree_level(i+1)
            # upShift = self[i].animate.shift(UP*self.uplevel*level)
            boxWidth = self.rectHeight*2**level + (2**level-1)*self.buffer
            newElement = (
                TreeElement(Rectangle(
                    height=self.rectHeight, 
                    width=boxWidth, 
                    color=BLUE
                    ), 
                    Text(str(tree.get_tree()[i+1]), weight=SEMIBOLD)
                    .scale(0.4)
                )
                .move_to(self[i].get_right(), RIGHT)
                .shift(UP*self.uplevel*level)
            )
            domainExpansion = Transform(self[i], newElement)
            animations.append(domainExpansion)

        return animations

