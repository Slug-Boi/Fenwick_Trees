from manim import *
from manim_dsa import *
from fenwick_tree import FenwickTree
from copy import deepcopy


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
        fenwick_tree_arr = fenwick_tree.get_tree()
        UPLEVEL = 1.3
        startArray = (
            MArray(array, style=MArrayStyle.BLUE)
            .add_indexes()
            .scale(0.7)
        )

        self.play(Create(startArray), run_time=3)
        self.play(startArray.animate.to_edge(UP))

        box_group = VGroup()
        text_group = VGroup()
        
        boxes = []
        for num in array:
            box = Square(1).set_fill(BLUE, opacity=1)
            if len(boxes) <= 0:
                box.to_edge(DOWN).to_edge(LEFT)
            else:
                box.next_to(boxes[-1][0])
            numText = (
                Text(str(num), stroke_width=3)
                .move_to(box.get_center())
            )
            boxes.append((box, numText))
            box_group.add(box)
            text_group.add(numText)

        self.play(Create(box_group,lag_ratio=0.1), Write(text_group, lag_ratio=0.1))

        plus = plus_sign(0, boxes)
        self.play(Write(plus),
                  startArray[0].animate.highlight(stroke_color=PINK),
                  startArray[1].animate.highlight(stroke_color=PINK)
                  )
        self.wait(0.5)
        self.play(Unwrite(plus))

        self.moveNumBox(boxes[1], UP, UPLEVEL)

        newLevel = (
            Rectangle(height=1, width=2.27) # 2.27 is the width of 2 square with the gap
            .to_edge(LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL)
            .set_fill(BLUE, opacity=1)
        )
        
        # integer = Integer(number=4).scale(1.8)
        # self.add(integer)

        newText = Text(str(fenwick_tree.sum(1)), stroke_width=3).move_to(newLevel.get_center())
        self.play(
            Transform(boxes[1][0], newLevel), 
            FadeTransform(boxes[1][1], newText, stretch=False),
            #rate_func=linear,
            # run_time=0.6
        )
        boxes[1] = (boxes[1][0], newText)

        # self.play(
        #     startArray[0].animate.unhighlight(),
        #     startArray[1].animate.unhighlight(),
        # )

        newNewLevel = (
            Rectangle(height=1, width=2.27*2+0.23)
            .to_edge(LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL*2)
            .set_fill(BLUE, opacity=1)
        )

        plus = plus_sign(2, boxes)
        plus2 = plus_sign_manual(newLevel, 0)
        self.play(Write(plus),
                  Write(plus2),
                  startArray[2].animate.highlight(stroke_color=PINK),
                  startArray[3].animate.highlight(stroke_color=PINK)
                  )
        self.wait(0.5)
        self.play(Unwrite(plus), Unwrite(plus2))

        self.moveNumBox(boxes[3], UP, UPLEVEL*2)

        newText = Text(str(fenwick_tree.sum(3)), stroke_width=3).move_to(newNewLevel.get_center())
        self.play(
            Transform(boxes[3][0], newNewLevel),
            # FadeOut(boxes[3][1]),
            # FadeIn(Text("19", stroke_width=3).move_to(newNewLevel.get_center()))
            FadeTransform(boxes[3][1], newText, stretch=False),
            # rate_func=linear,
            # run_time=0.75
        )
        boxes[3] = (boxes[3][0], newText)

        newNewNewLevel = (
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
        self.play(Write(plus),
                  startArray[4].animate.highlight(stroke_color=PINK),
                  startArray[5].animate.highlight(stroke_color=PINK)
                  )
        self.wait(0.5)
        self.play(Unwrite(plus))

        self.moveNumBox(boxes[5], UP, UPLEVEL)
        
        newText = Text(str(fenwick_tree.range_sum(4,5)), stroke_width=3).move_to(newNewNewLevel.get_center())
        self.play(
            Transform(boxes[5][0], newNewNewLevel),
            FadeTransform(boxes[5][1], newText, stretch=False),
        )
        boxes[5] = (boxes[5][0], newText)

        finalLevel = (
            Rectangle(height=1, width=2.27*4+0.23*3)
            .to_edge(LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL*3)
            .set_fill(BLUE, opacity=1)
        )

        plus = plus_sign(6, boxes)
        plus2 = plus_sign_manual(newNewLevel, 0)
        plus3 = plus_sign_manual(newNewNewLevel, 0)
        self.play(Write(plus), 
                  Write(plus2), 
                  Write(plus3),
                  startArray[0].animate.highlight(stroke_color=PINK),
                  startArray[1].animate.highlight(stroke_color=PINK),
                  startArray[2].animate.highlight(stroke_color=PINK),
                  startArray[3].animate.highlight(stroke_color=PINK),
                  startArray[6].animate.highlight(stroke_color=PINK),
                  startArray[7].animate.highlight(stroke_color=PINK)
                  )
        self.wait(0.5)
        self.play(Unwrite(plus), Unwrite(plus2), Unwrite(plus3))

        self.moveNumBox(boxes[7], UP, UPLEVEL*3)

        newText = Text(str(fenwick_tree.sum(7)), stroke_width=3).move_to(finalLevel.get_center())
        self.play(
            Transform(boxes[7][0], finalLevel),
            FadeTransform(boxes[7][1], newText, stretch=False),
        )
        boxes[7] = (boxes[7][0], newText)

        self.wait(1)

        self.play(*[i.animate.unhighlight() for i in startArray])


        # QUERY PART
        queryText = Text("")
        lines = []
        #self.play(Write(queryText))
        for i in range(array.__len__()):
            queryText.become(Text(f"Query: SUM({i})").to_edge(UP*2+RIGHT*-0.1).scale(0.85))
            # Find a prettier way of doing this
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

            self.play(*[boxes[j-1][0].animate.set_fill(BLUE, opacity=1) for j in range(len(boxes))],
                      *[boxes[j-1][0].animate.set_fill(PINK, opacity=1) for j in highlight_indices],
                      )
            
            self.play(Unwrite(queryText))


        for l in lines:
            self.remove(l)
        # Plus 2 is magick number i have no clue
        #self.play(*[i.animate.highlight(stroke_color=PINK) for i in startArray.submobjects[:query+2]])

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
            .to_edge(UP)
            .to_edge(LEFT)
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
    
    def moveNumBox(self, box, direction, amount):
        self.play(
            box[0].animate.shift(direction*amount),
            box[1].animate.shift(direction*amount)
        )