import trimesh

mesh = trimesh.load("scene.ply")
mesh.export("scene.obj")

print("Exported scene.obj")
