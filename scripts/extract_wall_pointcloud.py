import numpy as np
from sklearn.linear_model import RANSACRegressor

density = np.load("density.npy")  # (N,N,N)

GRID_RES = density.shape[0]
BOUND = 1.0
THRESH = 0.4

# Create grid
xs = np.linspace(-BOUND, BOUND, GRID_RES)
ys = np.linspace(-BOUND, BOUND, GRID_RES)
zs = np.linspace(-BOUND, BOUND, GRID_RES)

X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")

# Mask high-density points
mask = density > THRESH

points = np.stack([X[mask], Y[mask], Z[mask]], axis=1)

print("Total points:", points.shape[0])

np.save("nerf_points.npy", points)

# Remove floor + ceiling
y = points[:, 1]
wall_mask = (y > -0.3) & (y < 0.8)

wall_points = points[wall_mask]

print("Wall points:", wall_points.shape[0])

np.save("wall_points.npy", wall_points)

# downsample it before RANSAC 

MAX_POINTS = 50000

if wall_points.shape[0] > MAX_POINTS:
    idx = np.random.choice(wall_points.shape[0], MAX_POINTS, replace=False)
    wall_points = wall_points[idx]

print("Using points:", wall_points.shape[0])

# First plane: x = f(y, z)
X = wall_points[:, [1, 2]]   # y,z
Y = wall_points[:, 0]        # x

ransac1 = RANSACRegressor(residual_threshold=0.02)
ransac1.fit(X, Y)

inliers1 = ransac1.inlier_mask_
plane1 = wall_points[inliers1]
remaining = wall_points[~inliers1]

# Second plane: z = f(x, y)
X2 = remaining[:, [0, 1]]    # x,y
Y2 = remaining[:, 2]         # z

ransac2 = RANSACRegressor(residual_threshold=0.02)
ransac2.fit(X2, Y2)

plane2 = remaining[ransac2.inlier_mask_]

def plane_normal(points):
    mean = points.mean(axis=0)
    _, _, Vt = np.linalg.svd(points - mean)
    normal = Vt[-1]
    return normal / np.linalg.norm(normal), mean

n1, c1 = plane_normal(plane1)
n2, c2 = plane_normal(plane2)

print("Plane normals:")
print("Wall A:", n1)
print("Wall B:", n2)
print("Dot product (should be ~0):", np.dot(n1, n2))


