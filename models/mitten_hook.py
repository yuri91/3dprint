import math

from build123d import *

DEG = math.pi / 180

# --- Table edge the clip slots onto ---
table_th = 29 * MM       # thickness of the table top
overhang = 34 * MM       # how far the table top sticks out past the cabinet face
top_len = 40 * MM        # length of the top lip (rests on the table)
tol = 0.5 * MM           # clearance so it slides on easily

# --- Clip body ---
wall = 5 * MM            # wall thickness around the slot
width = 30 * MM          # width of the part, along the table edge
lip_angle = 2.0          # deg; tapers the top lip so the slot grips when pushed on

# --- Hook to hang mittens on ---
hook_w = 5 * MM         # width of the hook peg along the table edge (one side)
hook_len = 35 * MM       # length of the hook stem below the clip
hook_r = 14 * MM         # radius of the hook curl
hook_arc = 200.0         # curl wrap in degrees (>180 to retain the mitten)

fillet_r = 1.0 * MM

slot_h = table_th + tol          # inner height of the slot
# lower lip reaches from the outer edge, past the table front face (at the back
# wall), all the way to the cabinet face
bottom_len = overhang + wall


def run(show, export):
    # Cross-section drawn in local XY, then mapped onto the YZ plane and
    # extruded along X (the table edge). Local x -> Y (into the table),
    # local y -> Z (up). The outer edge that hangs over the table's front is
    # at Y = 0; the table slides in against the back wall at Y = wall.
    # Back wall stops at the slot ceiling (slot_h); the tilted top lip supplies
    # the material above it, so the top is one continuous slope with no step.
    back = Pos(0, -wall) * Rectangle(
        wall, slot_h + wall, align=(Align.MIN, Align.MIN)
    )
    # Top lip tilted as a whole (constant thickness = wall, so it doesn't look
    # like it grows): full slot height at the back wall, narrowing toward the
    # mouth so the lip pinches the flat of the tabletop inboard. Its back edge
    # stays flush with the back wall top.
    drop = top_len * math.tan(lip_angle * DEG)
    top = Polygon(
        (0, slot_h),                        # back-bottom: full slot height
        (top_len, slot_h - drop),           # mouth-bottom: narrowed, grips inboard
        (top_len, slot_h - drop + wall),    # mouth-top
        (0, slot_h + wall),                 # back-top: flush with back wall
        align=None,
    )
    bottom = Pos(0, -wall) * Rectangle(
        bottom_len, wall, align=(Align.MIN, Align.MIN)
    )

    # The lower lip reaches inward until it meets the cabinet's front face at
    # Y = bottom_len. The hook hangs down from there, its flat back flush
    # against that face, curling out (toward the table front) and up. Its rod is
    # as deep (in Y) as the clip walls, so it reads as the same thickness.
    x0 = bottom_len - wall / 2
    z0 = -wall - hook_len
    stem = Line((x0, 0), (x0, z0))
    curl = CenterArc((x0 - hook_r, z0), hook_r, start_angle=0, arc_size=-hook_arc)
    hook = trace(stem + curl, line_width=wall)

    # Clip spans the full width; the hook is a narrower peg pushed to one side so
    # a face of it is flush with the clip's side face (easier to print flat).
    clip = extrude(Plane.YZ * (back + top + bottom), amount=width / 2, both=True)
    hook = Pos(-width / 2, 0, 0) * extrude(Plane.YZ * hook, amount=hook_w)
    mitten_hook = fillet((clip + hook).edges(), radius=fillet_r)

    show(mitten_hook)
    export(mitten_hook)
