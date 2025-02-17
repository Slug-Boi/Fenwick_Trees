from manim import *
from manim_dsa import *
from manim_dsa.m_graph_generic.m_graph_generic import MGraphGeneric
from math import log2, ceil
from fenwick_tree import FenwickTree

def binary_index(index,b_len) -> str:
    return "{0:0{b_len}b}".format(index, b_len=b_len)

def tree_level(index) -> int:
    lsb = index & -index
    return int(log2(lsb))

class FenwickTree_Tree(Scene):
    def construct(self):
        UPLEVEL = 2

        # Create a Fenwick Tree
        arr = [3, 2, -3, 6, 5, 4, -2, 7]
        binary_len = ceil(log2(len(arr)+1))

        # fenwick tree
        fw = FenwickTree(arr)
        # Fenwick Tree Array
        fta = fw.get_tree()
        print(fta)
    
        dsa_arr = MArray(arr, margin=1.25, style=MArrayStyle.BLUE).scale(0.75).to_edge(DOWN)

        bin_indices = VGroup(*[Text(binary_index(i+1,binary_len), color=BLUE, stroke_width=0).scale(0.5) for i in range(len(arr))])

        for i, bi in enumerate(bin_indices):
            bi.move_to(dsa_arr[i].get_center()).align_to(dsa_arr[i].get_bottom()+DOWN*0.1, UP)

        self.play(Create(dsa_arr), Write(bin_indices))
        self.wait(0.5)

        level_map = {}

        #TODO change to range
        for i, _ in enumerate(arr):
            index = i+1
            lvl = tree_level(index)
            if lvl not in level_map:
                level_map[lvl] = []
                level_map[lvl].append((fta[index],index))
            else:
                level_map[lvl].append((fta[index],index))

            anim_group = AnimationGroup(dsa_arr[i].animate.shift(UP*UPLEVEL*lvl), bin_indices[i].animate.shift(UP*UPLEVEL*lvl), lag_ratio=0.025)
            self.play(anim_group)
            self.wait(0.5)

            old = dsa_arr[i].submobjects[1]
            Text.become(dsa_arr[i].submobjects[1], 
                        Text(str(fta[index]), stroke_width=old.stroke_width, color=old.color, weight=old.weight, font=old.font).match_style(old)
                        .scale(0.75)
                        .move_to(old)
                        )
            if lvl > 0:
                self.play(Write(dsa_arr[i].submobjects[1]))

        graph = {}
        label_dict = {}
        position_dict = {}
        i = 0
        while i in level_map:
            for j in range(0,len(level_map[i]),2):
                if i+1 not in level_map or not level_map[i+1][j//2:]:
                    key = str(level_map[i][j][1])
                    graph[key] = graph.get(key, ([], Circle(0.5)))
                    label_dict[key] = str(level_map[i][j][0])
                    position_dict[key] = dsa_arr[level_map[i][j][1]-1].submobjects[0].get_center()
                    break

                lvl_list = level_map[i]
                grab = 2
                if len(lvl_list) == 1:
                    grab = 1
                graph[str(level_map[i+1][j//2][1])] = ([str(x[1]) for x in lvl_list[j:grab+j]], Circle(0.5))

                for index in lvl_list[j:grab+j]:
                    graph[str(index[1])] = graph.get(str(index[1]), ([], Circle(0.5)))
                    label_dict[str(index[1])] = str(index[0])
                    position_dict[str(index[1])] = dsa_arr[index[1]-1].submobjects[0].get_center()

            i += 1

        print(graph)
        mgraph = MGraphGeneric(graph, style=MGraphStyle.PURPLE, nodes_position=position_dict, value_dict=label_dict, edge_arrows=False)
        self.play(FadeOut(dsa_arr))
        self.play(Create(mgraph))
        self.wait(3)





       
