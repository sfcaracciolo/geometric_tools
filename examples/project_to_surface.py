from src.geometric_tools import * 
import zarr
import geometric_plotter

ZARR_PATH = 'E:\db.zarr'
root = zarr.open(ZARR_PATH, mode='r')
nodes = root['/sinus_pig/data/torso/electrodes'][:]

geometric_plotter.set_export()

center, radius = compute_inner_sphere(nodes)
sphere_nodes = project_to_sphere(nodes, center, radius/2.)
triangle_mesh, indices = compute_convex_hull(sphere_nodes)
vertices, triangles = nodes[indices], np.asarray(triangle_mesh.triangles)

ax = geometric_plotter.figure(figsize=(5,5))

geometric_plotter.plot_trisurf(ax, vertices, triangles, color='k', alpha=.5)

surface = scene_surface(vertices, triangles)
projected_nodes = project_to_surface(sphere_nodes, surface)

geometric_plotter.scatter(ax, projected_nodes, s=25, color='red', alpha=1)
geometric_plotter.config_ax(ax, (50,-150,0), 1.)
geometric_plotter.execute(folder='E:\Repositorios\geometric_tools\export\\', name='project_to_surface')
