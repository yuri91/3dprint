from build123d import *
import math

density=2700*1000/(1000000000)

base_w=54
base_l=118
base_h=16
base_fillet_r=6

slot_w=16
slot_l=99

guide_b=22
guide_h=8
guide_a=60

side_l=55
side_w=14
side_h=42
side_fillet_r=12
side_hole_1_r=30/2
side_hole_2_r=38/2
side_hole_2_d=4

def guide():
    guide_p = guide_h/math.tan(math.radians(guide_a))
    guide_b2 = guide_b + guide_p*2
    t = (-Plane.YZ.offset(base_l/2)) * Trapezoid(guide_b2, guide_h, guide_a, align=(Align.CENTER, Align.MAX))
    g = extrude(t, base_l)
    return g
def base():
    r = Rectangle(base_l, base_w)
    r = fillet(r.vertices(), base_fillet_r)
    s = SlotOverall(slot_l, slot_w)
    r = r - s
    b = extrude(r, base_h)
    return b
def side():
    sh = side_h - guide_h
    r = Rectangle(side_l, sh)
    c = Circle(side_l/2)
    circle_pos = Pos(0, sh/2)
    b = r + (circle_pos * c)
    s = extrude(b, -side_w)
    #fillet_edges = s.edges().filter_by(GeomType.LINE).filter_by(Plane.XY).sort_by(Axis.X)[0]
    #s = fillet(fillet_edges, base_fillet_r)

    hole_1 = circle_pos * Circle(side_hole_1_r)
    hole_1 = extrude(hole_1, -side_w)
    hole_2 = circle_pos * Circle(side_hole_2_r)
    hole_2 = extrude(hole_2, -side_hole_2_d)
    s = s - hole_1 - hole_2
    s = (Plane.XZ.offset(base_w/2)*Pos(side_l/2-base_l/2, sh/2+guide_h)) * s
    return s
def close_arc(a):
    t1 = a%0
    t2 = a%1
    a1 = Axis(a@0, a%0)
    a2 = Axis(a@1, a%1)
    inters = a1.intersect(a2)
    l1 = Line(a@0, inters)
    l2 = Line(a@1, inters)
    return make_face([a, l1, l2])
    
def run(show, export):
    b = base()
    g = guide()
    b = b - g
    s = side()
    s2 = mirror(s, Plane.XZ)
    r = b + s + s2
    slope_edges = (r.edges() | GeomType.LINE | Axis.Y).filter_by_position(Axis.Z, base_h, base_h).filter_by_position(Axis.X, -side_l, side_l)
    r = fillet(slope_edges, side_fillet_r)
    base_fillet_arcs = (r.edges() | GeomType.CIRCLE).filter_by_position(Axis.Z, 0, 0)
    base_fillet_tri = [close_arc(a) for a in base_fillet_arcs]
    base_fillet_tri = Curve(base_fillet_tri)
    k=extrude(base_fillet_tri, side_h+side_l/2)
    r = r - k
    print(r.volume*density)
    show(r)
    pass

