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
                "Fenwick Tree Matrix", 
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
            AnimationGroup(
                Write(fenwick_mat_label),
                Create(dBitMatrix),
                lag_ratio=0.2
            )
        )
        self.wait(0.5)

        base_mat_label = (
            Text(
                "Base Matrix", 
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
        RANGE QUERY START
        """

        # Prepare the mother of all text objects...
        position1 = (1,1)
        position2 = (3,2)
        fullQuery = (
            Text(
                f"Query({position1}, {position2})", 
                font="DejaVu Sans Condensed", 
                font_size=30, 
                weight=SEMIBOLD
            )
            .to_edge(UP)
            .shift(DOWN*0.5+LEFT*0.3)
        )
        # queryText = (
        #     Text(
        #         "Sub-Query: (", 
        #         font="DejaVu Sans Condensed", 
        #         font_size=30
        #     )
        #     .to_edge(UP)
        #     .shift(DOWN*1.5+LEFT*0.8)
        # )
        # comma = (
        #     Text(
        #         ",", 
        #         font="DejaVu Sans Condensed", 
        #         font_size=30
        #     )
        #     .next_to(queryText,RIGHT)
        # )
        # endPar = (
        #     Text(
        #         ")", 
        #         font="DejaVu Sans Condensed", 
        #         font_size=30
        #     )
        #     .next_to(comma,RIGHT)
        # )
        # partialSums = (
        #     Text(
        #         "Partial Sums: [", 
        #         font="DejaVu Sans Condensed", 
        #         font_size=30
        #     )
        #     .move_to(queryText.get_bottom(),UP)
        #     .align_to(queryText,LEFT)
        #     .shift(DOWN*0.4)
        # )
        # endBracket = (
        #     Text(
        #         "]", 
        #         font="DejaVu Sans Condensed", 
        #         font_size=30
        #     )
        #     .next_to(partialSums,RIGHT)
        # )


        # Write static text items 
        ops = bit.SquareSumPositions(position1, position2)
        result, ops = ops[0], ops[1:]
        self.play(Write(fullQuery))
        # ops = bit.getSumPositions(2, 1)
        # self.play(Write(fullQuery),Write(queryText), Write(endPar))
        # self.wait(0.25)
        # self.play(Write(partialSums), Write(endBracket))

        # Create bounding rect in the base matrix
        
        rows = [item for sublist in [base_mat.get_mob_matrix()[i][position1[1]:position2[1]+1] for i in range(position1[0], position2[0]+1)] for item in sublist]
        area_base_rect = SurroundingRectangle(*rows, color=GREEN, buff=0.1)
        self.play(Create(area_base_rect))
        self.wait(0.25)       
        squareColors = [BLUE, PINK, RED, YELLOW]
        subSquares = []
        subQueriesText = []
        for color, square in zip(squareColors, ops):
            # Create and write sub query text
            subQueryText = (
                Text(
                    f"Query({square[0], square[1]}) = ",
                    font="DejaVu Sans Condensed",
                    font_size = 30,
                    color=color,
                    stroke_color=color,
                )
            )
            if subQueriesText:
                subQueryText.next_to(subQueriesText[-1], DOWN)
                subQueryText.align_to(subQueriesText[-1], LEFT)
                # subQueryText.shift(RIGHT*0.1)
            else:
                subQueryText.next_to(fullQuery, DOWN)
                subQueryText.align_to(fullQuery, LEFT)
                subQueryText.shift(RIGHT*0.1)
            self.play(Write(subQueryText), run_time=0.85)
            self.wait(0.3)
            subQueriesText.append(subQueryText)

            # Create and draw input matrix square
            subQueryRows = [item for sublist in [base_mat.get_mob_matrix()[i][0:square[1]+1] for i in range(0, square[0]+1)] for item in sublist]
            subQuerySquare = SurroundingRectangle(*subQueryRows, color=color, buff=0.1)
            subSquares.append(subQuerySquare)
            self.play(Create(subQuerySquare))
            self.wait(0.5)

