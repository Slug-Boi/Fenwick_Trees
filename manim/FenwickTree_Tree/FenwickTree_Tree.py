from manim import *
from manim_dsa import *
from manim_dsa.m_graph_generic.m_graph_generic import MGraphGeneric
from math import log2, ceil
from fenwick_tree import FenwickTree
from copy import deepcopy

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
        self.wait(2)

        print(dsa_arr.submobjects)
        #TODO figure out why channing the font size to 36 makes the text gap by like 5 pixels

        style = MGraphStyle.DEFAULT

        style.node_label["font_size"] = 36

        for index, val in enumerate(dsa_arr.submobjects[1:-1]):
            graph[str(index+1)] = ([], val.submobjects[0].copy())
            # print(index)
            # print(fta[index+1])
            label_dict[str(index+1)] = str(fta[index+1]).strip()

            position_dict[str(index+1)] = dsa_arr[index].submobjects[0].get_center()
        mgraph = MGraphGeneric(graph, style=style, nodes_position=position_dict, value_dict=label_dict, edge_arrows=False)
        
        self.remove(dsa_arr)
        self.add(mgraph)

        self.wait(5)
        anim_group = []
        i = 0
        while i in level_map:
            for j in range(0,len(level_map[i]),2):
                if i+1 not in level_map or not level_map[i+1][j//2:]:
                    break

                lvl_list = level_map[i]
                grab = 2
                if len(lvl_list) == 1:
                    grab = 1
                for e in range(grab):
                    self.play(mgraph.animate.add_edge(str(level_map[i+1][j//2][1]), str(lvl_list[j+e][1])))
            i += 1

        self.wait(3)



       
