from manim import *
from manim_dsa import *

class dynamic_render(Scene):
    def construct(self):
        arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        dsa_arr = MArray(arr, margin=1.25, style=MArrayStyle.BLUE).scale(0.75).to_edge(DOWN)

        print(dsa_arr.width)
        print(dsa_arr.height)
        print(dsa_arr.width/self.camera.frame_width)

        print(self.camera.frame_width)
        print(self.camera.frame_height)
        
        #self.camera.frame_width = self.camera.frame_width * 1.7
        #self.camera.frame_height = self.camera.frame_height * 1.7

        dsa_arr.scale(0.6)
        dsa_arr.scale_to_fit_width(13.22)
        
        self.play(Create(dsa_arr))


