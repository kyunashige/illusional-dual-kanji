from fnmatch import translate

import matplotlib.pyplot as plt
import numpy as np
import stl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

if __name__ == "__main__":
    from voxel import IllusionalVoxels
else:
    from .voxel import IllusionalVoxels


def build_cube(translation, orientation):
    data = np.zeros(4, dtype=stl.mesh.Mesh.dtype)
    base = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 1]])

    shift = IllusionalVoxels.views[orientation]["shift"]
    vertexes = np.roll(base, shift, axis=1)
    data["vectors"][0] = vertexes[:3]
    data["vectors"][1] = vertexes[2:]

    unit = np.zeros(3)
    unit[(shift + 1) % 3] = 1
    for i in range(2):
        data["vectors"][i + 2] = data["vectors"][i] + unit
        data["attr"][i + 2] = 1

    data["vectors"] += np.array(translation)

    return data


def cancel_triangles(data):
    polygons = data["vectors"].sum(axis=1)
    idx = np.lexsort(polygons.T)
    diff = np.all(polygons[idx[:-1]] == polygons[idx[1:]], axis=1)
    diff = np.concatenate(([False], diff, [False]))
    dup = diff[:-1] | diff[1:]
    return data[idx[~dup]]


class IllusionalMesh(IllusionalVoxels):
    def __init__(self, iv_or_path):
        if type(iv_or_path) == str and iv_or_path.endswith(".stl"):
            self.mesh = stl.mesh.Mesh.from_file(iv_or_path)
            print(f"Loaded (Mesh): {iv_or_path}")
            self.path = iv_or_path
        elif type(iv_or_path) == IllusionalVoxels:
            for key in dir(iv_or_path):
                if key in dir(self):
                    continue
                setattr(self, key, getattr(iv_or_path, key))
            self.mesh = self.__build_mesh_by_orientation()
            print(f"Created (Mesh): {self.name}")
            self.path = None
        else:
            raise TypeError

    def __build_mesh_by_orientation(self):
        self.triangles_by_orientation = {}
        for orientation in self.views:
            triangles = np.concatenate(
                [
                    build_cube(coordinate, orientation)
                    for coordinate in zip(*np.where(self.voxels == 1))
                ]
            )
            triangles = cancel_triangles(triangles)
            for triangle in triangles:
                if triangle["attr"]:
                    arr = triangle["vectors"]
                    arr[1, :], arr[2, :] = arr[2, :], arr[1, :].copy()
            self.triangles_by_orientation[orientation] = triangles
        mesh = stl.mesh.Mesh(
            np.concatenate([triangles for triangles in self.triangles_by_orientation.values()])
        )
        assert mesh.is_closed()
        return mesh

    def save(self):
        print(f"Saving: {self.name}.stl")
        self.mesh.save(f"{self.name}.stl")
        print(f"Saved: {self.name}.stl")

    def __visualize(self, ax):
        if self.path:
            self.render(ax)
        else:
            # color-coded
            facecolor = [0, 0, 0, 0.7]
            for i, orientation in enumerate(self.views):
                facecolor[i] = 1
                ax.add_collection3d(
                    Poly3DCollection(
                        self.triangles_by_orientation[orientation]["vectors"],
                        facecolor=facecolor,
                        edgecolor=[0.01] * 3 + [0.1],
                    )
                )
                facecolor[i] = 0
        scale = self.mesh.points.flatten()
        ax.auto_scale_xyz(scale, scale, scale)

    def visualize(self):
        print("Rendering (Mesh):", self.path or self.name)
        plt.figure(figsize=(6, 9))

        ax = plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=3, projection="3d")
        if self.path:
            ax.set_title(self.path)
        else:
            ax.set_title(f"use_mirror: {self.use_mirror}")
        self.__visualize(ax)

        for i, orientation in enumerate(self.views):
            ax = plt.subplot2grid((3, 3), (2, i), projection="3d")
            self._get_modified_axes(ax, orientation)
            self.__visualize(ax)

    def render(self, ax):
        ax.add_collection3d(Poly3DCollection(self.mesh.vectors))
        scale = self.mesh.points.flatten()
        ax.auto_scale_xyz(scale, scale, scale)


if __name__ == "__main__":
    from voxel import choose_sample_iv

    iv, save_fig = choose_sample_iv()
    im = IllusionalMesh(iv)
    if im.color_coded or save_fig:
        im.visualize()
        if save_fig:
            fig_name = save_fig
            print("Saving:", fig_name)
            plt.savefig(fig_name)
            print("Saved:", fig_name)
        else:
            plt.show()
    else:
        im.save()
