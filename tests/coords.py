from src.geometric_tools import spherical_to_cartesian_coords, cartesian_to_spherical_coords
import numpy as np 

cartesian = np.random.rand(100, 3)
spherical = cartesian_to_spherical_coords(cartesian)
new_cartesian = spherical_to_cartesian_coords(spherical)
assert np.allclose(cartesian, new_cartesian)
print('OK')