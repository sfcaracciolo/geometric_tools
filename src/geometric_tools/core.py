from typing import Tuple, Union, List
import numpy as np 
from open3d.utility import Vector3dVector, Vector3iVector
from open3d.geometry import PointCloud, TriangleMesh
from open3d.core import Tensor, float32, uint32
from open3d.t.geometry import RaycastingScene

def scene_surface(vertices: Vector3dVector, triangles: Vector3iVector) -> RaycastingScene:
    t_vertices = Tensor(np.asarray(vertices), float32)
    t_triangles = Tensor(np.asarray(triangles), uint32)
    scene = RaycastingScene()
    _ = scene.add_triangles(t_vertices, t_triangles)
    return scene

def project_to_surface(vertices: np.ndarray, surface: RaycastingScene) -> np.ndarray:
    t_vertices = Tensor(vertices, float32)
    return surface.compute_closest_points(t_vertices)['points'].numpy()

def triangle_mesh_by_convex_hull_of_inner_sphere(vertices:Union[np.ndarray, Vector3dVector]) -> np.ndarray:
    center, radius = compute_inner_sphere(vertices)
    projected_vertices = project_to_sphere(vertices, center, radius/2.)
    triangle_mesh, indices = compute_convex_hull(projected_vertices)
    return triangle_mesh, indices

def compute_convex_hull(vertices:Union[np.ndarray, Vector3dVector]) -> Tuple[Union[TriangleMesh, List[int]]]:
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
    ρ, φ, θ = spherical[:,0], spherical[:,1], spherical[:,2]
    ρ[:] = np.linalg.norm(vertices, axis=1) 
    φ[:] = np.arccos(z/ρ)
    θ[:] = np.arctan2(y, x)
    return spherical

def spherical_to_cartesian_coords(vertices:Union[np.ndarray, Vector3dVector]) -> np.ndarray:
    if isinstance(vertices, Vector3dVector): vertices = np.asarray(vertices)
    ρ, φ, θ = vertices[:,0], vertices[:,1], vertices[:,2]
    cartesian = np.empty_like(vertices)
    x, y, z = cartesian[:,0], cartesian[:,1], cartesian[:,2]
    x[:] = ρ*np.sin(φ)*np.cos(θ)
    y[:] = ρ*np.sin(φ)*np.sin(θ)
    z[:] = ρ*np.cos(φ)
    return cartesian
