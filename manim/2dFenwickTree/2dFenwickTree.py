from twoDBit import TwoDBIT
from manim import *
from box_tree import *
from fenwick_tree import FenwickTree
from copy import deepcopy

def binary_index(index,b_len) -> str:
    return "{0:0{b_len}b}".format(index, b_len=b_len)


class TwoDFenwick(Scene):
    def math_animate(self, index, repl_obj, point) -> Text:
        copy_repl = repl_obj.copy()
        copy_result_trans = repl_obj.copy().set_opacity(0)
        self.add(copy_repl)
        bit_value = (
            Text(
                binary_index(index, 3), 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, font_size=30
            )
            .move_to(point)
        )
        lsb = (
            Text(
                "+ "+binary_index((index & -index),3), 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .move_to(bit_value.get_bottom()+DOWN*0.15,UP)
            .align_to(bit_value,RIGHT)
        )
        line = Line(
            lsb.get_corner(DL), 
            lsb.get_corner(DR), 
            color=WHITE
            ).shift(DOWN*0.08)
        result = (
            Text(
                binary_index(index + (index & -index),3), 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .move_to(lsb.get_bottom()+DOWN*0.17,UP)
            .align_to(lsb,RIGHT)
        )
        self.play(LaggedStart(
            Transform(copy_repl, bit_value),
            LaggedStart(
                Write(lsb),
                Create(line),
                Write(result),
                lag_ratio=0.2
            ),
            lag_ratio=0.45
        ))
        self.wait(0.2)
        copy_result_trans.become(
            Text(
                str(index + (index & -index)), 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .move_to(repl_obj)
        )
        self.play(
            FadeOut(copy_repl), 
            FadeOut(bit_value), 
            FadeOut(lsb), 
            FadeOut(line), 
            FadeOut(repl_obj), 
            ReplacementTransform(result,copy_result_trans.set_opacity(1))
        )      
        self.wait(0.2)
        return copy_result_trans

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

        big_tree = (
            BoxTree(
                [0 for _ in range(len(M2))], 
                show_indices=True, 
                show_values=False, 
                style=big_tree_style
            )
            .create()
            .rotate(PI/2)
            .move_to(self.small_trees.get_corner(DL),DR)
            .shift(LEFT*0.3)
        )
        self.play(FadeIn(big_tree), run_time=0.7)
        self.play(big_tree.animate.to_edge(LEFT), run_time=0.7)
        self.play(self.small_trees.animate.move_to(big_tree.get_corner(DR),DL).shift(RIGHT*0.3), run_time=0.7)
        self.wait(1)

        fenwick_mat_label = (
            Text(
                "Fenwick Tree Array", 
                weight=SEMIBOLD, 
                font="DejaVu Sans Condensed", 
                font_size=36
            )
            .to_corner(UR)
            .shift(LEFT*0.2)
        )
        dBitMatrix = (
            Matrix(bit.BIT)
            .scale(0.7)
            .move_to(fenwick_mat_label.get_bottom(),UP)
            .shift(DOWN*0.2)
        )
        self.play(
            AnimationGroup(Write(fenwick_mat_label),
            Create(dBitMatrix),
            lag_ratio=0.2
        ))
        self.wait(0.2)

        base_mat_label = (
            Text(
                "Input Array", 
                weight=SEMIBOLD, 
                font="DejaVu Sans Condensed", 
                font_size=36
            )
            .next_to(dBitMatrix,DOWN)
            .shift(DOWN*0.2)
        )
        base_mat = (
            Matrix(M2)
            .scale(0.7)
            .move_to(base_mat_label.get_bottom(),UP)
            .shift(DOWN*0.2)
        )
        self.play(
            AnimationGroup(Write(base_mat_label), 
            Create(base_mat), 
            lag_ratio=0.2
        ))
        self.wait(0.5)

        operations = bit.CreatePositions()

        # Create codeblock to show shift operations
        codeblock = Code(
            code_file="updateShiftExample.py",
            background="rectangle",
            language="python",
            tab_width=2,
            add_line_numbers=False,
        ).scale_to_fit_width((dBitMatrix.get_left()[0]-self.small_trees.get_right()[0])*0.95).next_to(self.small_trees,RIGHT,buff=0.38).align_to(self.small_trees,DOWN)

        self.sliding_wins = VGroup()

        self.play(FadeIn(codeblock))

        row_col_center_dist = abs(self.small_trees.get_right()[0] - dBitMatrix.get_left()[0])
        # Magic space on x end dont question it 
        row_text = (
            Text(
                "row = ", 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .next_to(self.small_trees,RIGHT,buff=1.5)
        )
        row_value = (
            Text(
                "1", 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .next_to(row_text,RIGHT, buff=0.15)
            .align_to(row_text,DOWN)
        )
        col_text = (
            Text(
                "col =", 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, font_size=30
            )
            .next_to(row_value,RIGHT)
            .align_to(row_text,DOWN)
        )
        col_value = (
            Text(
                "1", 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .next_to(col_text,RIGHT,buff=0.15)
            .align_to(row_value,UP)
        )
        self.row_col_group = VGroup(row_text, row_value, col_text, col_value)
        self.row_col_group.move_to(self.small_trees.get_right() + (row_col_center_dist/2)*RIGHT).to_edge(UP).shift(DOWN*0.7)

        self.play(Write(row_text), Write(row_value), Write(col_text), Write(col_value))


        for line in codeblock.code_lines:
            self.sliding_wins.add(
                SurroundingRectangle(line,buff=0.025)
                .set_fill(YELLOW)
                .set_opacity(0)
                .stretch_to_fit_width(codeblock.background.get_width())
                .align_to(codeblock.background, LEFT)
            )
            if len(self.sliding_wins) > 1:
                self.sliding_wins[-1].stretch_to_fit_height(self.sliding_wins[0].get_height())
                self.sliding_wins[-1].shift(DOWN*0.05)

        self.add(self.sliding_wins)

        shifted_objects = False

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
                previous_x = op[1][0]
                replacement_x = (
                    Text(
                        str(op[0][0]+1), 
                        font="DejaVu Sans Condensed", 
                        weight=SEMIBOLD, 
                        font_size=30
                    )
                    .next_to(row_text,RIGHT,buff=0.15)
                    .align_to(row_text,DOWN)
                )
                self.play(Transform(self.row_col_group[1], replacement_x))
                self.row_col_group[1].become(replacement_x)
                for update in op[1]:
                    bit_rect = (
                        SurroundingRectangle(
                            dBitMatrix.get_rows()[update[0]][update[1]], 
                            color=GREEN, 
                            buff=0.1
                        )
                    )
                    bit_rects.append(bit_rect)

                    # Highlight while x <= matrix_size:
                    if update[0] != previous_x:
                        self.play(self.sliding_wins[0].animate.set_opacity(0.3))
                        self.wait(0.15)
                        self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins],
                                  self.sliding_wins[1].animate.set_opacity(0.3))
                        self.wait(0.15)
                        replacement_y = (
                            Text(
                                str(op[0][1]+1), 
                                font="DejaVu Sans Condensed", 
                                weight=SEMIBOLD, 
                                font_size=30
                                )
                            .next_to(col_text,RIGHT,buff=0.15)
                            .align_to(row_value,UP)
                        )
                        self.play(Transform(self.row_col_group[-1], replacement_y))
                        self.row_col_group[-1].become(replacement_y)

                    # Highlight while loop_y <= matrix_size:
                    self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins],
                              self.sliding_wins[2].animate.set_opacity(0.3))
                    self.wait(0.15)
                    self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins], 
                              self.sliding_wins[3].animate.set_opacity(0.3))
                    self.wait(0.1)

                    self.play(Create(bit_rect))
                    self.wait(0.15)
                    self.play(FadeOut(dBitMatrix.get_rows()[update[0]][update[1]]), run_time=0.5)
                    new_obj = (
                        dBitMatrix
                        .get_rows()[update[0]][update[1]]
                        .become(
                            MathTex(str(update[2]))
                            .scale(0.6)
                            .move_to(dBitMatrix.get_rows()[update[0]][update[1]])
                        )
                    )
                    self.play(FadeIn(new_obj),run_time=0.5)

                    # loop_y += (loop_y & -loop_y)
                    self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins],
                              self.sliding_wins[4].animate.set_opacity(0.3))
                    

                    temp = self.math_animate(update[1], self.row_col_group[-1], self.row_col_group.get_center()+DOWN*0.75)
                    self.row_col_group[-1] = temp

                    self.play(big_tree[update[0]-1].animate.highlight(GREEN),
                            self.small_trees[update[0]-1][update[1]-1].animate.highlight(GREEN)
                            )
                    self.wait(0.15)
                    if update[1] + (update[1] & -(update[1])) > bit.matrix_size:
                        self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins], 
                                  self.sliding_wins[5].animate.set_opacity(0.3))
                        self.wait(0.15)
                        temp = self.math_animate(update[0], self.row_col_group[1], self.row_col_group.get_center()+DOWN*0.75)
                        self.row_col_group[1] = temp
                        self.play(*[highlight.animate.set_opacity(0) for highlight in self.sliding_wins])
                        self.wait(0.15)

                    previous_x = update[0]
            else:
                # Faster version that highlights everything at once
                if not shifted_objects:
                    # Shift all the objects 
                    self.play(FadeOut(codeblock), FadeOut(self.row_col_group))
                    self.play(
                        AnimationGroup(
                            big_tree.animate.shift(RIGHT*1), 
                            fenwick_mat_label.animate.shift(LEFT*0.7)
                        ),
                        MaintainPositionRelativeTo(self.small_trees, big_tree),
                        MaintainPositionRelativeTo(dBitMatrix, fenwick_mat_label),
                        MaintainPositionRelativeTo(base_mat_label, fenwick_mat_label),
                        MaintainPositionRelativeTo(base_mat, fenwick_mat_label),
                        MaintainPositionRelativeTo(base_rect, fenwick_mat_label),
                    )
                    shifted_objects = True

                for update in op[1]:
                    bit_rect = SurroundingRectangle(
                        dBitMatrix.get_rows()[update[0]][update[1]], 
                        color=GREEN, 
                        buff=0.1
                    )
                    bit_rects.append(bit_rect)
                    fadeout_bit_numbers.append(FadeOut(dBitMatrix.get_rows()[update[0]][update[1]], run_time=0.5))
                    big_unhighlights.append(big_tree[update[0]-1])
                    small_unhighlights.append(self.small_trees[update[0]-1][update[1]-1])
                    big_tree_batch_highlights.append(big_tree[update[0]-1].animate.highlight(GREEN))
                    small_tree_batch_highlights.append(self.small_trees[update[0]-1][update[1]-1].animate.highlight(GREEN))

                #self.play(*fadeout_bit_numbers)
                self.play(*fadeout_bit_numbers)
                for update in op[1]:
                    new_obj = (
                        dBitMatrix.get_rows()[update[0]][update[1]]
                        .become(
                            MathTex(str(update[2]))
                            .scale(0.6)
                            .move_to(dBitMatrix.get_rows()[update[0]][update[1]])
                        )
                    )
                    fadein_bit_numbers.append(FadeIn(new_obj, run_time=0.5))
                self.play(*[Create(rect) for rect in bit_rects],
                          *fadein_bit_numbers,
                          *big_tree_batch_highlights,
                          *small_tree_batch_highlights)
                self.wait(0.8)
            

            self.play(
                *[box.animate.unhighlight() for box in big_unhighlights],
                *[box.animate.unhighlight() for box in small_unhighlights],
                *[Uncreate(rect) for rect in bit_rects]
            )
            self.wait(0.15)
            self.play(Uncreate(base_rect))
            self.wait(0.15)