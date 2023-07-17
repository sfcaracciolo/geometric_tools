from open3d.visualization import draw_geometries 
from open3d.geometry import PointCloud, TriangleMesh
from open3d.utility import Vector3dVector
from src.geometric_tools import triangle_mesh_by_convex_hull_of_inner_sphere
import zarr 

ZARR_PATH = 'E:\db.zarr'
root = zarr.open(ZARR_PATH, mode='r')
nodes = root['/sinus_pig/data/torso/electrodes'][:]
vertices = Vector3dVector(nodes)

sphere_triangle_mesh, indices = triangle_mesh_by_convex_hull_of_inner_sphere(vertices)
new_vertices = Vector3dVector(nodes[indices])
pig_triangle_mesh = TriangleMesh(new_vertices, sphere_triangle_mesh.triangles)
pcd = PointCloud(vertices)
draw_geometries([pcd, sphere_triangle_mesh, pig_triangle_mesh], mesh_show_back_face=True, mesh_show_wireframe=True) 