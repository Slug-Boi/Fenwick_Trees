from manim import *
from manim_dsa import *
from heapq import *
from math import floor, log2
from copy import copy
global_font = "DejaVu Sans Condensed"
arr = [3, 2, -3, 6, 5, 4, -2, 7]

class FenwickTree_Tree(Scene):
    @staticmethod
    def getLevel(index):
        return floor(log2(index + 1))

    def construct(self):
        DOWNLEVEL = 2
        SIDELEVEL = 1.5
        originalArray = list(map(str, copy(arr)))
        heapify(arr)
        print(arr)
        edges = {}
        node_positions = dict()

        for i in range(len(arr)):
            if i == 0:
                node_positions[str(arr[0])] = UP*3.2
            else:
                level = self.getLevel(i)
                if level == 1:
                    level_adjust = 1.2
                else:
                    level_adjust = 1.5
                if i % 2 == 1:
                    node_positions[str(arr[i])] = node_positions[str(arr[i // 2])] + DOWN * DOWNLEVEL + LEFT * ((SIDELEVEL / level)*level_adjust)
                else:
                    node_positions[str(arr[i])] = node_positions[str(arr[(i-1) // 2])] + DOWN * DOWNLEVEL + RIGHT * ((SIDELEVEL / level) * level_adjust)
            parent = i
            child1 = 2 * i + 1
            child2 = 2 * i + 2
            edges[str(arr[parent])] = []
            if child1 < len(arr):
                edges[str(arr[parent])].append(str(arr[child1]))
            if child2 < len(arr):
                edges[str(arr[parent])].append(str(arr[child2]))

        print(edges)

        heapText = Text(
            "Min Binary Heap",
            weight=SEMIBOLD,
            # font=global_font
        ).to_corner(UL).scale(0.8)
        inputArrayText = Text(
            "Input: [" + ", ".join(originalArray) + "]",
        ).move_to(heapText.get_bottom(), UP).scale(0.5).align_to(heapText.get_left(), LEFT)

        self.play(Write(heapText))
        self.wait(0.2)

        self.play(Write(inputArrayText), run_time=0.7)
        self.wait(0.2)
        graph = MGraph(edges, nodes_position=node_positions, style=MGraphStyle.PURPLE)
        # graph.scale(0.5)
        self.play(Create(graph), run_time=1.5)
        self.wait(1)
        
        self.play(Unwrite(inputArrayText), run_time=0.7)
        self.wait(0.5)

        """
        Insert Animation
        """
        heapArrayText = Text(
            "Heap: [" + ", ".join(list(map(str, copy(arr)))) + "]"
        ).move_to(heapText.get_bottom(), UP).scale(0.5).align_to(heapText.get_left(), LEFT)
        self.play(Write(heapArrayText), run_time=0.7)

        insertText = Text(
            "Insert(1)"
        ).move_to(heapArrayText.get_bottom(),UP).scale(0.5).align_to(heapArrayText.get_left(), LEFT)
        self.play(Write(insertText), run_time=0.7)

        self.play(
            graph.animate.add_node(
                "1",
                # ORIGIN
                node_positions["6"] + DOWN * DOWNLEVEL + RIGHT * ((SIDELEVEL / 3) * 1.5)
            ),
            run_time = 0.7
        )
        self.play(
            graph.animate.add_edge(
                "6",
                "1"
            ),
            run_time = 0.7
        )
        self.wait(0.5)
        Text.become(graph[str(6)].submobjects[1], Text("1", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(6)].submobjects[1].get_bottom(), DOWN))
        Text.become(graph[str(1)].submobjects[1], Text("6", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(1)].submobjects[1].get_bottom(), DOWN))
        self.play(Write(graph[str(6)].submobjects[1]), Write(graph[str(1)].submobjects[1]))
        
        self.wait(0.7)
        Text.become(graph[str(2)].submobjects[1], Text("1", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(2)].submobjects[1].get_bottom(), DOWN))
        Text.become(graph[str(6)].submobjects[1], Text("2", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(6)].submobjects[1].get_bottom(), DOWN))
        self.play(Write(graph[str(6)].submobjects[1]), Write(graph[str(2)].submobjects[1]))
        self.wait(0.2)
        
        self.play(FadeOut(heapArrayText), run_time=0.7)
        heapArrayText.become(
            Text(
                "Heap: [" + ", ".join(list(map(str, copy((lambda: heapify((lambda: arr.append(1) or arr)()) or arr)())))) + "]"
            ).scale(0.5).move_to(heapArrayText.get_left(), LEFT)
        )
        self.play(FadeIn(heapArrayText), run_time=0.7)
        self.wait(0.7)
        self.play(FadeOut(insertText), run_time=0.7)

        self.wait(1.5)

        """
        Remove animation
        """
        removeText = Text(
            "Remove(-2)"
        ).move_to(heapArrayText.get_bottom(),UP).scale(0.5).align_to(heapArrayText.get_left(), LEFT)
        self.play(Write(removeText), run_time=0.7)
        self.wait(0.7)

        self.play(Unwrite(graph[str(-2)].submobjects[1]))
        self.wait(0.5)

        self.play(Unwrite(graph[str(1)].submobjects[1]), Uncreate(graph[str(1)]), FadeOut(graph.edges[("6", "1")]))
        self.wait(0.5)

        Text.become(graph[str(-2)].submobjects[1], Text("6", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(-2)].submobjects[1].get_bottom(), DOWN))
        self.play(Write(graph[str(-2)].submobjects[1]))
        self.wait(0.7)
        
        Text.become(graph[str(-2)].submobjects[1], Text("3", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(-2)].submobjects[1].get_bottom(), DOWN))
        Text.become(graph[str(3)].submobjects[1], Text("6", **MGraphStyle.DEFAULT.node_label).move_to(graph[str(3)].submobjects[1].get_bottom(), DOWN))
        self.play(Write(graph[str(-2)].submobjects[1]), Write(graph[str(3)].submobjects[1]))
        
        self.wait(0.7)

        self.play(FadeOut(removeText), run_time=0.7)

        self.wait(1.5)
    
