from pathlib import Path
from twoDBit import TwoDBIT
from manim import *
from box_tree import *                
from fenwick_tree import FenwickTree
from copy import deepcopy



class QueryUpdateTwoDBIT(Scene):
    def construct(self):
        M2 = [
                [3,  4,  0, 2],
                [8,  11, 10, 3],
                [9,  7,  5, 8],
                [6,  2,  1, 2],
            ]
        bit = TwoDBIT(M2, 4)
        bit.Create()
        bit.PrintBit()

        test = [2, 1, 4, 1, 0, 8, 10, 2]

        small_tree_style = deepcopy(BoxTree.defaultStyle)
        small_tree_style["rect"]["height"] = 0.25
        small_trees = VGroup()
        for i in range(len(M2)):
            small_trees.add(
                BoxTree(
                    [0 for _ in range(len(M2[i]))], 
                    style=small_tree_style, 
                    show_indices=True, 
                    show_values=False
                )
                .create()
                .scale(0.75)
            )

        small_trees.arrange(UP, buff=1)
        self.play(LaggedStart(*[FadeIn(tree) for tree in small_trees], lag_ratio=0.5), run_time=0.7)
        self.wait(0.75)

        big_tree_style = deepcopy(BoxTree.defaultStyle)
        big_tree_style['x_buffer'] = 1.01
        #(small_trees[1].get_center() - small_trees[0].get_center())[1] - big_tree_style["rect"]["height"]*2
        big_tree_style["y_buffer"] = 0.4
        big_tree_style["rect"]["height"] = 0.35
        big_tree_style["rect"]["width"] = small_trees[0].get_height()

        big_tree = (
            BoxTree(
                [0 for _ in range(len(M2))], 
                show_indices=True, 
                show_values=False, 
                style=big_tree_style
            )
            .create()
            .rotate(PI/2)
            .move_to(small_trees.get_corner(DL),DR)
            .shift(LEFT*0.3)
        )
        self.play(FadeIn(big_tree), run_time=0.7)
        self.play(big_tree.animate.to_edge(LEFT).shift(RIGHT*0.2), run_time=0.7)
        self.play(small_trees.animate.move_to(big_tree.get_corner(DR),DL).shift(RIGHT*0.3), run_time=0.7)
        self.wait(2)

        fenwick_mat_label = (
            Text(
                "BIT Table", 
                weight=SEMIBOLD, 
                font="DejaVu Sans Condensed", 
                font_size=36
            )
            .to_corner(UR)
            .shift(LEFT*1.2)
        )
        dBitMatrix = (
            Matrix(bit.BIT)
            .scale(0.7)
            .move_to(fenwick_mat_label.get_bottom(),UP)
            .shift(DOWN*0.2)
        )
        self.play(
            AnimationGroup(
                Write(fenwick_mat_label),
                Create(dBitMatrix),
                lag_ratio=0.2
            )
        )
        self.wait(0.5)

        base_mat_label = (
            Text(
                "Input Table", 
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
            AnimationGroup(
                Write(base_mat_label), 
                Create(base_mat), 
                lag_ratio=0.2
            )
        )
        self.wait(0.5)

        """
        QUERY START
        """

        # Prepare the mother of all text objects...
        fullQuery = (
            Text(
                "Query(2,1)", 
                font="DejaVu Sans Condensed", 
                font_size=36, 
                weight=SEMIBOLD
            )
            .to_edge(UP)
            .shift(DOWN*0.3+LEFT*0.2)
        )
        queryText = (
            Text(
                "Sub-Query: (", 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .to_edge(UP)
            .shift(DOWN*1.5+LEFT*0.8)
        )
        comma = (
            Text(
                ",", 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .next_to(queryText,RIGHT)
        )
        endPar = (
            Text(
                ")", 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .next_to(comma,RIGHT)
        )
        partialSums = (
            Text(
                "Partial Sums: [", 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .move_to(queryText.get_bottom(),UP)
            .align_to(queryText,LEFT)
            .shift(DOWN*0.4)
        )
        endBracket = (
            Text(
                "]", 
                font="DejaVu Sans Condensed", 
                font_size=30
            )
            .next_to(partialSums,RIGHT)
        )


        # Write static text items 
        ops = bit.getSumPositions(2, 1)
        self.play(Write(fullQuery),Write(queryText), Write(endPar))
        self.wait(0.25)
        self.play(Write(partialSums), Write(endBracket))

        # Create bounding rect in the base matrix
        
        rows = [item for sublist in [base_mat.get_mob_matrix()[i][0:2] for i in range(0, 3)] for item in sublist]
        area_base_rect = SurroundingRectangle(*rows, color=GREEN, buff=0.1)
        self.play(Create(area_base_rect))
        self.wait(0.25)       

        sums_list = [] 
        comma_list = []
        x, y = None, None

        for query in ops[1]:
            animations = []
            if x is not None and y is not None:
                # Cleanup for next run
                self.play(FadeOut(rect_highlight), FadeOut(x), FadeOut(y))

            x = (
                Text(
                    str(query[0]), 
                    font="DejaVu Sans Condensed", 
                    font_size=30
                )
                .next_to(queryText,RIGHT,buff=0.15)
            )
            animations.append(Write(x))

            animations.append(
                Write(comma.next_to(x,RIGHT,buff=0.15).align_to(x,DOWN)) if y is None else comma.animate.next_to(x,RIGHT,buff=0.15).align_to(x,DOWN)
            )

            y = (
                Text(
                    str(query[1]), 
                    font="DejaVu Sans Condensed", 
                    font_size=30
                )
                .next_to(comma,RIGHT,buff=0.15)
                .align_to(x,DOWN)
            )
            animations.append(Write(y))

            self.play(endPar.animate.next_to(y,RIGHT,buff=0.15))
            
            self.play(*animations)
            self.wait(0.5)

            # Create bounding rects in the Fenwick Tree matrix
            rect_highlight = SurroundingRectangle(
                dBitMatrix.get_mob_matrix()[query[0]][query[1]], 
                color=GREEN, 
                buff=0.1
            )
            self.play(Create(rect_highlight))

            # Highlight BIT value in the Fenwick Tree matrix
            self.play(
                big_tree[query[0]-1].animate.highlight(GREEN),
                small_trees[query[0]-1][query[1]-1].animate.highlight(GREEN),
                run_time=0.5
            )
            self.wait(0.25)

            # add sum to partial sums
            sumText = (
                Text(
                    str(query[2]), 
                    font="DejaVu Sans Condensed", 
                    font_size=30
                )
                .move_to(partialSums.get_center(),ORIGIN)
                .align_to(partialSums,RIGHT)
                .shift(RIGHT*0.58)
            )
            sums_list.append(sumText)

            # Pre-move the end bracket to the right of the sum text to avoid overlap but keep y alignment
            if len(sums_list) > 1:
                sumText.move_to(sums_list[-1].get_bottom(),UP).align_to(sums_list[-1],LEFT).shift(DOWN*0.2)
                comma_list.append(
                    Text(
                        ",", 
                        font="DejaVu Sans Condensed", 
                        font_size=30
                    )
                    .next_to(sums_list[-2],RIGHT,buff=0.15)
                    .align_to(sums_list[-2],DOWN)
                )
                self.play(
                    AnimationGroup(
                        endBracket.animate.next_to(sums_list[-1],RIGHT,buff=0.15)
                            .align_to(sums_list[-1],DOWN)
                            .shift(DOWN*0.05),
                        Write(comma_list[-1]), 
                        lag_ratio=0.6
                    )
                )
                self.play(Write(sumText))
            else:  
                self.play(endBracket.animate.next_to(sumText,RIGHT,buff=0.15).align_to(partialSums,DOWN))
                self.play(Write(sumText))

            self.wait(0.25)

            

        # Final cleanup and write sum
        finalSumText = (
            Text(
                "Sum: ", 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD,
                font_size=30
            )
            .move_to(sums_list[-1].get_bottom(),UP)
            .align_to(partialSums,LEFT)
            .shift(DOWN*0.9)
        )
        finalSum = (
            Text(
                str(ops[0]), 
                font="DejaVu Sans Condensed", 
                weight=SEMIBOLD, 
                font_size=30
            )
            .next_to(finalSumText,RIGHT,buff=0.15)
            .align_to(finalSumText,DOWN)
        )

        self.play(
            AnimationGroup(
                Write(finalSumText), 
                Write(finalSum), 
                lag_ratio=0.4
            )
        )
        self.wait(2)
        
        # Clean up
        self.play(Unwrite(fullQuery), 
                  Unwrite(queryText),
                  Unwrite(comma), 
                  Unwrite(x),
                  Unwrite(y),
                  Unwrite(endPar), 
                  Unwrite(partialSums), 
                  Unwrite(endBracket), 
                  Uncreate(area_base_rect), 
                  Uncreate(rect_highlight),
                  Unwrite(finalSumText), 
                  Unwrite(finalSum), 
                  *[Unwrite(sum) for sum in sums_list], 
                  *[Unwrite(comma) for comma in comma_list],
                  *[box.animate.unhighlight() for box in big_tree],
                  *[innerbox.animate.unhighlight() for box in small_trees for innerbox in box],
                  )
        self.wait(1.5)
        """
        QUERY END
        """