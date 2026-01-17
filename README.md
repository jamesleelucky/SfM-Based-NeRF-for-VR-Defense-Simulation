# SfM and NeRF-Based 3D Reconstruction of Real World Environment for VR Navigation

This project reconstructs a real-world corner wall from monocular video using Structure-from-Motion and NeRF, extracts geometric structure from learned density, and deploys the resulting environment as a walkable VR scene in Unity.

The system bridges **computer vision, neural scene representation, and immersive VR interaction** for defense and simulation-oriented environments.

## Demo Preview
- capture.mov 
![corner_wall](https://github.com/user-attachments/assets/4c74be52-683d-4902-8a0f-a29eac470125)
- SfM result 
<img width="963" height="787" alt="SfM-graph" src="https://github.com/user-attachments/assets/6445e83c-bcdd-4efd-aa44-1cb7e9182c35" />
- NeRF mesh / Reconstructed corner wall
<img width="1512" height="857" alt="NeRF_mesh" src="https://github.com/user-attachments/assets/d2257e8e-4c90-4a5a-98e3-92f08d282e86" />
<img width="1512" height="878" alt="corner_wall" src="https://github.com/user-attachments/assets/0bb9881a-c0fc-4bf6-a12c-763c46443db4" />
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

  #### Algorithm
  Initialize NeRF network Fθ with random weights

  for epoch = 1 to E:
      Sample a random image Ii and its camera pose Ti
  
      Generate rays for all pixels:
          For each pixel (u, v):
              Compute ray origin o and direction d using intrinsics and pose
  
      Randomly sample a batch of rays
  
      For each ray r = (o, d):
          Sample N points along the ray:
              z1, z2, ..., zN ∈ [tn, tf]
              xi = o + zi · d
  
          Apply positional encoding:
              γ(xi) = [xi, sin(2^k xi), cos(2^k xi)] for k = 0..L−1
  
          Query NeRF:
              (ci, σi) = Fθ(γ(xi))
  
      Perform volume rendering:
          Compute distances Δi between samples
          Compute alpha values:
              αi = 1 − exp(−σi Δi)
  
          Compute transmittance:
              Ti = ∏j<i (1 − αj)
  
          Compute weights:
              wi = Ti αi
  
          Render pixel color:
              Ĉ = Σi wi ci
  
      Compute loss:
          L = ||Ĉ − C||²
  
      Backpropagate loss and update θ
  
  end for
  
  Save trained NeRF model

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
