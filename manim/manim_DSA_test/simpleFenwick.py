from manim import *
from manim_dsa import *


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

class Test(Scene):
    def construct(self):
        array = [4,8,5,2,6,1,0,8]
        UPLEVEL = 1.3
        startArray = (
            MArray(array, style=MArrayStyle.BLUE)
            .add_indexes()
            .scale(0.7)
        )

        self.play(Create(startArray), run_time=3)
        self.play(startArray.animate.to_edge(UP))
        
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
            self.play(Create(box), Write(numText), run_time=0.5)

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

        self.play(
            Transform(boxes[1][0], newLevel), 
            FadeTransform(boxes[1][1], Text("12", stroke_width=3).move_to(newLevel.get_center()), stretch=False),
            #rate_func=linear,
            # run_time=0.6
        )

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

        self.play(
            Transform(boxes[3][0], newNewLevel),
            # FadeOut(boxes[3][1]),
            # FadeIn(Text("19", stroke_width=3).move_to(newNewLevel.get_center()))
            FadeTransform(boxes[3][1], Text("19", stroke_width=3).move_to(newNewLevel.get_center()), stretch=False),
            # rate_func=linear,
            # run_time=0.75
        )

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
        
        self.play(
            Transform(boxes[5][0], newNewNewLevel),
            FadeTransform(boxes[5][1], Text("7", stroke_width=3).move_to(newNewNewLevel.get_center()), stretch=False),
        )

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

        self.play(
            Transform(boxes[7][0], finalLevel),
            FadeTransform(boxes[7][1], Text("34", stroke_width=3).move_to(finalLevel.get_center()), stretch=False),
        )

        self.wait(1)

        self.play(*[i.animate.unhighlight() for i in startArray])
    
    def moveNumBox(self, box, direction, amount):
        self.play(
            box[0].animate.shift(direction*amount),
            box[1].animate.shift(direction*amount)
        )