import numpy as np
import json

points = np.load("wall_points.npy")

# Project points to XZ plane (wall footprint)
xz = points[:, [0, 2]]

# Compute bounding box
min_x, min_z = xz.min(axis=0)
max_x, max_z = xz.max(axis=0)

# Height extents
min_y = points[:,1].min()
max_y = points[:,1].max()

wall_dimensions = {
    "width": float(max_x - min_x),
    "height": float(max_y - min_y),
    "depth": 0.1,  # fixed wall thickness
    "center": points.mean(axis=0).tolist()
}

with open("wall_dimensions.json", "w") as f:
    json.dump(wall_dimensions, f, indent=4)

print("Saved wall_dimensions.json")

