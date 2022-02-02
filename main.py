import argparse
import os

from src.face import char_to_face, image_to_face
from src.mesh import IllusionalMesh
from src.voxel import IllusionalVoxels


def exists_path(image_path):
    if os.path.exists(image_path):
        return image_path
    else:
        raise FileNotFoundError


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create a curious object whose appearance changes in the mirror.",
    )
    parser.add_argument("object_name_or_path")
    parser.add_argument("--resolution", "-r", type=int, default=64)
    parser.add_argument("--use_mirror", "-m", action="store_true")
    parser.add_argument("--image_paths", "-I", nargs="*", default=[])
    parser.add_argument("--chars", "-C", nargs="*", default=[])
    parser.add_argument(
        "--font_path", "-f", default="/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc", type=exists_path
    )
    parser.add_argument("--char_inv", "-i", action="store_true")
    parser.add_argument("--render", "-v", action="store_true")
    parser.add_argument("--color_coded", "-c", action="store_true")
    parser.add_argument("--save_fig", "-s", action="store_true")
    return parser


def is_name(name_or_parh):
    return not name_or_parh.endswith(".stl")


def get_path(name_or_parh):
    if is_name(name_or_parh):
        name_or_parh += ".stl"
    return name_or_parh


def get_faces(args):
    assert (
        1 <= len(args.image_paths) + len(args.chars) <= 3
    ), "Choose between 1 and 3 images or characters in total."

    faces = [image_to_face(image_path) for image_path in args.image_paths]
    faces += [
        char_to_face(
            char,
            args.font_path,
            char_inv=args.char_inv,
        )
        for char in args.chars
    ]
    return faces


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    parser = get_parser()
    args = parser.parse_args()

    if is_name(args.object_name_or_path):
        faces = get_faces(args)
        iv = IllusionalVoxels(
            size=args.resolution,
            use_mirror=args.use_mirror,
            name=args.object_name_or_path,
        ).build(*faces, color_coded=args.color_coded)
        im = IllusionalMesh(iv)
        im.save()
        if args.render:
            iv.visualize()
            if args.save_fig:
                fig_name = im.name + ".png"
                plt.savefig(fig_name)
                print("Saved:", fig_name)
            else:
                plt.show()
    else:
        path = get_path(args.object_name_or_path)
        im = IllusionalMesh(path).visualize()
        plt.show()
