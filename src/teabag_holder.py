from build123d import *  # Also works with cadquery objects!

thickness = 1.5

box_h = 120.0
box_w = 68.2
box_l = 78.0

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
cap_tolerance = 0.15

fillet_amount = 0.5

hook_a = 85.0
hook_thickness = 2.5
hook_w = 25.0
hook_d = 40.0
hook_h = 25.0
hook_fillet = 1.0

def run(show):
    with BuildPart() as shell:
        # base shell
        Box(box_w, box_l, box_h)
        topf = shell.faces().sort_by(Axis.Z)[-1]
        frontf = shell.faces().sort_by(Axis.Y)[0].rotate(Axis.Y, 90).translate((0, 0, -box_h/2))
        bottomf = shell.faces().sort_by(Axis.Z)[0].translate((0, -box_l/2, 0))
        sidef = shell.faces().sort_by(Axis.X)[0].rotate(Axis.X, 90).translate((0, -box_l/2, -box_h/2))
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
            fillet(c1.vertices()[0], radius=cap_fillet)
            mirror(about=Plane.YZ.offset(box_w/2))
        extrude(amount=-box_l-thickness)

    holder = shell.part + pocket.part + cap_holder.part


    with BuildPart() as cap:
        with BuildSketch(frontf.translate((-box_w/2, 0, box_h))) as c2:
            Triangle(a=cap_fill_w+cap_tolerance, b=cap_fill_w-cap_tolerance, C=90, rotation=0, align=(Align.MIN, Align.MAX))
            fillet(c2.vertices()[0], radius=cap_fillet)
            mirror(about=Plane.YZ.offset(box_w/2))
            make_hull()
        extrude(amount=-(box_l+thickness))
        topf = cap.faces().sort_by(Axis.Z)[-1]
        with BuildSketch(sidef.translate((0, 0, box_h))) as h:
            Rectangle(hook_w, hook_d, align=(Align.MAX, Align.MIN))

    show(holder, cap, h, names=["holder", "cap", "h"])

