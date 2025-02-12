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
        fenwick_tree_arr = fenwick_tree.get_tree()
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
        
        boxes = []
        for num in array:
            box = Square(1).set_fill(BLUE, opacity=1)
            numText = (Text(str(num), stroke_width=3))

            boxes.append((box, numText))
            box_group.add(box)
            text_group.add(numText)

        # Aligning the boxes and text
        box_group.arrange()
        box_group.to_edge(DOWN)
        for i in range(len(boxes)):
            boxes[i][1].move_to(boxes[i][0].get_center())        


        self.play(Create(box_group,lag_ratio=0.1), Write(text_group, lag_ratio=0.1))

        plus = plus_sign(0, boxes)
        self.play(Write(plus),
                  startArray[0].animate.highlight(stroke_color=PINK),
                  startArray[1].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(2)]
                  )
        
        self.wait(0.5)
        self.play(Unwrite(plus),
                  *[highlight_box(boxes[i][0], BLUE) for i in range(2)]
                  )
      


        self.moveNumBox(boxes[1], UP, UPLEVEL)


        sumBox1 = (
            Rectangle(height=1, width=2.27) # 2.27 is the width of 2 square with the gap
            .align_to(boxes[0][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL)
            .set_fill(BLUE, opacity=1)
        )
        
        # integer = Integer(number=4).scale(1.8)
        # self.add(integer)

                

        sumText = Text(str(fenwick_tree.sum(1)), stroke_width=3).move_to(sumBox1.get_center())
        self.play(
            Transform(boxes[1][0], sumBox1), 
            FadeTransform(boxes[1][1], sumText, stretch=False),
            #rate_func=linear,
            # run_time=0.6
        )
        boxes[1] = (boxes[1][0], sumText)

        # self.play(
        #     startArray[0].animate.unhighlight(),
        #     startArray[1].animate.unhighlight(),
        # )

        sumBox2 = (
            Rectangle(height=1, width=2.27*2+0.23)
            .align_to(boxes[1][0].get_left(), LEFT)
            .to_edge(DOWN)
            .shift(UP*UPLEVEL*2)
            .set_fill(BLUE, opacity=1)
        )

        plus = plus_sign(2, boxes)
        plus2 = plus_sign_manual(sumBox1, 0)
        self.play(Write(plus),
                  Write(plus2),
                  startArray[2].animate.highlight(stroke_color=PINK),
                  startArray[3].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(1,4)]
                  )
        self.wait(0.5)
        self.play(Unwrite(plus), 
                  Unwrite(plus2), 
                  *[highlight_box(boxes[i][0], BLUE) for i in range(1,4)]
                  )

        self.moveNumBox(boxes[3], UP, UPLEVEL*2)

        sumText = Text(str(fenwick_tree.sum(3)), stroke_width=3).move_to(sumBox2.get_center())
        self.play(
            Transform(boxes[3][0], sumBox2),
            # FadeOut(boxes[3][1]),
            # FadeIn(Text("19", stroke_width=3).move_to(newNewLevel.get_center()))
            FadeTransform(boxes[3][1], sumText, stretch=False),
            # rate_func=linear,
            # run_time=0.75
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
        self.play(Write(plus),
                  startArray[4].animate.highlight(stroke_color=PINK),
                  startArray[5].animate.highlight(stroke_color=PINK),
                  *[highlight_box(boxes[i][0]) for i in range(4,6)]
                  )
        self.wait(0.5)
        self.play(Unwrite(plus),
                  *[highlight_box(boxes[i][0], BLUE) for i in range(4,6)]
                  )

        self.moveNumBox(boxes[5], UP, UPLEVEL)
        
        sumText = Text(str(fenwick_tree.range_sum(4,5)), stroke_width=3).move_to(sumBox3.get_center())
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
        self.play(Write(plus), 
                  Write(plus2), 
                  Write(plus3),
                  startArray[0].animate.highlight(stroke_color=PINK),
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
        self.play(Unwrite(plus), Unwrite(plus2), Unwrite(plus3),
                  *[highlight_box(boxes[i][0], BLUE) for i in range(0,8)]
                  )

        self.moveNumBox(boxes[7], UP, UPLEVEL*3)

        sumText = Text(str(fenwick_tree.sum(7)), stroke_width=3).move_to(sumBox4.get_center())
        self.play(
            Transform(boxes[7][0], sumBox4),
            FadeTransform(boxes[7][1], sumText, stretch=False),
        )
        boxes[7] = (boxes[7][0], sumText)

        self.wait(1)

        self.play(*[i.animate.unhighlight() for i in startArray])


        # QUERY PART

        self.play(startArray.animate.shift(RIGHT*2)) # Make room for text
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
    
    def moveNumBox(self, box, direction, amount):
        self.play(
            box[0].animate.shift(direction*amount),
            box[1].animate.shift(direction*amount)
        )