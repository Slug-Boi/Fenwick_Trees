from twoDBit import TwoDBIT
from manim import *
from box_tree import *
from fenwick_tree import FenwickTree
from copy import deepcopy

class TwoDFenwick(Scene):
    def construct(self):
        M2 = [
                [3,  4,  0, 2],
                [8,  11, 10, 3],
                [9,  7,  5, 8],
                [6,  2,  1, 2],
            ]
        bit = TwoDBIT(M2, 4)
        operations = bit.CreatePositions()
        bit.PrintBit()

        test = [2, 1, 4, 1, 0, 8, 10, 2]

        small_tree_style = deepcopy(BoxTree.defaultStyle)
        small_tree_style["rect"]["height"] = 0.25
        small_trees = VGroup()
        for i in range(len(M2)):
            small_trees.add(BoxTree([0 for _ in range(len(M2[i]))], style=small_tree_style, show_indices=True, show_values=False).scale(0.5))

        small_trees.arrange(UP, buff=1)

        self.play(Create(small_trees,lag_ratio=0.2))
        self.wait(1)
        self.play(*[tree.create() for tree in small_trees])
        self.wait(2)

        big_tree_style = deepcopy(BoxTree.defaultStyle)
        big_tree_style['x_buffer'] = (small_trees[1].get_center() - small_trees[0].get_center())[1] - big_tree_style["rect"]["height"] + small_trees[0][0][2].get_height()/3
        #big_tree_style['y_buffer'] = 0.4
        big_tree_style["y_buffer"] = 0.4

        #TODO: add a create function and change current create to animate_create in box_tree module
        big_tree = BoxTree([0 for _ in range(len(M2))], show_indices=True, show_values=False, style=big_tree_style)
        self.play(Create(big_tree))
        self.play(big_tree.create())
        self.add(big_tree.rotate(PI/2).move_to(small_trees.get_corner(DL),DR).shift(LEFT*0.2))
        self.wait(2)
