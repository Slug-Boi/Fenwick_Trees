from manim import *
from manim_dsa import *
from heapq import *
global_font = "DejaVu Sans Condensed"
arr = [3, 2, -3, 6, 5, 4, -2, 7]


class FenwickTree_Tree(Scene):
       def construct(self):
        UPLEVEL = 2
        heapify(arr)

        edges = {}

        for i in range(len(arr)):
            if i == 0:
                continue
            parent = (i - 1) // 2
            edges[i] = parent
            child1 = 2 * i + 1
            child2 = 2 * i + 2
            if child1 < len(arr):
                edges[child1] = i
            if child2 < len(arr):
                edges[child2] = i
                

        

        graph = MGraph(arr, edges, vertex_config={"radius": 0.3, "color": BLUE},)
        graph.move_to(ORIGIN)
        graph.scale(0.5)
        self.add(graph)
        self.wait(0.5)

        # Add edges
        for edge in edges:
            start = graph.vertices[edge[0]].get_center()
            end = graph.vertices[edge[1]].get_center()
            line = Line(start, end, color=WHITE)
            self.add(line)
            self.wait(0.5)


    
