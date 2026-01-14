import json
import numpy as np

# Load points
plane1 = np.load("nerf_points.npy")   # large
plane2 = np.load("wall_points.npy")   # large

MAX_POINTS = 5000   # SAFE for SVD

def subsample(points, max_n=MAX_POINTS):
    if len(points) > max_n:
        idx = np.random.choice(len(points), max_n, replace=False)
        return points[idx]
    return points

def plane_normal_and_center(points):
    points = subsample(points)
    center = points.mean(axis=0)

    # PCA via SVD
    _, _, Vt = np.linalg.svd(points - center, full_matrices=False)
    normal = Vt[-1]
    normal = normal / np.linalg.norm(normal)

    return normal.tolist(), center.tolist()

n1, c1 = plane_normal_and_center(plane1)
n2, c2 = plane_normal_and_center(plane2)

data = {
    "walls": [
        {"normal": n1, "center": c1},
        {"normal": n2, "center": c2}
    ]
}

with open("wall_planes.json", "w") as f:
    json.dump(data, f, indent=4)

print("Saved wall_planes.json")
