import json
import os

VIDEO_JSON_PATH = "data/v2.json"
VIDEO_INFO_JSON_PATH = "data/v2_info.json"
OUTPUT_JSON_PATH = "data/v2_reformatted.json"

SKIP_VIDEOS = ["0000110.mp4", "0000112.mp4"]

with open(VIDEO_JSON_PATH, "r") as f:
    video_data = json.load(f)

with open(VIDEO_INFO_JSON_PATH, "r") as f:
    video_info_data = json.load(f)

combined_data = []

video_info_map = {info["Video Name"]: info for info in video_info_data}

for video in video_data:
    video_name = video["url"]
    
    if video_name in SKIP_VIDEOS:
        print(f"Skipping video {video_name}")
        continue
    
    video_info = video_info_map.get(video_name)

    if not video_info:
        print(f"Warning: Video info for {video_name} not found.")
        continue

    combined_video = {
        "fps": video_info["Frame Rate (FPS)"],
        "height": video_info["Height"],
        "width": video_info["Width"],
        "num_frames": video_info["Frame Count"],
        "video": video_name,
        "events": []
    }

    for action in video["actions"]:
        start_frame = round(action["start_id"] * video_info["Frame Rate (FPS)"])
        end_frame = round(action["end_id"] * video_info["Frame Rate (FPS)"])
        
        label = "_".join(action["label_names"])  
        outcome = "in"  # TODO fix temporary hard coded outcome

        event = {
            "frame": start_frame,
            "label": label,
            "outcome": outcome
        }
        combined_video["events"].append(event)

    combined_data.append(combined_video)

with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(combined_data, f, indent=4)

print("Combined JSON data saved successfully.")
