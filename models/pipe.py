from build123d import *  # Also works with cadquery objects!
import copy
import math

radius = 32.5/2
thickness = 2
choke = 2
straight_l = 25
merge_l = 1.5
curve_a = 60
curve_r = radius * 1.3

def make_path(straight_l, curve_a, curve_r) -> Curve:
    path_straight_1 = Line((0, 0), (0, straight_l))
    path_curve = JernArc(start=path_straight_1@1, tangent=path_straight_1%1, radius=curve_r, arc_size=-curve_a)
    straight_2_a = (path_curve%1).get_angle(Axis.X.direction)
    path_straight_2 = PolarLine(start=path_curve@1, length=straight_l, angle=straight_2_a)
    path = Plane.XZ * (path_straight_1 + path_curve + path_straight_2)
    return path

def make_filled(profile):
    profile_big = profile
    profile_small = scale(profile, by=1-choke/radius)

    path = make_path(straight_l+merge_l, curve_a, curve_r)
    straight_fraction = straight_l / path.wire().length
    straight_merge_fraction = (straight_l+merge_l) / path.wire().length
    path_1 = path.split(Plane.XY * (path^straight_fraction), keep=Keep.BOTTOM)
    path_2 = Curve(path.split(Plane.XY * (path^straight_merge_fraction), keep=Keep.TOP))
    path_3 = path_2.split(Plane.XY * (path^(1-straight_fraction)), keep=Keep.TOP)
    path_2 = path_2.split(Plane.XY * (path^(1-straight_merge_fraction)), keep=Keep.BOTTOM)

    pipe_1_top_face = (path_1^1) * profile_big
    pipe_2_bottom_face = (path_2^0) * profile_small
    pipe_2_top_face = (path_2^1) * profile_small
    pipe_3_bottom_face = (path_3^0) * profile_big

    pipe_1 = sweep((path_1^0)*profile_big, path=path_1)
    pipe_2 = sweep((path_2^0)*profile_small, path=path_2)
    pipe_3 = sweep((path_3^0)*profile_big, path=path_3)
    bridge_1 = loft([pipe_1_top_face, pipe_2_bottom_face])
    bridge_2 = loft([pipe_2_top_face, pipe_3_bottom_face])

    pipe = pipe_1 + bridge_1 + pipe_2 + bridge_2 + pipe_3
    return pipe

def run(show, export):
    pipe_outer = make_filled(RegularPolygon((radius+thickness)*2/math.sqrt(3), 6))
    pipe_inner = make_filled(Circle(radius))
    pipe = pipe_outer - pipe_inner

    show(pipe)
    export(pipe)

