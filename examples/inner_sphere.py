from src.geometric_tools import compute_inner_sphere, project_to_sphere
import zarr
import geometric_plotter

ZARR_PATH = 'E:\db.zarr'
root = zarr.open(ZARR_PATH, mode='r')
nodes = root['/sinus_pig/data/torso/electrodes'][:]

geometric_plotter.set_export()

ax = geometric_plotter.figure(figsize=(5,5))

geometric_plotter.scatter(ax, nodes, s=10, color='k')

center, radius = compute_inner_sphere(nodes)
projected_nodes = project_to_sphere(nodes, center, radius/2.)

geometric_plotter.scatter(ax, projected_nodes, s=10, color='red')

geometric_plotter.config_ax(ax, (50,-150,0), 1.)

geometric_plotter.execute(folder='E:\Repositorios\geometric_tools\export\\', name='inner_sphere')
