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
        self.play(
            LaggedStart(
                *[FadeIn(tree) for tree in small_trees], 
                lag_ratio=0.5
            ), 
            run_time=0.7
        )
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
            # This has to use a f string. 
            # Otherwise manim can't combine the sub-renders 
            # into the full animation (for some reason)
            Text(
                "Fenwick Tree Table",
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


        # Write static text items 
        ops = bit.SquareSumPositions(position1, position2)
        result, ops = ops[0], ops[1:]
        self.play(Write(fullQuery))

        # Create bounding rect in the base matrix
        rows = [item for sublist in [base_mat.get_mob_matrix()[i][position1[1]:position2[1]+1] for i in range(position1[0], position2[0]+1)] for item in sublist]
        area_base_rect = SurroundingRectangle(*rows, color=WHITE, buff=0.1)
        self.play(Create(area_base_rect))
        self.wait(0.25)

        squareColors = [GREEN, PINK, RED, YELLOW]
        subSquares = []
        subQueriesText = []
        subQueryResults = []
        for color, square in zip(squareColors, ops):
            # Create and write sub query text
            subQueryText = (
                Text(
                    f"Query({square[0]}, {square[1]}) =",
                    font="DejaVu Sans Condensed",
                    font_size = 28,
                    color=color,
                    stroke_color=color
                )
            )
            if subQueriesText:
                subQueryText.next_to(subQueriesText[-1], DOWN)
                subQueryText.align_to(subQueriesText[-1], LEFT)
                # subQueryText.shift(RIGHT*0.1)
            else:
                subQueryText.next_to(fullQuery, DOWN)
                subQueryText.align_to(fullQuery, LEFT)
                subQueryText.shift(RIGHT*0.3)
            self.play(Write(subQueryText), run_time=0.85)
            self.wait(0.3)
            subQueriesText.append(subQueryText)

            # Create and draw input matrix square
            subQueryRows = [item for sublist in [base_mat.get_mob_matrix()[i][0:square[1]+1] for i in range(0, square[0]+1)] for item in sublist]
            subQuerySquare = SurroundingRectangle(*subQueryRows, color=color, buff=0.1)
            subSquares.append(subQuerySquare)
            self.play(Create(subQuerySquare))
            self.wait(0.5)
            
            # Batch show indecies used for sub-query
            _, sub_ops = bit.getSumPositions(square[0], square[1])
            matrixSquares = []
            treePosition = []
            for op in sub_ops:
                treePosition.append((big_tree[op[0]-1], small_trees[op[0]-1][op[1]-1]))
                item = dBitMatrix.get_mob_matrix()[op[0]][op[1]]
                matrixSquares.append(SurroundingRectangle(item, color=color, buff=0.1))
            self.play(
                *[Create(square) for square in matrixSquares],
                *[position[0].animate.highlight(color) for position in treePosition],
                *[position[1].animate.highlight(color) for position in treePosition]
                )
            self.wait(0.4)
            
            # Show result of sub query
            subQueryResult = (
                Text(
                    str(square[2]),
                    font=subQueryText.font,
                    font_size=subQueryText.font_size,
                    color=color,
                    stroke_color=color
                )
                .next_to(subQueryText, RIGHT, buff=0.19)
                .align_to(subQueryText, UP)
            )

            self.play(Write(subQueryResult), run_time=0.7)
            subQueryResults.append(subQueryResult)
            self.wait(0.5)
            
            # Clean up
            self.play(
                *[Uncreate(square) for square in matrixSquares],
                *[position[0].animate.unhighlight() for position in treePosition],
                *[position[1].animate.unhighlight() for position in treePosition]
            )
            self.wait(0.1)
        
        
        # Calculate final result
        resultText = (
            Text(
                "Result =",
                font="DejaVu Sans Condensed",
                font_size=28,
            )
            .next_to(subQueriesText[-1], DOWN, buff=1)
            .align_to(fullQuery, LEFT)
        )
        self.play(Write(resultText))
        self.wait(0.2)
        self.add(*[result.copy() for result in subQueryResults])
        
        # Move sub results into calculation

        separation = 0.17
        minus1 = Text("-", font="DejaVu Sans Condensed", font_size=28)
        self.play(
            (
                subQueryResults[0].animate
                .next_to(resultText, RIGHT, buff=separation)
                .align_to(resultText, DOWN)
            )
        )
        self.play(FadeIn(minus1.next_to(subQueryResults[0], RIGHT, buff=separation)))

        minus2 = minus1.copy()
        self.play(
            (
                subQueryResults[1].animate
                .next_to(minus1, RIGHT, buff=separation)
                .align_to(resultText, DOWN)
            )
        )
        self.play(FadeIn(minus2.next_to(subQueryResults[1], RIGHT, buff=separation)))

        plus = Text("+", font="DejaVu Sans Condensed", font_size=20)
        self.play(
            (
                subQueryResults[2].animate
                .next_to(minus2, RIGHT, buff=separation)
                .align_to(resultText, DOWN)
            )
        )
        self.play(FadeIn(plus.next_to(subQueryResults[2], RIGHT, buff=separation)))

        self.play(
            (
                subQueryResults[3].animate
                .next_to(plus, RIGHT, buff=separation)
                .align_to(resultText, DOWN)
            )
        )

        self.wait(0.5)
        # Colaps into final result
        finalResult = (
            Text(
                str(result),
                font=resultText.font,
                font_size=resultText.font_size,
                weight=resultText.weight
            )
            .next_to(resultText, RIGHT, buff=separation)
            .align_to(resultText, DOWN)
        )
        resultGroup = VGroup(
            subQueryResults[0],
            minus1,
            subQueryResults[1],
            minus2,
            subQueryResults[2],
            plus,
            subQueryResults[3]
        )
        self.play(FadeTransformPieces(resultGroup, finalResult))

        self.wait(3)
