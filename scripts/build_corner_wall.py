# import json
# import numpy as np

# # ----------------------------
# # LOAD DATA
# # ----------------------------
# with open("wall_planes.json") as f:
#     planes = json.load(f)["walls"]

# with open("wall_dimensions.json") as f:
#     dims = json.load(f)

# WIDTH = dims["width"]
# HEIGHT = dims["height"]

# WORLD_UP = np.array([0, 1, 0], dtype=np.float32)

# # ----------------------------
# # CLEAN NORMALS (KEY FIX)
# # ----------------------------
# def horizontal_normal(n):
#     """Project normal onto XZ plane and renormalize"""
#     n = np.array(n, dtype=np.float32)
#     n[1] = 0.0
#     n /= np.linalg.norm(n)
#     return n

# n1 = horizontal_normal(planes[0]["normal"])
# n2 = np.cross(WORLD_UP, n1)
# n2 /= np.linalg.norm(n2)

# # Hinge center (average)
# c1 = np.array(planes[0]["center"], dtype=np.float32)
# c2 = np.array(planes[1]["center"], dtype=np.float32)
# hinge = 0.5 * (c1 + c2)
# hinge[1] = c1[1]  # preserve height

# # ----------------------------
# # BUILD WALL
# # ----------------------------
# def build_wall(normal, hinge, side):
#     normal = normal / np.linalg.norm(normal)
#     right = np.cross(WORLD_UP, normal)
#     right /= np.linalg.norm(right)
#     up = WORLD_UP

#     # Push wall away from hinge
#     center = hinge + normal * (WIDTH / 2) * side

#     p1 = center + right * WIDTH/2 + up * HEIGHT/2
#     p2 = center - right * WIDTH/2 + up * HEIGHT/2
#     p3 = center - right * WIDTH/2 - up * HEIGHT/2
#     p4 = center + right * WIDTH/2 - up * HEIGHT/2

#     return [p1, p2, p3, p4]

# walls = [
#     build_wall(n1, hinge, +1),
#     build_wall(n2, hinge, +1)
# ]

# # ----------------------------
# # EXPORT OBJ
# # ----------------------------
# with open("corner_wall.obj", "w") as f:
#     v = 1
#     for wall in walls:
#         for p in wall:
#             f.write(f"v {p[0]} {p[1]} {p[2]}\n")
#         f.write(f"f {v} {v+1} {v+2}\n")
#         f.write(f"f {v} {v+2} {v+3}\n")
#         v += 4

# print("Saved corner_wall.obj (vertical, perpendicular, no overlap)")

import numpy as np

# ----------------------------
# PARAMETERS (meters)
# ----------------------------
WALL_LENGTH = 3.0     # horizontal extent
WALL_HEIGHT = 2.8     # vertical (tall)
WALL_THICKNESS = 0.02  # optional (not used for plane)

# Corner vertical edge (shared)
corner = np.array([0.0, 0.0, 0.0])

# Axes
UP = np.array([0, 1, 0])
X  = np.array([1, 0, 0])
Z  = np.array([0, 0, 1])

walls = []

# =====================================================
# WALL 1 (XZ corner side, facing +X)
# Shared vertical edge = (corner → corner + UP*HEIGHT)
# =====================================================
p1 = corner
p2 = corner + UP * WALL_HEIGHT
p3 = corner + UP * WALL_HEIGHT + X * WALL_LENGTH
p4 = corner + X * WALL_LENGTH

walls.append([p1, p2, p3, p4])

# =====================================================
# WALL 2 (XZ corner side, facing +Z)
# SAME shared vertical edge
# =====================================================
p5 = corner
p6 = corner + UP * WALL_HEIGHT
p7 = corner + UP * WALL_HEIGHT + Z * WALL_LENGTH
p8 = corner + Z * WALL_LENGTH

walls.append([p5, p6, p7, p8])

# ----------------------------
# EXPORT OBJ
# ----------------------------
with open("corner_wall.obj", "w") as f:
    idx = 1
    for wall in walls:
        for v in wall:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # two triangles per wall
        f.write(f"f {idx} {idx+1} {idx+2}\n")
        f.write(f"f {idx} {idx+2} {idx+3}\n")

        idx += 4

print("Tall vertical corner wall created correctly.")
