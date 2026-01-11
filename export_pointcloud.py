import numpy as np
from plyfile import PlyData, PlyElement

pts = np.load("sfm_data.npz")["points_3d"]
vertices = [(p[0], p[1], p[2]) for p in pts]

ply = PlyData([PlyElement.describe(
    np.array(vertices, dtype=[('x','f4'),('y','f4'),('z','f4')]),
    'vertex'
)])
ply.write("scene.ply")
