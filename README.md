# SfM and NeRF-Based 3D Reconstruction of Real World Environment for VR Navigation

## Project Overview
This project demonstrates how a real indoor environment can be reconstructed from a simple phone video and transformed into a walkable VR scene.

The system combines **computer vision, neural scene representation, geometry extraction, and VR integration** to create an end-to-end pipeline that converts monocular video into an walkable virtual environment.

The pipeline first estimates camera movement and sparse 3D structure using Structure-from-Motion (SfM). The estimated camera poses are then used to train a NeRF model, which learns a continuous neural representation of the scene. Geometry is extracted from the learned density field and converted into a mesh that can be imported into Unity for VR navigation.

The goal of the project is to show how real-world environments captured with a phone camera can be reconstructed and deployed into immersive XR systems for simulation, spatial understanding, and defense-oriented indoor navigation scenarios.

## Demo Preview
- capture.mov 
![corner_wall](https://github.com/user-attachments/assets/4c74be52-683d-4902-8a0f-a29eac470125)

- SfM result
  
<img width="963" height="787" alt="SfM-graph" src="https://github.com/user-attachments/assets/6445e83c-bcdd-4efd-aa44-1cb7e9182c35" />
The SfM visualization shows the estimated movement of the phone camera and rough 3D structure reconstructed from the video. The red path represents the camera trajectory, while the blue points represent reconstructed scene features. Bundle Adjustment refines both the camera motion and 3D points to improve reconstruction accuracy before NeRF training.

- NeRF mesh / Reconstructed corner wall

<img width="1512" height="857" alt="NeRF_mesh" src="https://github.com/user-attachments/assets/d2257e8e-4c90-4a5a-98e3-92f08d282e86" />
<img width="1512" height="878" alt="corner_wall" src="https://github.com/user-attachments/assets/0bb9881a-c0fc-4bf6-a12c-763c46443db4" />
NeRF learns a neural 3D representation of the environment from video frames by predicting color and density for any 3D location. High-density regions correspond to physical surfaces such as walls and corners. After training, the learned density field is sampled and converted into a polygon mesh, producing the reconstructed corner-wall structure. Unlike the sparse SfM point cloud, the NeRF mesh represents continuous surfaces and usable geometry. This conversion is necessary because Unity requires explicit mesh geometry and colliders for rendering, navigation, and VR interaction, while raw NeRF density fields cannot be directly used inside game engines.

## What This Project Is Trying to Show
This project is trying to demonstrate three major ideas:

1. A monocular phone video can be used to estimate real-world 3D structure.
2. Neural scene representations such as NeRF can learn continuous volumetric geometry from images.
3. Neural reconstructions can be converted into explicit mesh geometry that supports real-time VR interaction inside Unity.

Rather than only generating rendered images, the project focuses on transforming learned neural representations into usable geometric environments for navigation and simulation.

## Pipeline Overview
1. Phone Video
2. Frame Extraction
3. Structure-from-Motion (Camera Poses + Sparse Points)
4. Bundke Adjustment
5. NeRF Training (RGB + Density)
6. Density Sampling & Geometry Extraction
7. Mesh Construction (Corner Wall)
8. Unity Integration (VR Walkable Scene)


## Technical Details

### 1. Structure-from-Motion Algorithm
```text
  Input:
      Monocular video frames I1, I2, ..., In
      Camera intrinsic matrix K
  
  Output:
      Camera poses
      Sparse 3D point cloud
  
  Initialize:
      camera_poses = []
      point_cloud = []
  
  Set initial camera pose:
      R0 = Identity matrix
      t0 = Zero vector
  
  Store initial pose:
      camera_poses.append((R0, t0))
  
  For each consecutive image pair (Ii, Ii+1):
  
      Detect ORB features:
          keypoints1, descriptors1 = ORB(Ii)
          keypoints2, descriptors2 = ORB(Ii+1)
  
      Match descriptors using Hamming distance:
          matches = BFMatcher(descriptors1, descriptors2)
  
      Remove incorrect matches using RANSAC
  
      If number of valid matches is too small:
          continue
  
      Extract matched feature coordinates:
          pts1, pts2
  
      Estimate Essential Matrix:
          E = findEssentialMat(pts1, pts2, K)
  
      Recover relative camera pose:
          (R, t) = recoverPose(E, pts1, pts2)
  
      Compute global camera pose:
          Ri+1 = R * Ri
          ti+1 = R * ti + t
  
      Store camera pose:
          camera_poses.append((Ri+1, ti+1))
  
      Construct projection matrices:
          P1 = K [Ri | ti]
          P2 = K [Ri+1 | ti+1]
  
      Triangulate matched feature points:
          X = triangulatePoints(P1, P2, pts1, pts2)
  
      Add triangulated points to sparse point cloud:
          point_cloud.append(X)
  
  Perform Bundle Adjustment:
      Optimize:
          camera intrinsics
          camera extrinsics
          3D point locations
  
      Minimize reprojection error across all observations
  
  Return:
      optimized camera poses
      optimized sparse 3D point cloud
```

### 2. NeRF Training Algorithm
```text
  Input:
      Training images
      Camera poses
      Camera intrinsics
  
  Output:
      Trained NeRF model
  
  Initialize NeRF network Fθ with random weights
  
  For epoch = 1 to E:
  
      Randomly sample training image Ii
      Retrieve corresponding camera pose Ti
  
      For each sampled pixel (u, v):
  
          Generate camera ray:
              ray origin o
              ray direction d
  
          Sample N points along the ray:
              x1, x2, ..., xN
  
          For each sampled point xi:
  
              Apply positional encoding:
                  γ(xi)
  
              Query NeRF network:
                  (color ci, density σi) = Fθ(γ(xi))
  
          Perform volume rendering:
  
              Compute opacity values:
                  αi = 1 - exp(-σi Δi)
  
              Compute transmittance:
                  Ti = Πj<i (1 - αj)
  
              Compute rendering weights:
                  wi = Ti * αi
  
              Render pixel color:
                  Ĉ = Σi wi ci
  
          Compare rendered color with ground truth:
              Loss = ||Ĉ - C||²
  
      Backpropagate loss
  
      Update network parameters using gradient descent
  
  Return trained NeRF model
```

### 3. Density-Based Geometry Extraction
After NeRF training, the system samples the learned density field across 3D space to identify where physical surfaces likely exist. High-density regions corresponding to walls and occupied geometry are isolated and converted into a point cloud. Plane detection is then used to identify the two perpendicular wall surfaces that form the corner structure.

### 4. Mesh Construction
The detected wall planes are converted into an explicit 3D mesh representing the reconstructed corner wall. The system adjusts plane orientation and edge alignment to create cleaner geometry, and the final mesh is exported as an OBJ file for use in real-time engines such as Unity. 

## Results
- Successfully reconstructed a **perpendicular corner wall** from phone video
- Converted implicit NeRF representation into explicit geometry
- Achieved stable VR navigation with collision-enabled walls

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
