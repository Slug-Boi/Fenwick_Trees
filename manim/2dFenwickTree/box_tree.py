from manim import *
from manim_dsa import Highlightable
from math import log2
from fenwick_tree import FenwickTree
from typing import override

class TreeElement(VGroup, Highlightable):
    def __init__(self, rect, value, index=None):
        super().__init__()
        self.rect = rect
        self._add_highlight(self.rect)
        self.default_color = self.rect.color
        self.default_stroke_color = self.rect.stroke_color
        self.value = value.move_to(self.rect)
        self += self.rect
        self += self.value
        if index:
            self.index = index.move_to(self.rect.get_bottom(), UP).shift(DOWN*0.1)
            self += self.index

    def highlight(self, color=GREEN, stroke_color=BLUE_A):
        self.rect.set_color(color)
        self.rect.stroke_color = stroke_color
        return self
    
    def unhighlight(self):
        self.rect.set_color(self.default_color)
        self.rect.stroke_color = self.default_stroke_color
        return self
    
class BoxTree(VGroup):
    defaultStyle = {
            "rect": {
                "height": 0.5,
                "width": 0.5,
                "color": BLUE_A,
                "fill_color": BLUE,
                "fill_opacity": 1.0
            },
            "index": {
                "color": WHITE,
            },
            "value": {},
            "x_buffer": 0,
            "y_buffer": 0,
            "value_scale": 0.4,
            "index_scale": 0.4,
            "uplevel": 0.5,   
}
    def __init__(self, array, style=defaultStyle, show_indices=False, show_values=True):
        super().__init__()
        self.array = array
        self.style = style
        self.show_values = show_values
        self.show_indices = show_indices
        for i,v in enumerate(self.array):
            self += (
                TreeElement(
                    Rectangle(**self.style["rect"]),
                    Text(str(v), **self.style["value"], fill_opacity=1 if self.show_values else 0).scale(self.style["value_scale"]),
                    index=Text(str(i+1), **self.style["index"]).scale(self.style["index_scale"]) if self.show_indices else None
                    )
            )
        self.arrange(buff=self.style["x_buffer"])
        self.move_to(ORIGIN)
    
    @staticmethod
    def _tree_level(index) -> int:
        lsb = index & -index
        return int(log2(lsb))

    def create(self):
        tree = FenwickTree(self.array)
        animations = []
        for i in range(len(self.array)):
            level = self._tree_level(i+1)
            boxWidth = self[0][0].get_width()*2**level + (2**level-1)*self.style["x_buffer"]
            tempStyle = self.style["rect"].copy()
            tempStyle["width"] = boxWidth
            tempStyle["height"] = self[0][0].get_height()
            newElement = (
                TreeElement(Rectangle(
                    **tempStyle
                    ), 
                    Text(str(tree.get_tree()[i+1]), **self.style["value"], fill_opacity=1 if self.show_values else 0)
                    .scale(self.style["value_scale"])
                )
                .move_to(self[i][0].get_right(), RIGHT)
                .shift(UP*self[0][0].get_height()*level + (UP*self.style["y_buffer"]*level))
            )
            if self.show_indices:
                newElement += self[i][2]
            domainExpansion = Transform(self[i], newElement)
            animations.append(domainExpansion)

        return animations
    
    def hightlight(self, index):
        pass

# @override
# def scale(self,n):
#     super().scale(n)

#     self.style["value"]["scale"] *= n
