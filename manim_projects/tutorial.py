from manim import *
from math import sqrt

class Test(Scene):
    def construct(self):
        length = Tex("r = 1").to_edge(UR, buff=1)
        circle = Circle(radius=3, color=GREEN)
        square = Square(side_length=6, stroke_color=GREEN, fill_color=BLUE, fill_opacity=0.1)
        line = Line(start = RIGHT, end = LEFT, color=RED).shift(LEFT*2)
        self.play(Write(length))
        self.play(Create(circle), run_time=2)
        self.play(DrawBorderThenFill(square), run_time=1.5)
        #self.play(Create(line), run_time=1)
        self.play(square.animate.scale(0.5), circle.animate.scale(0.5))
        self.play(circle.animate.scale(sqrt(2) + 10**-2))
        self.remove(length)
        length = MathTex(r"r = \sqrt{2}").to_edge(UR, buff=1)
        self.play(FadeIn(length))
        self.wait()