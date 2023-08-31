from open3d.geometry import TriangleMesh
from geometric_plotter import Plotter
import pathlib
import numpy as np
from src import geometric_tools

filename = pathlib.Path(__file__).stem

mesh = TriangleMesh().create_sphere(radius=1, resolution=10)

normals = geometric_tools.compute_triangle_normals(mesh.vertices, mesh.triangles)
centers = geometric_tools.compute_triangle_barycenters(mesh.vertices, mesh.triangles)

Plotter.set_export()

p0 = Plotter(figsize=(5,5))
p0.add_quiver(centers, normals, length=.2, color='k')
p0.add_trisurf(np.asarray(mesh.vertices), np.asarray(mesh.triangles), alpha=.1)
p0.camera(view=(0, 0, 0), zoom=1.5)
p0.save(folder='figs/', name=filename)

Plotter.show()