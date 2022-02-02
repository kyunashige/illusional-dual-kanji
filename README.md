# illusional-dual-kanji

![name](https://img.shields.io/badge/研究プロジェクト演習-blue.svg)

A program to create a mysterious object that changes its appearance in a mirror.

## Requirements

```shell
pip install -r requirements.txt
```

## Usage

```
usage: main.py [-h] [--resolution RESOLUTION] [--use_mirror]
               [--image_paths [IMAGE_PATHS ...]]
               [--chars [CHARS ...]] [--font_path FONT_PATH] [--char_inv]
               [--render] [--color_coded] [--save_fig]
               object_name_or_path
```

-   To set common parameters
    -   `object_name_or_path`
        -   Requires the name of the object to be used as the name of the output files.
        -   If `object_name_or_path` ends with the extension `.stl`, this program will load the STL file instead of creating a new object.
    -   `--resolution RESOLUTION`
    -   `--use_mirror`
        -   Reverses the top face.
-   To choose between 1 and 3 images or characters in total
    -   Image
        -   `--image_paths [IMAGE_PATHS ...]`
            -   You can specify multiple paths separated by spaces.
            -   Each path can be suffixed with the instruction to be binarized:
                -   e.g. `@ge30`
                    -   After converting the image to grayscale, keep only those pixels that are greater than 30.
                -   e.g. `@le128`
                    -   After converting the image to grayscale, keep only those pixels that are less than 128.
                -   e.g. `@border4`
                    -   Add a border of width 4.
    -   Character
        -   `--chars [CHARS ...]`
            -   You can specify multiple characters separated by spaces.
        -   `--font_path FONT_PATH`
        -   `--char_inv`
            -   Inverts whether the pixel is kept or not.
-   To visialize (after saving the STL file)
    -   `--render`
        -   Renders the generated object.
    -   `--color_coded`
        -   Separates the parts by color (if the stl file is not loaded).
    -   `--save_fig`

## Gallery

### Two characters: 祝 and ★

```shell
python main.py celebration-star \
    --resolution 64 \
    --chars 祝 ★ \
    --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc' \
    --render \
    --save_fig
```

| w/o `--color_coded`                                      | w/ `--color_coded`                                             |
| -------------------------------------------------------- | -------------------------------------------------------------- |
| <img src="assets/main-celebration-star.png" width="300"> | <img src="assets/main-celebration-star-color.png" width="300"> |

### Three characters: N, L and P

```shell
python main.py NLP \
    --resolution 64 \
    --chars Ｎ Ｌ Ｐ \
    --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc' \
    --render \
    --save_fig
```

| w/o `--color_coded`                         | w/ `--color_coded`                                |
| ------------------------------------------- | ------------------------------------------------- |
| <img src="assets/main-NLP.png" width="300"> | <img src="assets/main-NLP-color.png" width="300"> |

### Two images: Pickaxe and Sword

These images are borrowed from https://minecraft.fandom.com/wiki.

```shell
python main.py pickaxe-sword \
    --resolution 64 \
    --use_mirror \
    --image_paths img/Diamond_Pickaxe_JE3_BE3.png@ge1 img/Diamond_Sword_JE3_BE3.png@ge1 \
    --render \
    --save_fig
```

| w/o `--color_coded`                                   | w/ `--color_coded`                                          |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| <img src="assets/main-pickaxe-sword.png" width="300"> | <img src="assets/main-pickaxe-sword-color.png" width="300"> |
