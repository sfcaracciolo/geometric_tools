from typing import Tuple, Union
import numpy as np 
from open3d.utility import Vector3dVector, Vector3iVector
from open3d.geometry import PointCloud, TriangleMesh
from open3d.core import Tensor, float32, uint32
from open3d.t.geometry import RaycastingScene
from vector_tools import TriPoint

def scene_surface(vertices: Vector3dVector, triangles: Vector3iVector) -> RaycastingScene:
    t_vertices = Tensor(np.asarray(vertices), float32)
    t_triangles = Tensor(np.asarray(triangles), uint32)
    scene = RaycastingScene()
    _ = scene.add_triangles(t_vertices, t_triangles)
    return scene

def project_to_surface(vertices: np.ndarray, surface: RaycastingScene) -> np.ndarray:
    t_vertices = Tensor(vertices, float32)
    return surface.compute_closest_points(t_vertices)['points'].numpy()

def triangle_mesh_by_convex_hull_of_inner_sphere(vertices:Union[np.ndarray, Vector3dVector]) -> Tuple[Union[TriangleMesh, Tuple[int]]]:
    center, radius = compute_inner_sphere(vertices)
    projected_vertices = project_to_sphere(vertices, center, radius/2.)
    triangle_mesh, indices = compute_convex_hull(projected_vertices)
    return triangle_mesh, indices

def compute_convex_hull(vertices:Union[np.ndarray, Vector3dVector]) -> Tuple[Union[TriangleMesh, Tuple[int]]]:
    if isinstance(vertices, np.ndarray): vertices = Vector3dVector(vertices)
    pcd = PointCloud(vertices)
    return pcd.compute_convex_hull()

def compute_inner_sphere(vertices:Union[np.ndarray, Vector3dVector]) -> Tuple[Union[np.ndarray, float]]:
    if isinstance(vertices, np.ndarray): vertices = Vector3dVector(vertices)
    pcd = PointCloud(vertices)
    center = pcd.get_center()[np.newaxis, :]
    distances_to_center = pcd.compute_point_cloud_distance(PointCloud(Vector3dVector(center)))
    max_radius = np.asarray(distances_to_center).min()
    return center, max_radius

def project_to_sphere(vertices:Union[np.ndarray, Vector3dVector], center: np.ndarray, radius: float) -> np.ndarray:
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    m = vertices - center
    m /= np.linalg.norm(m, axis=1, keepdims=True)
    return center + radius * m

def cartesian_to_spherical_coords(vertices:Union[np.ndarray, Vector3dVector]) -> np.ndarray:
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    x, y, z = vertices[:,0], vertices[:,1], vertices[:,2]
    spherical = np.empty_like(vertices)
    ρ, θ, φ = spherical[:,0], spherical[:,1], spherical[:,2]
    ρ[:] = np.linalg.norm(vertices, axis=1) 
    θ[:] = np.arccos(z/ρ)
    φ[:] = np.arctan2(y, x)
    return spherical

def spherical_to_cartesian_coords(vertices:Union[np.ndarray, Vector3dVector]) -> np.ndarray:
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    ρ, θ, φ = vertices[:,0], vertices[:,1], vertices[:,2]
    cartesian = np.empty_like(vertices)
    x, y, z = cartesian[:,0], cartesian[:,1], cartesian[:,2]
    x[:] = ρ*np.sin(θ)*np.cos(φ)
    y[:] = ρ*np.sin(θ)*np.sin(φ)
    z[:] = ρ*np.cos(θ)
    return cartesian

def interp_vertices_values_to_triangles(vertices:Union[np.ndarray, Vector3dVector], triangles:Union[np.ndarray, Vector3iVector], values: np.ndarray, method:str='bary') -> np.ndarray:
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    if isinstance(triangles, Vector3iVector): triangles = np.asarray(triangles)
    
    T = triangles.shape[0]
    interp_values = np.empty(T, dtype=np.float32)
    for t_index in range(T):
        t_indices = triangles[t_index]
        interp_values[t_index] = TriPoint.barycentric_interp(vertices[t_indices], values[t_indices])
    return interp_values

def compute_triangle_normals(vertices:Union[np.ndarray, Vector3dVector], triangles:Union[np.ndarray, Vector3iVector], normalize=True):
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    if isinstance(triangles, Vector3iVector): triangles = np.asarray(triangles)
    
    T = triangles.shape[0]
    triangle_normals = np.empty((T, 3), dtype=np.float32)
    for t_index in range(T):
        t_indices = triangles[t_index]
        triangle_normals[t_index] = TriPoint.normal(vertices[t_indices], normalize=normalize)
    return triangle_normals 

def compute_triangle_barycenters(vertices:Union[np.ndarray, Vector3dVector], triangles:Union[np.ndarray, Vector3iVector], normalize=True):
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    if isinstance(triangles, Vector3iVector): triangles = np.asarray(triangles)
    
    T = triangles.shape[0]
    triangle_barycenters = np.empty((T, 3), dtype=np.float32)
    for t_index in range(T):
        t_indices = triangles[t_index]
        triangle_barycenters[t_index] = TriPoint.barycenter(vertices[t_indices])
    return triangle_barycenters
