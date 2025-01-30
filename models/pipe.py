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
epsilon = 0.2

def make_path(straight_l, curve_a, curve_r) -> Curve:
    path_straight_1 = Line((0, 0), (0, straight_l))
    path_curve = JernArc(start=path_straight_1@1, tangent=path_straight_1%1, radius=curve_r, arc_size=-curve_a)
    straight_2_a = (path_curve%1).get_angle(Axis.X.direction)
    path_straight_2 = PolarLine(start=path_curve@1, length=straight_l, angle=straight_2_a)
    path = Plane.XZ * (path_straight_1 + path_curve + path_straight_2)
    return path

def make_filled(profile_1, profile_2, profile_3):
    path = make_path(straight_l+merge_l, curve_a, curve_r)
    straight_fraction = straight_l / path.wire().length
    straight_merge_fraction = (straight_l+merge_l) / path.wire().length
    path_1 = path.split(Plane.XY * (path^straight_fraction), keep=Keep.BOTTOM)
    path_2 = Curve(path.split(Plane.XY * (path^straight_merge_fraction), keep=Keep.TOP))
    path_3 = path_2.split(Plane.XY * (path^(1-straight_fraction)), keep=Keep.TOP)
    path_2 = path_2.split(Plane.XY * (path^(1-straight_merge_fraction)), keep=Keep.BOTTOM)

    pipe_1_top_face = (path_1^1) * profile_1
    pipe_2_bottom_face = (path_2^0) * profile_2
    pipe_2_top_face = (path_2^1) * profile_2
    pipe_3_bottom_face = (path_3^0) * profile_3

    pipe_1 = sweep((path_1^0)*profile_1, path=path_1)
    pipe_2 = sweep((path_2^0)*profile_2, path=path_2)
    pipe_3 = sweep((path_3^0)*profile_3, path=path_3)
    bridge_1 = loft([pipe_1_top_face, pipe_2_bottom_face])
    bridge_2 = loft([pipe_2_top_face, pipe_3_bottom_face])

    pipe = pipe_1 + bridge_1 + pipe_2 + bridge_2 + pipe_3
    return pipe

def hex_pipe_joint_60():
    profile_hex_ends = RegularPolygon((radius+thickness)*2/math.sqrt(3), 6)
    profile_hex_middle = scale(profile_hex_ends, by=1-choke/radius)
    profile_inner_ends = Circle(radius)
    profile_inner_middle = scale(profile_inner_ends, by=1-choke/radius)

    pipe_outer = make_filled(profile_hex_ends, profile_hex_middle, profile_hex_ends)
    pipe_inner = make_filled(profile_inner_ends, profile_inner_middle, profile_inner_ends)
    pipe = pipe_outer - pipe_inner
    return pipe
def hex_pipe_joint_in_60():
    profile_hex_end_1 = RegularPolygon((radius+thickness)*2/math.sqrt(3), 6)
    profile_hex_end_2 = Circle(radius-epsilon)
    profile_hex_middle = scale(profile_hex_end_1, by=1-choke/radius)
    profile_inner_end_1 = Circle(radius)
    profile_inner_end_2 = Circle(radius-epsilon-thickness)
    profile_inner_middle = scale(profile_inner_end_1, by=1-choke/radius)

    pipe_outer = make_filled(profile_hex_end_1, profile_hex_middle, profile_hex_end_2)
    pipe_inner = make_filled(profile_inner_end_1, profile_inner_middle, profile_inner_end_2)
    pipe = pipe_outer - pipe_inner
    return pipe
def run(show, export):
    joint_60 = hex_pipe_joint_60()
    joint_in_60 = hex_pipe_joint_in_60()

    show(joint_60, joint_in_60)
    export(joint_60, joint_in_60)

