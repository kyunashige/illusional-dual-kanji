import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Face:
    def __init__(self, img, keep_aspect_ratio):
        self.img = img
        self.keep_aspect_ratio = keep_aspect_ratio

    def __remove_blank(self):
        left, *_, right = np.nonzero(np.sum(self.img, axis=0))[0]
        upper, *_, lower = np.nonzero(np.sum(self.img, axis=1))[0]
        self.img = self.img.crop((left, upper, right, lower))

    def __expand_to_square(self):
        width, height = self.img.size
        if width == height:
            return
        elif width > height:
            img = Image.new(self.img.mode, (width, width), 0)
            img.paste(self.img, (0, (width - height) // 2))
            self.img = img
        else:
            img = Image.new(self.img.mode, (height, height), 0)
            img.paste(self.img, ((height - width) // 2, 0))
            self.img = img

    def resize(self, size):
        self.__remove_blank()
        if self.keep_aspect_ratio:
            self.__expand_to_square()
        self.img = self.img.resize((size, size))
        return self

    def to_binary_array(self):
        return np.asarray(self.img) > 0

    def render(self, ax, *, size=64):
        ax.imshow(self.to_binary_array(), cmap="gray_r", vmin=0, vmax=1)


def char_to_face(char, font_path, *, size=256, keep_aspect_ratio=False):
    img = Image.new("L", (size * len(char), size))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)
    draw.text((0, 0), char, fill=1, font=font)
    return Face(img, keep_aspect_ratio)


def image_to_face(image_path, *, mode="less", th=254, keep_aspect_ratio=True):
    if "@" in image_path:
        image_path, mode = image_path.split("@")
        assert mode.startswith("ge") or mode.startswith("le")
        th = int(mode[2:])
        mode = "greater" if mode.startswith("ge") else "less"
    img = Image.open(image_path).convert("L")
    if mode == "greater":
        img = img.point(lambda val: val >= th)
    elif mode == "less":
        img = img.point(lambda val: val <= th)
    else:
        raise Exception(f"Unknown binarize mode: {mode}")
    return Face(img, keep_aspect_ratio)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--resolution", "-r", type=int, default=23)
    parser.add_argument("--char", "-C", default="祝")
    parser.add_argument("--font_path", "-f", default="/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc")
    parser.add_argument("--image_path", "-I", default="img/Diamond_Pickaxe_JE3_BE3.png@ge1")
    parser.add_argument("--save_fig", "-s", default="")
    args = parser.parse_args()

    ax1 = plt.subplot(1, 2, 1)
    char_to_face(args.char, args.font_path).resize(args.resolution).render(ax1)

    # from: https://minecraft.fandom.com/wiki/Pickaxe
    ax2 = plt.subplot(1, 2, 2)
    image_to_face(args.image_path).resize(args.resolution).render(ax2)

    if args.save_fig:
        fig_name = args.save_fig
        plt.savefig(fig_name)
        print("Saved:", fig_name)
    else:
        plt.show()
