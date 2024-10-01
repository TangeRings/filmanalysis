import cv2
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()
video_path = os.getenv("VIDEO_PATH")
output_folder=os.getenv("OUTPUT_FOLDER")


# set the interval to capture screenshots (interval is seconds), in this example, it is 0.5 seconds

def capture_screenshots(video_path, output_folder, interval=0.5):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)

    frame_count = 0
    screenshot_count = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Save the frame as an image
            screenshot_path = os.path.join(output_folder, f"screenshot_{screenshot_count:04d}.png")
            cv2.imwrite(screenshot_path, frame)
            screenshot_count += 1

        frame_count += 1

    # Release the video capture object
    video.release()

    print(f"Captured {screenshot_count} screenshots.")



capture_screenshots(video_path, output_folder)


