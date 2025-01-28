from build123d import *

w=29
l1=65
l2=30
h1=15
h2=62
r=14.5
density=1020*1000/(1000000000)

def pillar():
    base = Pos(0, l2/2) * Rectangle(w, l2)
    ret = extrude(base, h2)
    return ret
def foot():
    l = l2-l1-r
    rec = Rectangle(w, l)
    circle = Circle(r)
    base = rec + (Pos(0, l/2)*circle)
    base = Pos(0, l/2+l2) * base
    ret = extrude(base, h1)
    return ret
def run(show, export):
    p = pillar()
    f = foot()
    ret = p + f
    print(ret.volume*density)
    show(ret)

