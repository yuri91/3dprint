import os
import cadquery as cq

self_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = self_dir + "/../imports/temper-bottomplate.dxf"

main_wire = (
    cq.importers.importDXF(profile_path, tol=1e-1, include=["main"]).wires().toPending()
)
holes = (
    cq.importers.importDXF(profile_path, tol=1e-1, include=["hole1","hole2","hole3","hole4","hole5"]).wires().toPending()
)

plate_thickness = 3.2
hole_bottom_thickness = 0.2
border_tolerance = 0.2
border_thickness = 0.6
border_height = 7.6
screw_diameter = 3.2
pillar_diameter = 5
pillar_height = 1.5
switch_offset = 9
switch_length = 6.6
switch_height = 2.5

shell_inner = cq.Workplane().add(main_wire.val().offset2D(border_tolerance))
shell_outer = cq.Workplane().add(main_wire.val().offset2D(border_tolerance + border_thickness))

main = shell_inner.toPending().extrude(plate_thickness)

hole_centers = [h.Center().toTuple()[0:2] for h in holes.objects]

pillars = main.faces(">Z").workplane().pushPoints(hole_centers).circle(pillar_diameter/2).extrude(pillar_height)

holes = pillars.faces(">Z").workplane().pushPoints(hole_centers).hole(screw_diameter, pillar_height + plate_thickness - hole_bottom_thickness)

shell = cq.Workplane().add(shell_inner.val()).add(shell_outer.val()).toPending().extrude(border_height) + holes


start_point = main_wire.vertices(">X").objects[0].Center()

case = shell.faces(">Z").workplane().moveTo(start_point.x, start_point.y+switch_offset).rect(4, switch_length, centered=False).cutBlind(-switch_height)

mirror = case.mirror("YZ")
