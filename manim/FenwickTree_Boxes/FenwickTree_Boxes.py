from manim import *
from manim_dsa import *
from bit_ds import BIT as FenwickTree


def plus_sign(boxnum, boxes):
    plus = Text("+", stroke_width=3)
    plus.z_index = 1
    box = boxes[boxnum][0]
    plus.move_to(box.get_center()+RIGHT*((box.width/2)+0.135)+UP*(box.height/2+0.135))
    return plus

def plus_sign_manual(box, elevate):
    plus = Text("+", stroke_width=3)
    plus.z_index = 1
    plus.move_to(box.get_center()+RIGHT*(box.width/2+0.27)+UP*elevate)
    return plus

def updateArrayValue(array: MArray, index: int, newValue: int) -> Text:
    oldIndex = array.submobjects[index+1].submobjects[1]
    newIndex = (
        Text(str(int(oldIndex.text)+newValue),
             font=oldIndex.font,
             font_size=oldIndex.font_size,
             stroke_width=oldIndex.stroke_width,
             weight=oldIndex.weight
        )
        .match_style(oldIndex)
        .move_to(oldIndex)
    )
    return newIndex

def highlight_box(box: Square, color: str = PINK):
    return box.animate.set_fill(color, opacity=1)
    

def updateBoxValue(text: Text, newValue: int) -> Text:
    newText = (
        Text(str(int(text.text)+newValue),
             font=text.font,
             font_size=text.font_size,
             stroke_width=text.stroke_width,
             weight=text.weight
        )
        .match_style(text)
        .move_to(text)
    )
    return newText

