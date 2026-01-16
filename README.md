# SfM and NeRF-Based 3D Reconstruction of Real World Environment for VR Navigation

This project reconstructs a real-world corner wall from monocular video using Structure-from-Motion and NeRF, extracts geometric structure from learned density, and deploys the resulting environment as a walkable VR scene in Unity.

The system bridges **computer vision, neural scene representation, and immersive VR interaction** for defense and simulation-oriented environments.

## Demo Preview

> *Screenshots / GIFs to be uploaded here*
- NeRF novel view rendering
- Extracted mesh / reconstructed corner
- Unity VR walkable scene

## Motivation

Accurate indoor geometry reconstruction is critical for **VR-based training, simulation, and spatial reasoning** in constrained environments such as rooms, hallways, and corners.  
This project explores how **NeRF density fields** can be transformed into **usable geometry** for real-time VR navigation.


## Pipeline Overview

1. Phone Video
2. Frame Extraction
3. Structure-from-Motion (Camera Poses + Sparse Points)
4. NeRF Training (RGB + Density)
5. Density Sampling & Geometry Extraction
6. Mesh Construction (Corner Wall)
7. Unity Integration (VR Walkable Scene)


## Technical Details

### 1. Structure-from-Motion
- Feature matching and camera pose estimation
- Bundle Adjustment over ~170 camera views
- Outputs camera intrinsics and extrinsics for NeRF training

  #### Algorithm
  Initialize empty lists for camera poses, 3D points, and observations
  Set first camera pose:
      R0 = I
      t0 = 0
  for each consecutive image pair (Ii, Ii+1):
      Detect ORB features in both images
      Match descriptors using brute-force Hamming distance
  
      if number of matches < MIN_MATCHES:
          skip this image pair
  
      Estimate Essential Matrix E using RANSAC:
          E = findEssentialMat(pts1, pts2, K)
  
      Recover relative pose (R, t) from E
  
      Chain camera pose:
          Ri+1 = R · Ri
          ti+1 = R · ti + t
  
      Construct projection matrices:
          P1 = K [Ri | ti]
          P2 = K [Ri+1 | ti+1]
  
      Select inlier correspondences from RANSAC mask
  
      Triangulate 3D points:
          X = triangulatePoints(P1, P2, x1, x2)
  
      For each valid triangulated point:
          Store 3D point
          Store 2D observation in both cameras
          Record camera–point associations
  end for

### 2. NeRF Training
- MLP-based NeRF (RGB + density)
- Positional encoding for high-frequency geometry
- Trained on monocular video frames
- Novel view synthesis for validation

### 3. Density-Based Geometry Extraction
- Dense 3D grid sampling of NeRF density field
- Thresholding to isolate occupied regions
- Plane detection from density-derived point cloud
- Reconstruction of perpendicular wall planes

### 4. Mesh Construction
- Procedural generation of a corner wall mesh
- Corrected plane orientation and edge alignment
- Exported as OBJ for real-time engines

## Results

- Successfully reconstructed a **perpendicular corner wall** from phone video
- Converted implicit NeRF representation into explicit geometry
- Achieved stable VR navigation with collision-enabled walls

## Unity & VR Integration

- Imported reconstructed wall mesh into Unity
- Added physics colliders for walkable interaction
- Configured XR Origin and locomotion system
- Enabled keyboard-based VR simulation via XR Device Simulator
- Validated camera movement and head rotation without a physical headset

## How to Run

### Python (Reconstruction & NeRF)

- python extract_frames.py
- python track_sfm.py
- python bundle_adjust.py
- python export_nerf_data.py
- python intrinsics.py
- python prepare_nerf.py
- python train_render_nerf.py
- python extract_density_grid.py
- python extract_mesh.py
- python extract_wall_pointcloud.py
- python fit_plane_RANSAC.py
- python export_wall_planes.py
- python wall_extend.py
- python build_corner_wall.py

### Unity (VR Scene)

- Open the Unity project
- Import corner_wall.obj into Assets/Models
- Add Box Collider to the wall mesh
- Add XR Origin (VR) to the scene
- Enable XR Device Simulator
- Press Play to walk and look around the reconstructed corner wall

### Tech Stack

- Python, NumPy, OpenCV
- PyTorch (NeRF implementation)
- Structure-from-Motion, Bundle Adjustment
- Unity (URP), XR Interaction Toolkit
- VR Device Simulation
