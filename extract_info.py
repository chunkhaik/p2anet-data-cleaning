import cv2
import os
import json

def extract_video_info(video_path):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"The video file {video_path} does not exist.")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open the video file.")

    video_info = {}
    video_info['Video Name'] = os.path.basename(video_path)
    video_info['Width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_info['Height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_info['Frame Count'] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_info['Frame Rate (FPS)'] = cap.get(cv2.CAP_PROP_FPS)
    video_info['Duration (s)'] = video_info['Frame Count'] / video_info['Frame Rate (FPS)'] if video_info['Frame Rate (FPS)'] > 0 else None

    cap.release()

    return video_info

# Paths
VIDEO_FOLDER_PATH = "/home/kokchunkhai/dataset/video/v2"
LOG_FILE_PATH = os.path.join("data", "v2_info.json")

video_data = []

for i in range(1208):
    video_file = f"{i:07d}.mp4"  # 7-digit zero-padded video names
    video_path = os.path.join(VIDEO_FOLDER_PATH, video_file)

    if os.path.isfile(video_path):
        try:
            info = extract_video_info(video_path)
            video_data.append(info)
        except Exception as e:
            video_data.append({"Video Name": video_file, "Error": str(e)})
    else:
        video_data.append({"Video Name": video_file, "Error": "File not found"})

    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1} videos")

with open(LOG_FILE_PATH, "w") as json_file:
    json.dump(video_data, json_file, indent=4)

print("Video information extraction completed and saved to JSON.")
