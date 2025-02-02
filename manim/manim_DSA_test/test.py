from manim import *
from manim_dsa import *


class Example(Scene):
    def construct(self):
        graph = {
            'A': [('C', 11), ('D', 7)],
            'B': [('A', 5),  ('C', 3)],
            'C': [('A', 11), ('B', 3)],
            'D': [('A', 7),  ('C', 4)],
        }
        nodes_and_positions = {
            'A': LEFT * 1.5,
            'B': UP * 2,
            'C': RIGHT * 1.5,
            'D': DOWN * 2,
        }

        mArray = (
            MArray([1, 2, 3], style=MArrayStyle.BLUE)
            .add_indexes()
            .scale(0.9)
            .add_label(Text("Array", font="Cascadia Code"))
            .to_edge(LEFT, 1)
        )

        mStack = (
            MStack([3, 7, 98, 1], style=MStackStyle.GREEN)
            .scale(0.8)
            .add_label(Text("Stack", font="Cascadia Code"))
            .move_to(ORIGIN)
        )

        mGraph = (
            MGraph(graph, nodes_and_positions, MGraphStyle.PURPLE)

            .add_label(Text("Graph", font="Cascadia Code"))
            .to_edge(RIGHT, 1)
        )

        self.play(Create(mArray))
        self.play(Create(mStack))
        self.play(Create(mGraph))
        self.wait()
