import matplotlib.pyplot as plt
import numpy as np
import stl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

if __name__ == "__main__":
    from voxel import IllusionalVoxels
else:
    from .voxel import IllusionalVoxels


def build_cube(translation, direction):
    data = np.zeros(2, dtype=stl.mesh.Mesh.dtype)

    assert direction in [view["name"] for view in IllusionalVoxels.views]
    if direction == "Left":
        data["vectors"][0] = np.array([[0, 0, 0], [1, 0, 0], [1, 0, 1]])
        data["vectors"][1] = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 1]])
    if direction == "Top":
        data["vectors"][0] = np.array([[0, 1, 1], [1, 0, 1], [0, 0, 1]])
        data["vectors"][1] = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 1]])
    if direction == "Right":
        data["vectors"][0] = np.array([[1, 0, 0], [1, 0, 1], [1, 1, 0]])
        data["vectors"][1] = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 0]])

    center = 1 / 2
    data["vectors"] -= center

    cube_front = stl.mesh.Mesh(data.copy())
    cube_back = stl.mesh.Mesh(data.copy())

    if direction == "Left":
        cube_back.rotate([center, 0.0, 0.0], np.radians(180))
    if direction == "Top":
        cube_back.rotate([0.0, center, 0.0], np.radians(180))
    if direction == "Right":
        cube_back.rotate([0.0, 0.0, center], np.radians(180))

    cube = stl.mesh.Mesh(np.concatenate([cube_front.data.copy(), cube_back.data.copy()]))
    cube.translate(np.array(translation) + center)
    return cube


class IllusionalMesh(IllusionalVoxels):
    def __init__(self, iv_or_path):
        if type(iv_or_path) == str and iv_or_path.endswith(".stl"):
            print(f"Loading: {iv_or_path}")
            self.mesh = stl.mesh.Mesh.from_file(iv_or_path)
            print(f"Loaded: {iv_or_path}")
            self.path = iv_or_path
        elif type(iv_or_path) == IllusionalVoxels:
            for key in dir(iv_or_path):
                if key.endswith("__") or key in dir(self):
                    continue
                setattr(self, key, getattr(iv_or_path, key))
            self.mesh = self.__build_mesh_by_direction()
            self.path = None
        else:
            raise TypeError

    def __build_mesh_by_direction(self):
        self.mesh_by_direction = {}
        for view in self.views:
            self.mesh_by_direction[view["name"]] = stl.mesh.Mesh(
                np.concatenate(
                    [
                        build_cube(coordinate, view["name"]).data.copy()
                        for coordinate in zip(*np.where(self.voxels == 1))
                    ]
                )
            )
        return stl.mesh.Mesh(
            np.concatenate([mesh.data.copy() for mesh in self.mesh_by_direction.values()])
        )

    def save(self):
        self.mesh.save(f"{self.name}.stl")
        print(f"Saved: {self.name}.stl")

    def __visualize(self, ax):
        if self.path:
            self.render(ax, self.mesh)
        else:
            facecolor = [0, 0, 0, 0.8]
            for i, view in enumerate(self.views):
                facecolor[i] = 1
                ax.add_collection3d(
                    Poly3DCollection(
                        self.mesh_by_direction[view["name"]].vectors, facecolor=facecolor
                    )
                )
                facecolor[i] = 0
        scale = self.mesh.points.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    def __getitem__(self, i):
        if self.path:
            return True, self.views[i]
        else:
            if i == 0:
                return self.has_cube1, self.views[0]
            elif i == 1:
                return self.has_cube2, self.views[1]
            elif i == 2:
                return self.has_cube3, self.views[2]
            else:
                raise IndexError

    def visualize(self):
        plt.figure(figsize=(6, 9))

        ax = plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=3, projection="3d")
        if self.path:
            ax.set_title(self.path)
        else:
            ax.set_title(f"use_mirror: {self.use_mirror}")
        self.__visualize(ax)

        for i, (exists, d) in enumerate(self):
            if not exists:
                continue
            ax = plt.subplot2grid((3, 3), (2, i), projection="3d")
            self._get_modified_axes(ax, d)
            self.__visualize(ax)

    @classmethod
    def render(cls, ax, mesh):
        ax.add_collection3d(Poly3DCollection(mesh.vectors))
        scale = mesh.points.flatten()
        ax.auto_scale_xyz(scale, scale, scale)


if __name__ == "__main__":
    from voxel import choose_sample_iv

    im = IllusionalMesh(choose_sample_iv())
    if im.color_coded:
        im.visualize()
        plt.show()
    else:
        im.save()
