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

        #print(dsa_arr.submobjects)
        #TODO figure out why channing the font size to 36 makes the text gap by like 5 pixels

        style = MGraphStyle.DEFAULT

        style.node_label["font_size"] = 48
    
        for index, val in enumerate(dsa_arr.submobjects[1:-1]):
            graph[str(index+1)] = ([], val.submobjects[0].copy())
            # print(index)
            # print(fta[index+1])
            label_dict[str(index+1)] = str(fta[index+1]).strip()

            position_dict[str(index+1)] = dsa_arr[index].submobjects[0].get_center()
        mgraph = MGraphGeneric(graph, style=style, nodes_position=position_dict, value_dict=label_dict, edge_arrows=False)      

        # Scale the font to fit the marray text
        for text in mgraph.submobjects:
            text[1].scale(0.75)

        self.remove(dsa_arr)
        self.add(mgraph)

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
                    anim_group.append(mgraph.animate.add_edge(str(level_map[i+1][j//2][1]), str(lvl_list[j+e][1])))
            i += 1

        self.play(*anim_group)
        self.wait(3)

        # Query

        queryText = Text("Query: Sum(0)").scale(0.75).to_corner(UL)

        prev_hightlights = []
        prev_boxes = []
        for i in range(1, len(arr)+1):
            queryText.become(Text("Query: Sum({})".format(i-1)).scale(0.75).to_corner(UL))
            self.play(Write(queryText))
            self.wait(1)

            highlight_indices = []
            z = i
            while z > 0:
                highlight_indices.append(z)
                z -= -z & z

            prevIndex = -1

            edge_highlight = []
            boxes_highlight = []

            for index in highlight_indices:
                boxes_highlight.append(mgraph[str(index)])
                if(str(index), str(prevIndex)) in mgraph:
                    edge_highlight.append(mgraph[(str(index), str(prevIndex))])
                prevIndex = index

            

            self.play(
                *[box.animate.unhighlight() for box in prev_boxes if box not in boxes_highlight],
                *[box.animate.highlight(PINK) for box in boxes_highlight], 
                *[edge.animate.unhighlight() for edge in prev_hightlights if edge not in edge_highlight],
                *[edge.animate.highlight(PINK) for edge in edge_highlight ]
                )
            prev_hightlights = edge_highlight
            prev_boxes = boxes_highlight
            self.wait(1)
    
        self.wait(2)

        self.play(Unwrite(queryText), mgraph.nodes[str(len(fta)-1)][0].animate.set_fill(BLUE))

        """
        Update Tree Animation
        """
        updateIndex = 5
        prevIndex = -1
        updateBy = 3
        fw.update(updateIndex-1, updateBy)
        updateText = (
            Text(f"Update({updateIndex-1}, {updateBy})")
            .scale(0.75)
            .to_edge(UP+LEFT)
            .shift(LEFT*0.3)
        )
        self.play(Write(updateText))
        while updateIndex < len(fta):
            mathText = []
            leaf = tree_level(updateIndex) == 0
            # Create mobjects for binary equation for finding next index in tree
            if leaf:
                mathText.append(
                    Text(f"{updateIndex-1} + 1 = {updateIndex} = {binary_index(updateIndex, 4)}")
                    .scale(0.75)
                    .move_to(updateText.get_left(), LEFT)
                    .shift(DOWN)
                )
            else:
                mathText.append(
                    Text(binary_index(prevIndex, 4))
                    .scale(0.75)
                    .move_to(updateText.get_left(), LEFT)
                    .shift(DOWN+RIGHT*1.4)
                )
                # lsbText = Text(f"+ lsb({binary_index(prevIndex, 4)})").scale(0.75).move_to(indexText.get_right(), RIGHT).shift(DOWN*0.6)
                mathText.append(
                    Text(f"+ {binary_index(prevIndex & -prevIndex, 4)}")
                    .scale(0.75)
                    .move_to(mathText[-1].get_right(), RIGHT)
                    .shift(DOWN*0.6)
                )
                mathText.append(
                    Line(mathText[-1].get_left()+DOWN*0.3, mathText[-1].get_right()+DOWN*0.3)
                )
                mathText.append(
                    Text(binary_index(updateIndex, 4))
                    .scale(0.75)
                    .move_to(mathText[-1].get_right(), RIGHT)
                    .shift(DOWN*0.3)
                )
            mathAnimation = AnimationGroup(*[Write(x) for x in mathText], lag_ratio=0.3)
            self.play(mathAnimation)
            self.wait(0.4)

            # Highlight and change text in tree
            self.play(mgraph[str(updateIndex)].animate.highlight())
            Text.become(mgraph[str(updateIndex)].submobjects[1], Text(str(fw.get_tree()[updateIndex]), **style.node_label).scale(0.75).move_to(mgraph[str(updateIndex)].submobjects[1]))
            self.play(Write(mgraph[str(updateIndex)].submobjects[1]))
            
            # Prep for next loop
            self.play(*[Unwrite(x) for x in mathText])
            self.wait(0.3)
            prevIndex = updateIndex
            updateIndex += updateIndex & -updateIndex
        
        self.play(Unwrite(updateText))
    
        self.wait(3)