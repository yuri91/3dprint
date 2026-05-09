import math

from build123d import *  # Also works with cadquery objects!

DEG = math.pi / 180

base_depth = 50 * MM
border = 5 * MM
frame_bottom_h = 14.50 * MM
frame_h = 96.37 * MM
hole_tolerance = 0.30 * MM
mount_d = 1.50 * MM
mount_h = 8.0 * MM
mount_l = 7.65 * MM
screen_d = 7.75 * MM
screen_h = 94.20 * MM
screen_l = 165.00 * MM
screen_max_d = 14.40 * MM
base_height = 2 * border + mount_d
base_angle = 10 * DEG
support_extra_l = 15 * MM
support_thickness = 1 * MM
fillet_r = 0.3 * MM


def run(show, export):
    base_hole = Rectangle(screen_l, mount_d)
    slot = offset(base_hole, border, kind=Kind.INTERSECTION) - base_hole
    tilt = (0, -math.tan(base_angle), 1)
    base = extrude(slot, frame_bottom_h, dir=tilt)
    bb = base.bounding_box()

    p1 = (bb.min.X, bb.min.Y, bb.max.Z)
    p2_vert = (bb.min.X, bb.min.Y, bb.min.Z)
    p2 = (bb.min.X, slot.bounding_box().min.Y, bb.min.Z)
    p3 = (bb.min.X, bb.min.Y - support_extra_l, bb.min.Z)
    side1_vert = Line(p1, p2_vert)
    side1 = Line(p1, p2)
    side2 = Line(p2, p3)
    curve = Spline(p1, p3, tangents=[side1_vert % 0, side2 % 1])
    profile = make_face(side1 + side2 + curve)
    support = extrude(profile, bb.size.X, dir=(1, 0, 0))
    upper = base + support
    upper_bb = upper.bounding_box()

    platform = Pos(
        upper_bb.center().X,
        upper_bb.center().Y,
        upper_bb.min.Z - support_thickness / 2,
    ) * Box(
        upper_bb.size.X,
        upper_bb.size.Y,
        support_thickness,
    )
    
    screen_base = fillet((platform + upper).edges(), radius=fillet_r)

    show(screen_base)
    export(screen_base)
