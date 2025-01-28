import os
import re
from glob import glob
from os.path import basename, dirname, join
from pathlib import Path
import subprocess

import fire

def concat_videoJAM(folder1="DiT30B_labeled", folder2="our_results_labeled", output_folder="concat_labeled"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    # Get lists of files in both folders
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # Find common files between the two folders
    common_files = files1.intersection(files2)
    for file_name in common_files:
        if not "A_dog_jumping_over_a_wooden_hurdle._Slow_motion." in file_name:
            print("continuing on ", file_name)
            continue
        input1 = os.path.join(folder1, file_name)
        input2 = os.path.join(folder2, file_name)
        output_file = os.path.join(output_folder, file_name)

        # ffmpeg command
        command = [
            "ffmpeg",
            "-i", input1,
            "-i", input2,
            "-filter_complex", "[0:v:0][1:v:0]hstack=inputs=2:shortest=1[v]",
            "-map", "[v]",
            "-map", "0:a?",
            "-map", "1:a?",
            "-c:v", "libx264",
            "-crf", "17",
            "-preset", "slow",
            output_file,
            "-y"
        ]

        print(f"Processing: {file_name}")
        try:
            subprocess.run(command, check=True)
            print(f"Finished: {file_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {file_name}: {e}")

def add_names(folder_path, output_path):
    folder_path = Path(folder_path)
    os.makedirs(output_path, exist_ok=True)

    for mp4_path in glob(join(folder_path, "*.mp4")):
        mp4_output_path = join(
            output_path, f"{basename(mp4_path).replace(' ', '_')}"
        )
        # model_name = "DiT-30B"
        model_name = "VideoJAM"
        cmd = f"""
            ffmpeg -i "{mp4_path}" -vf "drawtext=text='"{model_name}"':fontfile='font.ttf':fontcolor=white:fontsize=25:x=(w-text_w)/8-40:y=h-line_h-10:box=1:boxcolor=black@0.65:text_align=center" -c:v libx264 -crf 1 -preset slow {mp4_output_path} -y
            """
        os.system(cmd)


if __name__ == "__main__":
    fire.Fire(concat_videoJAM)
