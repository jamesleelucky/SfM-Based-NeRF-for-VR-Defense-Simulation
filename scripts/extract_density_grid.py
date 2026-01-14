import torch
import numpy as np
from tqdm import tqdm

# --------------------------------
# CONFIG
# --------------------------------
GRID_RES = 256          # 128 if your GPU is weak
BOUND = 1.0             # scene assumed in [-1,1]
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --------------------------------
# LOAD NeRF MODEL
# --------------------------------
# IMPORTANT:
# Replace this with how YOUR NeRF model is loaded
from train_render_nerf import NeRF

nerf = NeRF()
nerf.load_state_dict(torch.load("nerf_rgb.pt", map_location=DEVICE))
nerf.eval().to(DEVICE)

# --------------------------------
# CREATE GRID
# --------------------------------
xs = np.linspace(-BOUND, BOUND, GRID_RES)
ys = np.linspace(-BOUND, BOUND, GRID_RES)
zs = np.linspace(-BOUND, BOUND, GRID_RES)

density = np.zeros((GRID_RES, GRID_RES, GRID_RES), dtype=np.float32)

# --------------------------------
# SAMPLE DENSITY
# --------------------------------
with torch.no_grad():
    for i, x in enumerate(tqdm(xs)):
        for j, y in enumerate(ys):
            pts = np.stack([[x, y, z] for z in zs])
            pts = torch.from_numpy(pts).float().to(DEVICE)

            # ---- KEY LINE ----
            # Your NeRF MUST expose density (sigma)
            sigma = nerf.query_density(pts)   # shape (N,)

            density[i, j, :] = sigma.cpu().numpy()

np.save("density.npy", density)
print("Saved density.npy")
