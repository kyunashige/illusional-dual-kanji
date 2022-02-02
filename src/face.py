import re

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


class Face:
    def __init__(self, img, keep_aspect_ratio, *, border=0, inv=False):
        assert img.mode == "1"
        self.img = img
        self.keep_aspect_ratio = keep_aspect_ratio
        self.border = border
        self.inv = inv

    def __remove_blank(self):
        if np.sum(self.img):
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

    @property
    def valid_color(self):
        return not self.inv

    def add_margin(self, top=0, right=0, bottom=0, left=0, color=0, all=None):
        if all == 0:
            return self
        if all is not None:
            top, right, bottom, left = [all] * 4

        width, height = self.img.size
        new_width = width + right + left
        new_height = height + top + bottom
        img = Image.new(self.img.mode, (new_width, new_height), color)
        img.paste(self.img, (left, top))
        self.img = img
        return self

    def resize(self, size):
        self.__remove_blank()
        self.keep_aspect_ratio and self.__expand_to_square()
        border = self.border if self.border else size // 16 if self.inv else 0
        self.img = self.img.resize((size - border * 2, size - border * 2))
        border_color = self.valid_color
        return self.add_margin(all=border, color=border_color)

    def to_binary_array(self):
        return np.asarray(self.img) == self.valid_color

    def render(self, ax):
        ax.imshow(self.to_binary_array(), cmap="gray_r", vmin=0, vmax=1)


def char_to_face(char, font_path, *, size=256, keep_aspect_ratio=False, char_inv=False):
    img = Image.new("1", (size * len(char), size))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size)
    draw.text((0, 0), char, fill=1, font=font)
    return Face(img, keep_aspect_ratio, inv=char_inv)


def image_to_face(image_path, *, mode="greater", th=1, keep_aspect_ratio=True, border=0):
    def parse_image_path(image_path):
        pattern = re.compile(r"(?P<key>ge|le|border)(?P<val>\d+)")
        image_path, *cmds = image_path.split("@")
        kwargs = {}
        for cmd in cmds:
            match = pattern.fullmatch(cmd)
            assert match, f"Unknown commnad: {cmd}"
            key, val = match.groups()
            if key in ["ge", "le"]:
                kwargs["mode"] = "greater" if key == "ge" else "less"
                kwargs["th"] = int(val)
            elif key == "border":
                kwargs["border"] = int(val)
        return image_path, kwargs

    if "@" in image_path:
        image_path, kwargs = parse_image_path(image_path)
        return image_to_face(image_path, **kwargs)

    img = Image.open(image_path).convert("L")

    if mode == "greater":
        img = img.point(lambda val: val >= th, mode="1")
    elif mode == "less":
        img = img.point(lambda val: val <= th, mode="1")
    else:
        raise Exception(f"Unknown binarize mode: {mode}")

    return Face(img, keep_aspect_ratio, border=border)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--resolution", "-r", type=int, default=32)
    parser.add_argument("--char", "-C", default="A")
    parser.add_argument("--font_path", "-f", default="/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc")
    parser.add_argument("--char_inv", "-i", action="store_true")
    # borrowed from https://minecraft.fandom.com/wiki/Sword
    parser.add_argument("--image_path", "-I", default="img/Diamond_Sword_JE3_BE3.png@ge1")
    parser.add_argument("--save_fig", "-s", default="", metavar="OUTPUT_PATH")
    args = parser.parse_args()

    ax1 = plt.subplot(1, 2, 1)
    char_to_face(args.char, args.font_path, char_inv=args.char_inv).resize(
        args.resolution
    ).render(ax1)

    ax2 = plt.subplot(1, 2, 2)
    image_to_face(args.image_path).resize(args.resolution).render(ax2)

    if args.save_fig:
        fig_name = args.save_fig
        plt.savefig(fig_name)
        print("Saved:", fig_name)
    else:
        plt.show()
