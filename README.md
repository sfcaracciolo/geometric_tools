# geometric tools

Some basic geometric operations based on Open3D like:

### compute_inner_sphere()

Compute parameters of a sphere which is inner of a point cloud given. The *center* is obtained through the geometry coordinates and the *radius* is the maximum possible to be enclosed by the point cloud.
### project_to_sphere()

Project a point cloud to a sphere based on centre and radius parameters. In this example, the centre and radius of the sphere were computed with ```compute_inner_sphere()``` and the radius was divided by two
<img src="export/inner_sphere.png" alt="drawing" width="200"/>

### project_to_surface()

Project a point cloud to a surface. In this example, the red inner sphere of above was projected to the triangle mesh. The implementation use RaycastingScene (open3d).
<img src="export/project_to_surface.png" alt="drawing" width="200"/>

### ...