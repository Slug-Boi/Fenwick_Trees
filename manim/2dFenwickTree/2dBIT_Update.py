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
        self.bit = TwoDBIT(M2, 4)
        self.bit.Create()

        small_tree_style = deepcopy(BoxTree.defaultStyle)
        small_tree_style["rect"]["height"] = 0.25
        self.small_trees = VGroup()
        for i in range(len(M2)):
            self.small_trees.add(
                BoxTree(
                    [0 for _ in range(len(M2[i]))], 
                    style=small_tree_style, 
                    show_indices=True, 
                    show_values=False
                )
                .create()
                .scale(0.75)
            )

        self.small_trees.arrange(UP, buff=1)
        self.play(LaggedStart(*[FadeIn(tree) for tree in self.small_trees], lag_ratio=0.5), run_time=0.7)
        self.wait(0.75)

        big_tree_style = deepcopy(BoxTree.defaultStyle)
        big_tree_style['x_buffer'] = 1.01
        big_tree_style["y_buffer"] = 0.4
        big_tree_style["rect"]["height"] = 0.35
        big_tree_style["rect"]["width"] = self.small_trees[0].get_height()

        self.big_tree = (
            BoxTree(
                [0 for _ in range(len(M2))], 
                show_indices=True, 
                show_values=False, 
                style=big_tree_style
            )
            .create()
            .rotate(PI/2)
            .move_to(self.small_trees.get_corner(DL),DR).shift(LEFT*0.3)
        )
        self.play(FadeIn(self.big_tree), run_time=0.7)
        self.play(self.big_tree.animate.to_edge(LEFT).shift(RIGHT*1.5), run_time=0.7)
        self.play(self.small_trees.animate.move_to(self.big_tree.get_corner(DR),DL).shift(RIGHT*0.3), run_time=0.7)
        self.wait(1)

        fenwick_mat_label = (
            Text(
                "Fenwick Tree Matrix", 
                weight=SEMIBOLD, 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .to_corner(UR)
            .shift(DOWN*1.2)
        )
        self.dBitMatrix = (
            Matrix(self.bit.BIT)
            .scale(0.55)
            .move_to(fenwick_mat_label.get_bottom(),UP)
            .shift(DOWN*0.2)
        )
        self.play(
            AnimationGroup(Write(fenwick_mat_label),
            Create(self.dBitMatrix)
            ,lag_ratio=0.2
            ))
        self.wait(0.5)

        base_mat_label = (
            Text(
                "Base Matrix", 
                weight=SEMIBOLD, 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .next_to(self.dBitMatrix,DOWN)
            .shift(DOWN*0.2)
        )
        self.base_mat = (
            Matrix(M2)
            .scale(0.55)
            .move_to(base_mat_label.get_bottom(),UP)
            .shift(DOWN*0.2)
        )
        self.play(AnimationGroup(Write(base_mat_label), 
        Create(self.base_mat), 
        lag_ratio=0.2))
        self.wait(0.5)
    
        updatePosition = (1,2)
        updateValue = 4

        self.animateUpdate(updatePosition, updateValue)
        self.wait(2)

        self.animateUpdate((0,1), -3)
        self.wait(2)
    
    def animateUpdate(self, position, val):
        updateText=(
            Text(
                f"Update({position[0]},{position[1]},{val})", 
                font_size=30, 
                weight=MEDIUM, 
                font="DejaVu Sans Condensed"
            )
            .to_edge(UP)
            .shift(RIGHT+DOWN*0.4)
        )
        self.play(Write(updateText))
        self.wait(1)

        updates = self.bit.UpdatePositions(position[0], position[1], val)

        base_row = self.base_mat.get_rows()[position[0]]
        base_col = base_row[position[1]]
        base_rect = SurroundingRectangle(base_col, color=GREEN, buff=0.1)
        self.play(Create(base_rect))
        self.wait(0.25)
        self.play(FadeOut(self.base_mat.get_rows()[position[0]][position[1]]), run_time=0.5)
        new_val = self.bit.startMatrix[position[0]][position[1]] + val
        new_obj = (
            self.base_mat.get_rows()[position[0]][position[1]]
            .become(
                MathTex(str(new_val))
                .scale(0.6)
                .move_to(self.base_mat.get_rows()[position[0]][position[1]])
            )
        )
        self.play(FadeIn(new_obj),run_time=0.5)
        self.wait(0.5)

        big_unhighlights = []
        small_unhighlights = []
        bit_rects = []
        for update in updates:
            bit_rect = SurroundingRectangle(self.dBitMatrix.get_rows()[update[0]][update[1]], color=GREEN, buff=0.1)
            bit_rects.append(bit_rect)
            big_unhighlights.append(self.big_tree[update[0]-1])
            small_unhighlights.append(self.small_trees[update[0]-1][update[1]-1])
            self.play(
                self.big_tree[update[0]-1].animate.highlight(GREEN),
                self.small_trees[update[0]-1][update[1]-1].animate.highlight(GREEN),
                Create(bit_rect),
                run_time=1.5
            )
            self.wait(0.5)
            self.play(FadeOut(self.dBitMatrix.get_rows()[update[0]][update[1]]), run_time=0.5)
            new_obj = (
                self.dBitMatrix.get_rows()[update[0]][update[1]]
                .become(
                    MathTex(str(update[2]))
                    .scale(0.6)
                    .move_to(self.dBitMatrix.get_rows()[update[0]][update[1]])
                )
            )
            self.play(FadeIn(new_obj),run_time=0.5)

           
        self.play(
            *[box.animate.unhighlight() for box in big_unhighlights],        
            *[box.animate.unhighlight() for box in small_unhighlights],
            *[Uncreate(rect) for rect in bit_rects]
        )
        self.wait(0.25)
        self.play(Uncreate(base_rect))
        self.wait(0.25)
        self.play(Unwrite(updateText))