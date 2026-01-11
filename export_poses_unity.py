import numpy as np
import json

poses = np.load("poses.npy")  # (N, 4, 4)

# OpenCV → Unity conversion matrix
Z_FLIP = np.diag([1, 1, -1, 1])

unity_poses = []

for i, pose in enumerate(poses):
    unity_pose = pose @ Z_FLIP

    unity_poses.append({
        "id": int(i),
        "position": unity_pose[:3, 3].tolist(),
        "rotation": unity_pose[:3, :3].tolist()
    })

with open("unity_camera_poses.json", "w") as f:
    json.dump(unity_poses, f, indent=4)

print(f"Exported {len(unity_poses)} Unity camera poses")
