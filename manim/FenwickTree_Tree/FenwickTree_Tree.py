from manim import *
from manim_dsa import *
from manim_dsa.m_graph_generic.m_graph_generic import MGraphGeneric
from math import log2, ceil
from fenwick_tree import FenwickTree
from copy import deepcopy

global_font = "DejaVu Sans Condensed"

def binary_index(index,b_len) -> str:
    return "{0:0{b_len}b}".format(index, b_len=b_len)

def tree_level(index) -> int:
    lsb = index & -index
    return int(log2(lsb))

class FenwickTree_Tree(Scene):
    def resetPartialSums(self):
        animGroup = AnimationGroup(FadeOut(self.results), self.bracket.animate.move_to(self.bin_text.get_right()+RIGHT*0.15, LEFT), lag_ratio=0.5)
        self.play(animGroup)

    def addToPartialSum(self) -> None:
        if len(self.results) > 1:
            self.results.insert(-1, Text(";", font=global_font).scale(0.6))

        self.results.arrange(buff=0.18, aligned_edge=DOWN)
        self.results.move_to(self.bin_text.get_right()+RIGHT*0.15, LEFT)
        if len(self.results) == 1:
            animGroup = AnimationGroup(self.bracket.animate.move_to(self.results[-1].get_right()+RIGHT*0.15, LEFT), FadeIn(self.results[-1]), lag_ratio=0.5)
        else:
            animGroup = AnimationGroup(self.bracket.animate.move_to(self.results[-1].get_right()+RIGHT*0.15, LEFT), FadeIn(VGroup(self.results[-2], self.results[-1])), lag_ratio=0.5)
        self.play(animGroup)

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
    
        dsa_arr = MArray(arr, margin=1.25, style=MArrayStyle.BLUE).scale(0.75).to_edge(DOWN).shift(UP*0.3)
        bin_indices = VGroup(*[Text(binary_index(i+1,binary_len), color=BLUE_B, weight=NORMAL, stroke_width=1.2, stroke_color=BLUE_E, font=global_font).scale(0.5) for i in range(len(arr))])

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
        
        self.wait(0.5)
        indexMoveGroup = AnimationGroup(*[index.animate.shift(DOWN*0.2) for i, index in enumerate(bin_indices) if tree_level(i+1) != 0],lag_ratio=0.15)
        self.play(indexMoveGroup)

        graph = {}
        label_dict = {}
        position_dict = {}
        self.wait(2)

        #print(dsa_arr.submobjects)

        style = MGraphStyle.DEFAULT
        style.edge_line["stroke_width"] = 5.5
        style.edge_line["color"] = GOLD_E
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
        
        self.bring_to_front(bin_indices)
        self.play(*anim_group)
        self.wait(3)

        # Query
        queryText = Text("Query: Sum(").scale(0.75).to_corner(UL)
        queryParen = Text(")").scale(0.75).move_to(queryText.get_right()+RIGHT*0.42, LEFT).align_to(queryText.get_top(), UP)

        self.bin_text = Text("Partial sums = [").scale(0.6).move_to(queryText.get_left(),LEFT).shift(DOWN*0.5)
        self.bracket = Text("]").scale(0.6).move_to(self.bin_text.get_right(), LEFT).shift(RIGHT*0.15)
        self.play(AnimationGroup(Write(queryText), Write(queryParen), lag_ratio=0.3), AnimationGroup(Write(self.bin_text), Write(self.bracket), lag_ratio=0.3))
        
        edge_highlight = []
        boxes_highlight = []
        for i in range(1, len(arr)+1):
            self.results = VGroup()
            
            sum_index = Text("{}".format(i-1)).scale(0.75).move_to(queryText.get_right()+RIGHT*0.1, LEFT).align_to(queryParen.get_center(), ORIGIN)
            self.play(Write(sum_index), queryParen.animate.align_to(sum_index.get_right()+RIGHT*0.1, LEFT))
            self.wait(1)

            highlight_indices = []
            z = i
            prev_z = -1
            while z > 0:
                mathGroup = VGroup()
                highlight_indices.append(z)
                prev_z = z
                z -= -z & z
                if z > 0:
                    if prev_z == i:
                        startIndex = (
                            Text(binary_index(prev_z, 4), font=global_font)
                            .scale(0.6)
                            .move_to(self.bin_text.get_bottom(), UP)
                            .shift(DOWN*0.3)
                        )
                        self.results.add(startIndex.copy().set_color(PINK))
                        self.wait(0.5)
                        self.play(Write(startIndex))
                        self.wait(1)
                        self.play(startIndex.animate.set_color(PINK))

                        self.addToPartialSum()

                        self.play(FadeOut(startIndex), self.results.animate.set_color(WHITE))

                    mathGroup.add(
                        Text(binary_index(prev_z, 4),font=global_font).scale(0.6),
                        Text("- "  + binary_index(-prev_z & prev_z, 4),font=global_font).scale(0.6),
                    )
                    mathGroup.add(
                        Line(mathGroup[1].get_left(), mathGroup[1].get_right()),
                        Text(binary_index(z, 4),font=global_font).scale(0.6)
                    )
                    mathGroup.arrange(DOWN, center=False, aligned_edge=RIGHT)
                    mathGroup.move_to(self.bin_text.get_bottom(), UP).shift(DOWN*0.3)

                    self.play(Write(mathGroup))
                    self.wait(0.5)
                    self.play(mathGroup[-1].animate.set_color(PINK))

                    self.results.add(mathGroup[-1].copy().set_color(PINK))
                    self.addToPartialSum()
                    
                    self.wait(1)
                    self.play(FadeOut(mathGroup), self.results[-1].animate.set_color(WHITE))
                elif len(highlight_indices) == 1:
                    mathGroup.add(Text(binary_index(prev_z, 4),font=global_font).scale(0.6))
                    mathGroup.move_to(self.bin_text.get_bottom(), UP).shift(DOWN*0.3)

                    self.play(Write(mathGroup))
                    self.wait(0.5)
                    self.play(mathGroup[-1].animate.set_color(PINK))

                    self.results.add(mathGroup[-1].copy().set_color(PINK))
                    self.addToPartialSum()

                    self.wait(1)
                    self.play(FadeOut(mathGroup), self.results[-1].animate.set_color(WHITE))

            prevIndex = -1

            edge_highlight = []
            boxes_highlight = []

            for index in highlight_indices:
                boxes_highlight.append(mgraph[str(index)])
                if(str(index), str(prevIndex)) in mgraph:
                    edge_highlight.append(mgraph[(str(index), str(prevIndex))])
                prevIndex = index

            self.play(
                *[box.animate.highlight(PINK) for box in boxes_highlight], 
                *[edge.animate.highlight(PINK) for edge in edge_highlight ]
                )
            self.wait(1)
            if boxes_highlight:
                self.play(*[box.animate.unhighlight() for box in boxes_highlight], *[edge.animate.unhighlight() for edge in edge_highlight],Unwrite(sum_index))
            self.resetPartialSums()

        self.wait(2)

        self.play(Unwrite(queryText), 
                  mgraph.nodes[str(len(fta)-1)][0].animate.set_fill(BLUE), 
                  AnimationGroup(Unwrite(self.bracket), Unwrite(self.bin_text), lag_ratio=0.3),
                  AnimationGroup(Unwrite(queryParen),Unwrite(sum_index,queryText),lag_ratio=0.1)
                  )

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
        highlights = []
        while updateIndex < len(fta):
            mathText = []
            leaf = tree_level(updateIndex) == 0
            # Create mobjects for binary equation for finding next index in tree
            if leaf:
                mathText.append(
                    Text(f"{updateIndex-1} + 1 = {updateIndex} = {binary_index(updateIndex, 4)}", font=global_font)
                    .scale(0.6)
                    .move_to(updateText.get_left(), LEFT)
                    .shift(DOWN)
                )
            else:
                mathText.append(
                    Text(binary_index(prevIndex, 4),font=global_font)
                    .scale(0.6)
                    .move_to(updateText.get_left(), LEFT)
                    .shift(DOWN+RIGHT*1.4)
                )
                # lsbText = Text(f"+ lsb({binary_index(prevIndex, 4)})").scale(0.75).move_to(indexText.get_right(), RIGHT).shift(DOWN*0.6)
                mathText.append(
                    Text(f"+ {binary_index(prevIndex & -prevIndex, 4)}",font=global_font)
                    .scale(0.6)
                    .move_to(mathText[-1].get_right(), RIGHT)
                    .shift(DOWN*0.6)
                )
                mathText.append(
                    Line(mathText[-1].get_left()+DOWN*0.3, mathText[-1].get_right()+DOWN*0.3)
                )
                mathText.append(
                    Text(binary_index(updateIndex, 4), font=global_font)
                    .scale(0.6)
                    .move_to(mathText[-1].get_right(), RIGHT)
                    .shift(DOWN*0.3)
                )
            mathAnimation = AnimationGroup(*[Write(x) for x in mathText], lag_ratio=0.3)
            self.play(mathAnimation)
            self.wait(0.4)

            # Highlight and change text in tree
            highlights.append(updateIndex)
            self.play(mgraph[str(updateIndex)].animate.highlight(PINK))
            Text.become(mgraph[str(updateIndex)].submobjects[1], Text(str(fw.get_tree()[updateIndex]), **style.node_label).scale(0.75).move_to(mgraph[str(updateIndex)].submobjects[1]))
            self.play(Write(mgraph[str(updateIndex)].submobjects[1]))
            
            # Prep for next loop
            self.play(*[Unwrite(x) for x in mathText])
            self.wait(0.3)
            prevIndex = updateIndex
            updateIndex += updateIndex & -updateIndex
        
        self.play(Unwrite(updateText), *[mgraph[str(node)].animate.unhighlight() for node in highlights])

        """
        Range Query
        """
        
        startRange = 3
        endRange = 6
        rangeText = (
            Text(f"Range Query({startRange}, {endRange})")
            .scale(0.75)
            .to_edge(UP+LEFT)
            .shift(LEFT*0.3)
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
        z = endRange+1 # Adjust for 1 index
        while z > 0:
            highlight_indices.append(z)
            z -= z & -z
    
        edge_highlight = []
        boxes_highlight = []

        for index in highlight_indices:
            boxes_highlight.append(mgraph[str(index)])
            if(str(index), str(prevIndex)) in mgraph:
                edge_highlight.append(mgraph[(str(index), str(prevIndex))])
            prevIndex = index

        self.play(
            *[box.animate.highlight(PINK) for box in boxes_highlight], 
            *[edge.animate.highlight(PINK) for edge in edge_highlight ]
        )

        endResultText = (
            Text(f"= {fw.sum(endRange)}")
            .scale(0.6)
            .move_to(endQueryText.get_right(), LEFT)
            .shift(RIGHT*0.2+UP*0.03)
        )
        self.play(Write(endResultText))
        self.play(
            *[box.animate.unhighlight() for box in boxes_highlight], 
            *[edge.animate.unhighlight() for edge in edge_highlight ]
        )
        self.wait(1)
        
        # Start qurey
        startQueryText = (
            Text(f"Query: Sum({startRange})")
            .scale(0.6)
            .move_to(endQueryText.get_left(), LEFT)
            .shift(DOWN*0.5)
        )
        self.play(Write(startQueryText))
    
        highlight_indices = []
        z = startRange+1 # Adjust for 1 index
        while z > 0:
            highlight_indices.append(z)
            z -= z & -z
    
        edge_highlight = []
        boxes_highlight = []

        for index in highlight_indices:
            boxes_highlight.append(mgraph[str(index)])
            if(str(index), str(prevIndex)) in mgraph:
                edge_highlight.append(mgraph[(str(index), str(prevIndex))])
            prevIndex = index

        self.play(
            *[box.animate.highlight(PINK) for box in boxes_highlight], 
            *[edge.animate.highlight(PINK) for edge in edge_highlight ]
        )

        startResultText = (
            Text(f"= {fw.sum(startRange)}")
            .scale(0.6)
            .move_to(startQueryText.get_right(), LEFT)
            .shift(RIGHT*0.2+UP*0.03)
        )
        self.play(Write(startResultText))
        self.play(
            *[box.animate.unhighlight() for box in boxes_highlight], 
            *[edge.animate.unhighlight() for edge in edge_highlight ]
        )
        self.wait(1)
        
        # Final result
        rangeResultText = (
            Text(f"= {fw.sum(endRange)} - {fw.sum(startRange)} = {fw.sum(endRange) - fw.sum(startRange)}")
            .scale(0.75)
            .move_to(rangeText.get_right(), LEFT)
            .shift(RIGHT*0.28+UP*0.04)
        )
        self.play(
            Write(rangeResultText), 
            FadeOut(endQueryText),
            FadeOut(endResultText),
            FadeOut(startQueryText),
            FadeOut(startResultText)
        )
        self.wait(2)
        self.play(
            AnimationGroup(
                Unwrite(rangeResultText), 
                Unwrite(rangeText), 
                lag_ratio=0.6
            )
        )

        self.wait(3)