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
        bit.PrintBit()

        test = [2, 1, 4, 1, 0, 8, 10, 2]

        small_tree_style = deepcopy(BoxTree.defaultStyle)
        small_tree_style["rect"]["height"] = 0.25
        small_trees = VGroup()
        for i in range(len(M2)):
            small_trees.add(BoxTree([0 for _ in range(len(M2[i]))], style=small_tree_style, show_indices=True, show_values=False).create().scale(0.75))

        small_trees.arrange(UP, buff=1)
        self.play(LaggedStart(*[FadeIn(tree) for tree in small_trees], lag_ratio=0.5))
        self.wait(0.75)

        big_tree_style = deepcopy(BoxTree.defaultStyle)
        big_tree_style['x_buffer'] = 1.01
        #(small_trees[1].get_center() - small_trees[0].get_center())[1] - big_tree_style["rect"]["height"]*2
        big_tree_style["y_buffer"] = 0.4
        big_tree_style["rect"]["height"] = 0.35
        big_tree_style["rect"]["width"] = small_trees[0].get_height()

        big_tree = BoxTree([0 for _ in range(len(M2))], show_indices=True, show_values=False, style=big_tree_style).create().rotate(PI/2).move_to(small_trees.get_corner(DL),DR).shift(LEFT*0.3)
        self.play(FadeIn(big_tree))
        self.play(big_tree.animate.to_edge(LEFT).shift(RIGHT*1.5))
        self.play(small_trees.animate.move_to(big_tree.get_corner(DR),DL).shift(RIGHT*0.3))
        self.wait(2)

        fenwick_mat_label = Text("Fenwick Tree Matrix", weight=SEMIBOLD, font="DejaVu Sans Condensed", font_size=36).to_corner(UR).shift(LEFT*1)
        dBitMatrix = Matrix(bit.BIT).scale(0.7).move_to(fenwick_mat_label.get_bottom(),UP).shift(DOWN*0.2)
        self.play(
            AnimationGroup(Write(fenwick_mat_label),
            Create(dBitMatrix)
            ,lag_ratio=0.2
            ))
        self.wait(0.5)

        base_mat_label = Text("Base Matrix", weight=SEMIBOLD, font="DejaVu Sans Condensed", font_size=36).next_to(dBitMatrix,DOWN).shift(DOWN*0.2)
        base_mat = Matrix(M2).scale(0.7).move_to(base_mat_label.get_bottom(),UP).shift(DOWN*0.2)
        self.play(AnimationGroup(Write(base_mat_label), 
        Create(base_mat), 
        lag_ratio=0.2))
        self.wait(0.5)

        operations = bit.CreatePositions()

        for i,op in enumerate(operations):
            base_row = base_mat.get_rows()[op[0][0]]
            base_col = base_row[op[0][1]]
            base_rect = SurroundingRectangle(base_col, color=GREEN, buff=0.1)
            self.play(Create(base_rect))
            self.wait(0.5)

            big_unhighlights = []
            small_unhighlights = []
            bit_rects = []
            small_tree_batch_highlights = []
            big_tree_batch_highlights = []
            fadein_bit_numbers = []
            fadeout_bit_numbers = []
            if i < 2:
                for update in op[1]:
                    bit_rect = SurroundingRectangle(dBitMatrix.get_rows()[update[0]][update[1]], color=GREEN, buff=0.1)
                    bit_rects.append(bit_rect)
                    self.play(Create(bit_rect))
                    self.wait(0.15)
                    self.play(FadeOut(dBitMatrix.get_rows()[update[0]][update[1]]), run_time=0.5)
                    new_obj = dBitMatrix.get_rows()[update[0]][update[1]].become(MathTex(str(update[2])).scale(0.6).move_to(dBitMatrix.get_rows()[update[0]][update[1]]))
                    self.play(FadeIn(new_obj),run_time=0.5)

                    big_unhighlights.append(big_tree[update[0]-1])
                    small_unhighlights.append(small_trees[update[0]-1][update[1]-1])
                    self.play(big_tree[update[0]-1].animate.highlight(GREEN),
                            small_trees[update[0]-1][update[1]-1].animate.highlight(GREEN)
                            )
                    self.wait(0.15)
            else:
                # Faster version that highlights everything at once
                #TODO: Try and find a neater way to fade them out by somehow delaying the actual value overwrite
                for update in op[1]:
                    bit_rect = SurroundingRectangle(dBitMatrix.get_rows()[update[0]][update[1]], color=GREEN, buff=0.1)
                    bit_rects.append(bit_rect)
                    fadeout_bit_numbers.append(FadeOut(dBitMatrix.get_rows()[update[0]][update[1]], run_time=0.5))
                    big_unhighlights.append(big_tree[update[0]-1])
                    small_unhighlights.append(small_trees[update[0]-1][update[1]-1])
                    big_tree_batch_highlights.append(big_tree[update[0]-1].animate.highlight(GREEN))
                    small_tree_batch_highlights.append(small_trees[update[0]-1][update[1]-1].animate.highlight(GREEN))

                #self.play(*fadeout_bit_numbers)
                self.play(*fadeout_bit_numbers)
                for update in op[1]:
                    new_obj = dBitMatrix.get_rows()[update[0]][update[1]].become(MathTex(str(update[2])).scale(0.6).move_to(dBitMatrix.get_rows()[update[0]][update[1]]))
                    fadein_bit_numbers.append(FadeIn(new_obj, run_time=0.5))
                self.play(*[Create(rect) for rect in bit_rects],
                          *fadein_bit_numbers,
                          *big_tree_batch_highlights,
                          *small_tree_batch_highlights)
                self.wait(0.8)
            

            self.play(*[box.animate.unhighlight() for box in big_unhighlights],
                      *[box.animate.unhighlight() for box in small_unhighlights],
                      *[Uncreate(rect) for rect in bit_rects]
                      )
            self.wait(0.15)
            self.play(Uncreate(base_rect))
            self.wait(0.15)