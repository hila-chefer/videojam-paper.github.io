import os
import mediapy as media
import numpy as np

# Set the directory path where the videos are stored
input_directory = "/Users/hilachefer/Downloads"  # change this to your folder path

# Traverse through the directory and subdirectories to find all .mp4 files
for root, dirs, files in os.walk(input_directory):
    for file in files:
        # Check if the file has a .mp4 extension
        if file.endswith(".mp4"):
            # Construct the full path to the video file
            input_path = os.path.join(root, file)

            # Read and resize the video
            resized_vid = media.read_video(input_path)
            resized_vid = np.stack([media.resize_image(image, (400, 400)) for image in resized_vid])

            # Construct the output path (same location, same filename)
            output_path = input_path  # Overwrite the original video

            # Write the compressed video
            media.write_video(output_path, resized_vid.astype(np.float32) / 255., fps=16, bps=1_000_000, codec='h264')

            print(f"Processed and overwritten: {input_path}")
