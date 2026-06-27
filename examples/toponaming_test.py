from build123d import *
from build123d.topology.naming.indexed_name import IndexedName
from build123d.topology.naming.mapped_name import MappedName
import build123d.topology.utils as GeomUtils
from ocp_vscode import *

set_port(3939)

with BuildPart() as basicPart:
    with BuildSketch(Plane.XY) as sk1:
        r = Rectangle(20, 25)
        r.tag = "Rect1"
    # extrude(sk1.face(), amount = 10)
    extShape = GeomUtils._makeNamedExtrusion(sk1.face(), Vector(0, 0, 10), "Ext1")

print(f"extShape tag: {extShape.tag}")

show(extShape, port = 3939)