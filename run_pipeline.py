import subprocess
import sys

def run(cmd):
    print(f"\n▶ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

if __name__ == "__main__":
    # --------------------------------------------------
    # 1. Extract frames from video
    # --------------------------------------------------
    run("python scripts/extract_frames.py")

    # --------------------------------------------------
    # 2. Track-based SfM (creates sfm/sfm_data.npz)
    # --------------------------------------------------
    run("python data/sfm/track_sfm.py")

    # --------------------------------------------------
    # 3. Bundle Adjustment
    # --------------------------------------------------
    run("python scripts/bundle_adjust.py")

    # --------------------------------------------------
    # 4. Export NeRF camera poses
    # --------------------------------------------------
    run("python scripts/export_nerf_data.py")

    # --------------------------------------------------
    # 5. Estimate intrinsics
    # --------------------------------------------------
    run("python scripts//intrinsics.py")

    # --------------------------------------------------
    # 6. Prepare NeRF transforms.json
    # --------------------------------------------------
    run("python scripts/prepare_nerf.py")

    # 7. Train and render NeRF
    run("python scripts//train_render_nerf.py")

    print("\n✅ Pipeline finished successfully")
