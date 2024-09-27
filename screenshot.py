import cv2
import os
import numpy as np

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

# Example usage
video_path = "C:/Users/nicol/Downloads/Gen48/The Room/The Room _ Runway Gen_48 3rd Edition.mp4"
output_folder = "C:/Users/nicol/Downloads/Gen48/The Room/Screenshots"
capture_screenshots(video_path, output_folder)