class Test(Scene):
    def construct(self):
        array = [4,8,5,2,6,1,0,8]
        fenwick_tree = FenwickTree(array)
        fenwick_tree_arr = fenwick_tree.tree

        UPLEVEL = 1.3
        startArray = (
            MArray(array, style=MArrayStyle.BLUE)
            .add_indexes()
            .scale(0.7)
        )

        self.play(Create(startArray), run_time=3)
        self.play(startArray.animate.to_edge(UP))

        # Using groups to draw using lag ratio delete after
        box_group = VGroup()
        text_group = VGroup()
        index_group = VGroup()
        
        boxes = []
        for i, num in enumerate(array):
            box = Square(1).set_fill(BLUE, opacity=1)
            numText = (Text(str(num), stroke_width=3))
            indexText = Text(str(i+1), color=BLUE, font_size=25)

            boxes.append((box, numText))
            box_group.add(box)
            text_group.add(numText)
            index_group.add(indexText)

        # Aligning the boxes and text
        box_group.arrange()
        box_group.to_edge(DOWN)
        for i in range(len(boxes)):
            boxes[i][1].move_to(boxes[i][0].get_center())
            index_group[i].move_to(boxes[i][0].get_bottom()).shift(DOWN*0.27)


        self.play(Create(box_group,lag_ratio=0.1), Write(text_group, lag_ratio=0.1), Write(index_group, lag_ratio=0.1))

        plus = plus_sign(0, boxes)
        self.play(FadeIn(plus),run_time=0.25)
        self.play(
                  startArray[0].animate.highlight(stroke_color=PINK),
                  startArray[1].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(2)]
                  )
        
        self.wait(0.5)
        self.play(FadeOut(plus),run_time=0.25)
        self.play(*[highlight_box(boxes[i][0], BLUE) for i in range(2)])
      
        self.moveNumBox(boxes[1], UP, UPLEVEL, index_group[1])

        sumBox1 = (
            Rectangle(height=1, width=2.27) # 2.27 is the width of 2 square with the gap
            .align_to(boxes[0][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL)
            .set_fill(BLUE, opacity=1)
        )       

        sumText = Text(str(fenwick_tree.sum(1)), stroke_width=3).move_to(sumBox1.get_center())
        self.play(
            Transform(boxes[1][0], sumBox1), 
            FadeTransform(boxes[1][1], sumText, stretch=False),
        )
        boxes[1] = (boxes[1][0], sumText)

        sumBox2 = (
            Rectangle(height=1, width=2.27*2+0.23)
            .align_to(boxes[1][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL*2)
            .set_fill(BLUE, opacity=1)
        )

        plus = plus_sign(2, boxes)
        plus2 = plus_sign_manual(sumBox1, 0)
        self.play(FadeIn(plus), FadeIn(plus2), run_time=0.25)
        self.play(startArray[2].animate.highlight(stroke_color=PINK),
                  startArray[3].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(1,4)]
                  )
        self.wait(0.5)
        self.play(FadeOut(plus), FadeOut(plus2), run_time=0.25)
        self.play(*[highlight_box(boxes[i][0], BLUE) for i in range(1,4)])

        self.moveNumBox(boxes[3], UP, UPLEVEL*2, index_group[3])

        sumText = Text(str(fenwick_tree.sum(3)), stroke_width=3).move_to(sumBox2.get_center())
        self.play(
            Transform(boxes[3][0], sumBox2),
            FadeTransform(boxes[3][1], sumText, stretch=False),
        )
        boxes[3] = (boxes[3][0], sumText)

        sumBox3 = (
            Rectangle(height=1, width=2.27)
            .align_to(boxes[4][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL)
            .set_fill(BLUE, opacity=1)
        )

        self.play(startArray[0].animate.unhighlight(),
                  startArray[1].animate.unhighlight(),
                  startArray[2].animate.unhighlight(),
                  startArray[3].animate.unhighlight())

        plus = plus_sign(4, boxes)
        self.play(FadeIn(plus), run_time=0.25)
        self.play(startArray[4].animate.highlight(stroke_color=PINK),
                  startArray[5].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(4,6)]
                  )
        self.wait(0.5)
        self.play(FadeOut(plus), run_time=0.25)
        self.play(*[highlight_box(boxes[i][0], BLUE) for i in range(4,6)])

        self.moveNumBox(boxes[5], UP, UPLEVEL, index_group[5])
        
        sumText = Text(str(fenwick_tree_arr[6]), stroke_width=3).move_to(sumBox3.get_center())
        self.play(
            Transform(boxes[5][0], sumBox3),
            FadeTransform(boxes[5][1], sumText, stretch=False),
        )
        boxes[5] = (boxes[5][0], sumText)

        sumBox4 = (
            Rectangle(height=1, width=2.27*4+0.23*3)
            .align_to(boxes[0][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL*3)
            .set_fill(BLUE, opacity=1)
        )

        plus = plus_sign(6, boxes)
        plus2 = plus_sign_manual(sumBox2, 0)
        plus3 = plus_sign_manual(sumBox3, 0)
        self.play(FadeIn(plus), FadeIn(plus2), FadeIn(plus3), run_time=0.25)
        self.play(startArray[0].animate.highlight(stroke_color=PINK),
                  startArray[1].animate.highlight(stroke_color=PINK),
                  startArray[2].animate.highlight(stroke_color=PINK),
                  startArray[3].animate.highlight(stroke_color=PINK),
                  startArray[6].animate.highlight(stroke_color=PINK),
                  startArray[7].animate.highlight(stroke_color=PINK),
                  highlight_box(boxes[3][0]),
                  highlight_box(boxes[5][0]),
                  highlight_box(boxes[-1][0]),
                  )
        self.wait(0.5)
        self.play(FadeOut(plus), FadeOut(plus2), FadeOut(plus3), run_time=0.25)
        self.play(*[highlight_box(boxes[i][0], BLUE) for i in range(0,8)])

        self.moveNumBox(boxes[7], UP, UPLEVEL*3, index_group[7])

        sumText = Text(str(fenwick_tree.sum(7)), stroke_width=3).move_to(sumBox4.get_center())
        self.play(
            Transform(boxes[7][0], sumBox4),
            FadeTransform(boxes[7][1], sumText, stretch=False),
        )
        boxes[7] = (boxes[7][0], sumText)

        self.wait(1)

        self.play(*[i.animate.unhighlight() for i in startArray])

        """
        QUERY PART 
        """

        self.play(startArray.animate.shift(RIGHT*2)) # Make room for text
        queryText = Text("")
        resultText = Text("")
        lines = []
        for i in range(array.__len__()):
            queryText.become(Text(f"Query: SUM({i})", font_size=44).to_edge(UP*1.2 + LEFT).shift(LEFT*0.24))
            self.play(Write(queryText))
            self.wait(0.5)


            highlight_indices = []
            z = i + 1
            while z > 0:
                highlight_indices.append(z)
                z -= -z & z

            
            line = Line(startArray[0].get_bottom()+DOWN*0.2 + LEFT * (startArray[0].width/2),
            startArray[i].get_bottom()+DOWN*0.2 + RIGHT * (startArray[i].width/2))
            line.set_color(PINK)
            line.set_stroke(width=5)
            lines.append(line)
            self.play(startArray[i].animate.highlight(stroke_color=PINK),
                      Create(line))
            
            self.wait(0.5)
            numbers = [boxes[j-1][1].text for j in highlight_indices]
            numbers.reverse()
            resultText.become(Text("+".join(numbers), font_size=44))
            resultText.align_to(queryText.get_bottom(), UP).align_to(queryText.get_left(), LEFT).shift(DOWN*0.2)
            
            self.play(
                        *[boxes[j-1][0].animate.set_fill(BLUE, opacity=1) for j in range(len(boxes))],
                        *[boxes[j-1][0].animate.set_fill(PINK, opacity=1) for j in highlight_indices],
                        Write(resultText, lag_ration=0.2)
                    )
            self.wait(0.5)
            resultSumText = Text("")
            if len(numbers) > 1:
                result = sum(map(int, numbers))
                resultSumText.become(Text(f"= {result}", font_size=44).align_to(resultText.get_right(), LEFT).align_to(resultText.get_bottom(), DOWN).shift(RIGHT*0.27))
            self.play(
                Write(resultSumText)
            )
            self.wait(0.75)
            self.play(Unwrite(queryText), Unwrite(resultText), Unwrite(resultSumText))
            self.wait(0.3)


        for l in lines:
            self.remove(l)
       
        # Query clean up
        self.play(
            *[i.animate.unhighlight() for i in startArray],
            boxes[-1][0].animate.set_fill(BLUE, opacity=1),
            FadeOut(line)
        )

        """
        Update part vvv
        """
        updateText = (
            Text("Update(2, 3)")
            .to_edge(UP*2+RIGHT*-0.1)
        )
        self.play(Write(updateText))

        newIndex = updateArrayValue(startArray, 2, 3)
        self.play(startArray[2].animate.highlight(stroke_color=PINK))
        self.play(Unwrite(startArray.submobjects[3].submobjects[1]))
        self.wait(0.3)
        self.play(Write(newIndex))

        self.play(boxes[2][0].animate.set_fill(PINK))
        self.play(Unwrite(boxes[2][1]))
        newIndex = updateBoxValue(boxes[2][1], 3)
        self.wait(0.3)
        self.play(Write(Text(newIndex.text, stroke_width=3).move_to(boxes[2][0].get_center())))
        
        self.play(boxes[3][0].animate.set_fill(PINK, opacity=1))
        self.play(Unwrite(boxes[3][1]))
        newIndex = updateBoxValue(boxes[3][1], 3)
        self.wait(0.3)
        self.play(Write(Text(newIndex.text, stroke_width=3).move_to(boxes[3][0].get_center())))

        self.play(boxes[-1][0].animate.set_fill(PINK, opacity=1))
        self.play(Unwrite(boxes[-1][1]))
        newIndex = updateBoxValue(boxes[-1][1], 3)
        self.wait(0.3)
        self.play(Write(Text(newIndex.text, stroke_width=3).move_to(boxes[-1][0].get_center())))
        self.wait(2)
        self.play(
            Unwrite(updateText),
            startArray[2].animate.unhighlight(),
            boxes[2][0].animate.set_fill(BLUE),
            boxes[3][0].animate.set_fill(BLUE),
            boxes[-1][0].animate.set_fill(BLUE),
        ) # Clean up
        self.wait(1)

        fenwick_tree.update(2, 3)

        """
        Range Query
        """
        startRange = 3
        endRange = 6
        rangeText = (
            Text(f"Range query({startRange}, {endRange})")
            .scale(0.75)
            .to_corner(UL)
            .shift(LEFT*0.2)
        )
        self.play(Write(rangeText))

        # End query
        endQueryText = (
            Text(f"Query: Sum({endRange})")
            .scale(0.6)
            .move_to(rangeText.get_left(), LEFT)
            .shift(DOWN*0.6)
        )
        self.play(Write(endQueryText))

        highlight_indices = []
        z = endRange + 1
        while z > 0:
            highlight_indices.append(z)
            z -= -z & z
        
        self.play(
            *[boxes[j-1][0].animate.set_fill(PINK, opacity=1) for j in highlight_indices],
        )

        endResultEqual = (
            Text("=")
            .scale(0.6)
            .move_to(endQueryText.get_right(), LEFT)
            .shift(RIGHT*0.2+UP*0.03)
        )

        endResultText = (
            Text(f"{fenwick_tree.sum(endRange)}")
            .scale(0.6)
            .move_to(endResultEqual.get_right(), LEFT)
            .shift(RIGHT*0.2+UP*0.03)
        )
        self.play(
            AnimationGroup(
                Write(endResultEqual),
                Write(endResultText),
                lag_ratio=0.3
            )
        )
        
        self.play(
            *[boxes[j-1][0].animate.set_fill(BLUE, opacity=1) for j in range(len(boxes))],
        )
        self.wait(1)

        # Start query
        startQueryText = (
            Text(f"Query: Sum({startRange-1})")
            .scale(0.6)
            .move_to(endQueryText.get_left(), LEFT)
            .shift(DOWN*0.5)
        )
        self.play(Write(startQueryText))

        highlight_indices = []
        z = startRange
        while z > 0:
            highlight_indices.append(z)
            z -= -z & z
        
        self.play(
            *[boxes[j-1][0].animate.set_fill(PINK, opacity=1) for j in highlight_indices],
        )

        startResultEqual = (
            Text("=")
            .scale(0.6)
            .move_to(startQueryText.get_right(), LEFT)
            .shift(RIGHT*0.2+UP*0.03)
        )

        startResultText = (
            Text(f"{fenwick_tree.sum(startRange-1)}")
            .scale(0.6)
            .move_to(startResultEqual.get_right(), LEFT)
            .shift(RIGHT*0.2)
        )
        self.play(
            AnimationGroup(
                Write(startResultEqual),
                Write(startResultText),
                lag_ratio=0.2
            )
        )

        self.play(
            *[boxes[j-1][0].animate.set_fill(BLUE, opacity=1) for j in range(len(boxes))],
        )
        self.wait(1)

        # Calculate Result
        self.play(
            FadeOut(endQueryText),
            FadeOut(endResultEqual),
            FadeOut(startQueryText),
            FadeOut(startResultEqual),
        )
        self.play(
            startResultText.animate.shift(LEFT*2.5),
            endResultText.animate.shift(LEFT*2.5)
        )

        minusText = (
            Text("-")
            .scale(0.6)
            .move_to(startResultText.get_left()+LEFT*0.1, RIGHT)
        )
        mathLine = (
            Line(startResultText.get_left()+LEFT*0.3, startResultText.get_right())
            .shift(DOWN*0.3)
        )
        self.wait(0.5)
        self.play(
            FadeIn(minusText),
            FadeIn(mathLine)
        )

        sumText = (
            Text(str(fenwick_tree.sum(endRange) - fenwick_tree.sum(startRange-1)))
            .scale(0.6)
            .move_to(startResultText.get_right(), RIGHT)
            .shift(DOWN*0.6)
        )
        self.play(Write(sumText))
        self.wait(1)

        # Final result
        rangeResultText = (
            Text(f"= {fenwick_tree.sum(endRange) - fenwick_tree.sum(startRange-1)}")
            .scale(0.75)
            .move_to(rangeText.get_right(), LEFT)
            .shift(RIGHT*0.28+UP*0.04)
        )
        self.play(
            Write(rangeResultText), 
            FadeOut(endResultText),
            FadeOut(startResultText),
            FadeOut(mathLine),
            FadeOut(sumText),
            FadeOut(minusText)
        )
        self.wait(2)
        self.play(
            AnimationGroup(
                Unwrite(rangeResultText),
                Unwrite(rangeText),
                lag_ratio=0.5
            )
        )

        self.wait(3)
    
    def moveNumBox(self, box, direction, amount, index):
        temp = VGroup()
        temp.add(box[0])
        temp.add(box[1])
        animation = AnimationGroup(temp.animate.shift(direction*amount), index.animate.shift(direction*amount), lag_ratio=0.45)
        self.play(animation)
