from build123d import *  # Also works with cadquery objects!
from bd_warehouse.fastener import SocketHeadCapScrew, HexNut, ClearanceHole
import copy

thickness = 1.5

box_h = 120.0 - thickness
box_w = 68.2 -  thickness
box_l = 78.0 - thickness

pocket_l = 78.0
pocket_off = 34.0
pocket_sloped = 5
pocket_d = 5.5
pocket_fillet = 3
pocket_cover = 7.0

bag_w = 65.2
bag_h = 75.0

opening_off = 5.0
opening_h = pocket_off - opening_off
opening_gap = thickness + 2
opening_d = 5.0
opening_bottom_w = 21.2
opening_bottom_l = 62.10
opening_fillet = 3.0
opening_bottom_fillet = 7.0

cap_fill_w = 3.0
cap_fill_a = 45.0
cap_fillet = 0.30
cap_tolerance = 0.20

fillet_amount = 0.5

hook_a = 85.0
hook_thickness = 3
hook_w = 25.0
hook_d = 40.0
hook_h = 25.0
hook_overhang = 15
hook_screw_1_y = 8
hook_screw_2_y = 8 + hook_d/2
hook_fillet = 1.0

def run(show, export):
    with BuildPart() as shell:
        # base shell
        Box(box_w, box_l, box_h)
        topf = shell.faces().sort_by(Axis.Z)[-1]
        frontf = shell.faces().sort_by(Axis.Y)[0].rotate(Axis.Y, 90).translate((0, 0, -box_h/2))
        bottomf = shell.faces().sort_by(Axis.Z)[0].translate((0, -box_l/2, 0))
        sidef = shell.faces().sort_by(Axis.X)[0]
        offset(amount=thickness, openings=topf)
        shellfront = shell.faces().sort_by(Axis.Y)[0]

        # opening bottom
        with BuildSketch(bottomf.offset(-opening_off+opening_fillet/2).translate((0, -thickness, 0))) as b1:
            Rectangle(box_w, opening_gap, align=(Align.CENTER, Align.MAX))
            with Locations((0, -opening_gap)):
                Rectangle(opening_bottom_w, opening_bottom_l, align=(Align.CENTER, Align.MAX))
            v=b1.vertices().filter_by_position(axis=Axis.X, minimum=-opening_bottom_w/2, maximum=opening_bottom_w/2)
            fillet(v, radius=opening_bottom_fillet)
        extrude(amount=thickness+opening_off, mode=Mode.SUBTRACT)

        # opening trapezoid
        with BuildSketch(frontf) as trapez:
            Rectangle(box_w, opening_off, align=(Align.CENTER, Align.MIN))
            with Locations((0, opening_off)):
                Trapezoid(box_w, opening_h, 45, align=(Align.CENTER, Align.MIN))
            fillet(trapez.vertices(), radius=opening_fillet)
        extrude(amount=thickness, mode=Mode.SUBTRACT)

        # cap back opening
        with BuildSketch(frontf.translate((-box_w/2, 0, box_h))) as c:
            Rectangle(box_w, cap_fill_w, align=(Align.MIN, Align.MAX))
        extrude(amount=-box_l-thickness, mode=Mode.SUBTRACT)

    with BuildPart() as pocket:
        # pocket
        with BuildSketch(frontf.translate((0, 0, pocket_off+thickness/2))):
            Rectangle(box_w, pocket_l-thickness/2, align=(Align.CENTER, Align.MIN))
        with BuildSketch(frontf.translate((0, 0, pocket_off+pocket_sloped)).offset(pocket_d)):
            Rectangle(box_w, pocket_l-pocket_sloped, align=(Align.CENTER, Align.MIN))
        loft()
        pocket_top = pocket.faces().sort_by(Axis.Z)[-1]
        offset(amount=thickness, openings=[pocket_top])
        extrude(to_extrude=shellfront, amount=-thickness*2, mode=Mode.SUBTRACT)
        with BuildSketch(frontf.translate((0, 0, pocket_off+pocket_sloped+pocket_d/2))) as r:
            Rectangle(box_w-pocket_d, pocket_l-pocket_sloped-pocket_d/2, align=(Align.CENTER, Align.MIN))
            with Locations((0, pocket_l-pocket_sloped-pocket_d/2)):
                Rectangle(box_w+10, 10, align=(Align.CENTER, Align.MIN))
            v=r.vertices().filter_by_position(axis=Axis.X, minimum=-box_w/2, maximum=box_w/2)
            fillet(v, radius=pocket_fillet)
        extrude(amount=100, mode=Mode.SUBTRACT)

    with BuildPart() as cap_holder:
        with BuildSketch(frontf.translate((-box_w/2, 0, box_h))) as c1:
            Triangle(a=cap_fill_w, b=cap_fill_w, C=90, rotation=180, align=(Align.MAX, Align.MIN))
            mirror(about=Plane.YZ.offset(box_w/2))
        extrude(amount=-box_l-thickness)
        f1, f2, *_ = cap_holder.edges().sort_by_distance(topf.center());
        fillet([f1, f2], radius=cap_fillet)

    holder = shell.part + pocket.part + cap_holder.part
    LinearJoint(label="cap", to_part=holder, axis=Axis.Y)

    # screw
    screw = SocketHeadCapScrew(size="M2-0.4", length=4, simple=True)
    nut = HexNut(size="M2-0.4")

    # cap
    with BuildPart() as cap:
        with BuildSketch(frontf.translate((-box_w/2, 0, box_h))) as c2:
            Triangle(a=cap_fill_w+cap_tolerance, b=cap_fill_w-cap_tolerance, C=90, rotation=0, align=(Align.MIN, Align.MAX))
            mirror(about=Plane.YZ.offset(box_w/2))
            make_hull()
        extrude(amount=-(box_l+thickness))
        f1, *_, f2 = cap.edges().sort_by(Axis.X);
        fillet([f1, f2], radius=cap_fillet)
        with Locations(-topf.translate((0, -box_l/2 + hook_screw_1_y, -cap_fill_w))):
            h1=ClearanceHole(nut, captive_nut=True)
            LinearJoint(label="nut1", axis=Axis.Z.located(nut.hole_locations[-1]))
        with Locations(-topf.translate((0, -box_l/2 + hook_screw_2_y, -cap_fill_w))):
            ClearanceHole(nut, captive_nut=True)
            LinearJoint(label="nut2", axis=Axis.Z.located(nut.hole_locations[-1]))
        RigidJoint(label="holder", joint_location=cap.location)
        h1p = h1.position + Vector(0, 0, cap_fill_w + hook_thickness)
        RigidJoint(label="hook_screw_1", joint_location=Location(h1p, h1.orientation))
    cap = cap.part

    #hook
    with BuildPart() as hook:
        with BuildSketch(topf.translate((0, 0, 0))) as h:
            Rectangle(hook_w, hook_d+hook_overhang, align=(Align.CENTER, Align.MAX))
        extrude(amount=hook_thickness)
        with BuildSketch(sidef.translate((box_w/2, -hook_d-hook_overhang-thickness+hook_thickness/2, box_h/2+hook_thickness))):
            with BuildLine(Plane.YZ) as l:
                s1 = Line((0, 0), (hook_thickness, 0))
                s2 = PolarLine(s1 @ 0, hook_h + hook_thickness, 90)
                s3 = PolarLine(s1 @ 1, hook_h, 90)
                s4 = PolarLine(s2 @ 1, hook_d + hook_thickness, hook_a-90)
                s5 = PolarLine(s3 @ 1, hook_d, hook_a-90)
                s6 = Line(s4 @ 1, s5 @ 1 )
            make_face()
            mirror(about=Plane.XZ, mode=Mode.REPLACE)
        extrude(amount=hook_w/2, both=True)
        with Locations(topf.translate((0, -box_l/2 + hook_screw_1_y, hook_thickness))):
            h1=ClearanceHole(screw, counter_sunk=True)
            LinearJoint(label="screw1", axis=Axis.Z.located(screw.hole_locations[-1]))
        with Locations(topf.translate((0, -box_l/2 + hook_screw_2_y, hook_thickness))):
            ClearanceHole(screw, counter_sunk=True)
            LinearJoint(label="screw2", axis=Axis.Z.located(screw.hole_locations[-1]))
        RigidJoint(label="cap_screw_1", joint_location=-h1.location)
    hook = hook.part

    nut1 = copy.copy(nut)
    nut2 = copy.copy(nut)
    screw1 = copy.copy(screw)
    screw2 = copy.copy(screw)

    holder.joints["cap"].connect_to(cap.joints["holder"], position=75)

    cap.joints["nut1"].connect_to(nut1.joints["b"], position=5)
    cap.joints["nut2"].connect_to(nut2.joints["b"], position=5)
    cap.joints["hook_screw_1"].connect_to(hook.joints["cap_screw_1"], position=5)

    hook.joints["screw1"].connect_to(screw1.joints["a"], position=5)
    hook.joints["screw2"].connect_to(screw2.joints["a"], position=5)


    assembly = Compound(
        children=[holder, cap, hook, nut1, nut2, screw1, screw2]
    )
    show(assembly)
    export(holder, cap, hook)

