#!/bin/bash
set -eu

function task_src() {
    echo "Task: src"
    python src/face.py -s assets/face.png
    python src/voxel.py MC -s assets/voxel-MC.png
    python src/voxel.py NLP --color_coded -s assets/voxel-NLP.png
    python src/mesh.py MC --color_coded -s assets/mesh-MC.png
    python src/mesh.py NLP --color_coded -s assets/mesh-NLP.png
}

function task_wo_color() {
    echo "Task: w/o --color_coded"
    python main.py assets/main-celebration-star \
        --resolution 64 \
        --chars 祝 ★ \
        --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc' \
        --render \
        --save_fig
    python main.py assets/main-NLP \
        --resolution 64 \
        --chars Ｎ Ｌ Ｐ \
        --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc' \
        --render \
        --save_fig
    python main.py assets/main-pickaxe-sword \
        --resolution 64 \
        --use_mirror \
        --image_paths img/Diamond_Pickaxe_JE3_BE3.png@ge1 img/Diamond_Sword_JE3_BE3.png@ge1 \
        --render \
        --save_fig
}

function task_w_color() {
    echo "Task: w/ --color_coded"
    python main.py assets/main-celebration-star-color \
        --resolution 64 \
        --chars 祝 ★ \
        --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc' \
        --render --color_coded \
        --save_fig
    python main.py assets/main-NLP-color \
        --resolution 64 \
        --chars Ｎ Ｌ Ｐ \
        --font_path '/System/Library/Fonts/ヒラギノ角ゴシック W9.ttc' \
        --render --color_coded \
        --save_fig
    python main.py assets/main-pickaxe-sword-color \
        --resolution 64 \
        --use_mirror \
        --image_paths img/Diamond_Pickaxe_JE3_BE3.png@ge1 img/Diamond_Sword_JE3_BE3.png@ge1 \
        --render --color_coded \
        --save_fig
}

task_src
task_wo_color
task_w_color
