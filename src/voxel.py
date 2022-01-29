import matplotlib.pyplot as plt
import numpy as np


class IllusionalVoxels:
    views = [
        {"elev": 0, "azim": -90, "name": "Left"},
        {"elev": 90, "azim": -90, "name": "Top"},
        {"elev": 0, "azim": 0, "name": "Right"},
    ]

    def __init__(self, size, use_mirror=True, name=None):
        self.size = size
        self.spatial_axes = [self.size] * 3
        self.use_mirror = use_mirror
        self.name = name

    def __build_cube(self, face=None, mode="y-z"):
        if face is None:
            return np.ones(self.spatial_axes, dtype=np.bool_)

        face = face.resize(self.size).to_binary_array()
        prism = np.zeros(self.spatial_axes, dtype=np.bool_)
        if mode == "y-z":
            cube = prism + face[::-1].T
        if mode == "x-z":
            cube = prism + face[::-1].T
            cube = cube.swapaxes(0, 1)
        if mode == "x-y":
            cube = prism + face[::-1]
            cube = cube.swapaxes(0, 2)
        if mode == "x-y-mirror":
            cube = prism + face
            cube = cube.swapaxes(0, 2)
        return cube

    def build(self, face1=None, face2=None, face3=None, color_coded=True):
        self.cube1 = self.__build_cube(face1, "x-z")
        self.has_cube1 = face1 is not None
        self.cube2 = self.__build_cube(face2, "x-y-mirror" if self.use_mirror else "x-y")
        self.has_cube2 = face2 is not None
        self.cube3 = self.__build_cube(face3, "y-z")
        self.has_cube3 = face3 is not None
        self.voxels = self.cube1 & self.cube2 & self.cube3
        self.colors = np.zeros(self.spatial_axes + [4], dtype=np.float32)
        self.color_coded = color_coded

        if self.color_coded:
            # self.cube1, self.cube2, self.cube3 => red, green, blue
            self.union = np.array(self.voxels)
            for i, (exists, cube, _) in enumerate(self):
                if not exists:
                    continue
                self.colors[cube, i] = 1
                self.union |= cube
            self.colors[self.union, -1] = 0.15
            self.colors[self.voxels, -1] = 1
        else:
            self.colors[self.voxels] = [0.2, 0.5, 0.1, 1]

        return self

    def __getitem__(self, i):
        if i == 0:
            return self.has_cube1, self.cube1, self.views[0]
        elif i == 1:
            return self.has_cube2, self.cube2, self.views[1]
        elif i == 2:
            return self.has_cube3, self.cube3, self.views[2]
        else:
            raise IndexError

    @classmethod
    def _get_modified_axes(self, ax, d=None):
        ax.set_box_aspect((1, 1, 1))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        if d:
            ax.view_init(d["elev"], d["azim"])
            ax.set_title(d["name"])
        return ax

    def visualize(self):
        plt.figure(figsize=(6, 9))

        ax = plt.subplot2grid((4, 3), (0, 0), rowspan=2, colspan=3, projection="3d")
        if self.color_coded:
            ax.voxels(self.union, facecolors=self.colors)
        ax.voxels(self.voxels, facecolors=self.colors)
        ax.set_box_aspect((1, 1, 1))
        ax.set_title(f"use_mirror: {self.use_mirror}")

        for i, (exists, cube, d) in enumerate(self):
            if not exists:
                continue
            ax_before = plt.subplot2grid((4, 3), (2, i), projection="3d")
            self._get_modified_axes(ax_before)
            ax_before.voxels(cube)
            ax_after = plt.subplot2grid((4, 3), (3, i), projection="3d")
            self._get_modified_axes(ax_after, d)
            if self.color_coded:
                ax_after.voxels(self.union, facecolors=self.colors)
            ax_after.voxels(self.voxels, facecolors=self.colors)


def choose_sample_iv():
    import argparse

    from face import char_to_face, image_to_face

    parser = argparse.ArgumentParser()
    parser.add_argument("sample_name", type=str, choices=["MC", "NLP"])
    parser.add_argument("--resolution", "-r", type=int, default=23)
    parser.add_argument("--font_path", default="/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc")
    parser.add_argument("--color_coded", "-c", action="store_true")
    args = parser.parse_args()

    if args.sample_name == "MC":
        iv = IllusionalVoxels(size=args.resolution, use_mirror=True, name="MC").build(
            # borrowed from https://minecraft.fandom.com/wiki/Pickaxe
            face1=image_to_face("img/Diamond_Pickaxe_JE3_BE3.png", mode="greater", th=1),
            # borrowed from https://minecraft.fandom.com/wiki/Sword
            face2=image_to_face("img/Diamond_Sword_JE3_BE3.png", mode="greater", th=1),
            color_coded=args.color_coded,
        )
    else:
        iv = IllusionalVoxels(size=args.resolution, use_mirror=False, name="NLP").build(
            face1=char_to_face("N", args.font_path, keep_aspect_ratio=False),
            face2=char_to_face("L", args.font_path, keep_aspect_ratio=False),
            face3=char_to_face("P", args.font_path, keep_aspect_ratio=False),
            color_coded=args.color_coded,
        )

    return iv


if __name__ == "__main__":

    choose_sample_iv().visualize()
    plt.show()
