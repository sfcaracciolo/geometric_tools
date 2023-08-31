from open3d.geometry import TriangleMesh
from geometric_plotter import Plotter
import pathlib
import numpy as np 
from src import geometric_tools

filename = pathlib.Path(__file__).stem

# create cylinder surface
mesh = TriangleMesh().create_cylinder(radius=1.0, height=2.0, resolution=20, split=4)
surface = geometric_tools.scene_surface(mesh.vertices, mesh.triangles)

# create inner sphere mesh
center, radius = geometric_tools.compute_inner_sphere(mesh.vertices)
sphere_nodes = geometric_tools.project_to_sphere(mesh.vertices, center, radius/2.)

# projection
projected_nodes = geometric_tools.project_to_surface(sphere_nodes, surface)

Plotter.set_export()

p0 = Plotter(figsize=(5,5))
p0.add_trisurf(np.asarray(mesh.vertices), np.asarray(mesh.triangles), alpha=.1)
p0.add_scatter(projected_nodes, s=50, color='r')
p0.camera(view=(25, 0, 0), zoom=1.)
p0.save(folder='figs/', name=filename)

Plotter.show()
