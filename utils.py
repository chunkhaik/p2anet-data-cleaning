import json

def decode_labels(input_file, output_file):
    """
    Decodes Chinese Unicode characters in 'label_names' fields from input_file and saves the cleaned data to output_file.

    Args:
    - input_file (str): Path to the JSON file with encoded Chinese characters.
    - output_file (str): Path to save the decoded JSON data.
    """
    
    print(f'[1/2] decoding labels from {input_file}')
    
    def decode_text(text):
        try:
            return text.encode('latin1').decode('utf-8')
        except UnicodeError:
            return text

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for video in data:
        for action in video.get("actions", []):
            action["label_names"] = [decode_text(label) for label in action.get("label_names", [])]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f'[1/2] decode complete, saving file to {output_file}')
    
def reformat_data(video_info_path, video_json_path, output_json_path, skip_videos=None):
    """
    Reformats video data by combining metadata from video_info_path with action data from video_json_path.

    Args:
    - video_info_path (str): Path to the JSON file containing video information metadata.
    - video_json_path (str): Path to the JSON file containing video action data.
    - output_json_path (str): Path where the reformatted JSON data will be saved.
    - skip_videos (list): Optional list of video filenames to skip during processing.

    Returns:
    - None
    """
    print(f'[2/2] reformatting data from {video_info_path} and {video_json_path}')
    
    if skip_videos is None:
        skip_videos = []

    with open(video_json_path, "r", encoding='utf-8') as f:
        video_data = json.load(f)

    with open(video_info_path, "r", encoding='utf-8') as f:
        video_info_data = json.load(f)

    video_info_map = {info["Video Name"]: info for info in video_info_data}
    combined_data = []

    for video in video_data:
        video_name = video["url"]

        if video_name in skip_videos:
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
            outcome = "in"  # TODO: fix hard-coded outcome if needed

            event = {
                "frame": start_frame,
                "label": label,
                "outcome": outcome
            }
            combined_video["events"].append(event)

        combined_data.append(combined_video)

    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print(f'[2/2] data reformatting complete, saved to {output_json_path}')

def process_dataset_version(dataset_version, videos_to_skip):
    """
    Processes a single dataset version by decoding labels and reformatting data.

    Args:
    - dataset_version (str): The version of the dataset (e.g., 'v1', 'v2').
    - videos_to_skip (list): List of video filenames to skip for this dataset version.
    """
    original_json_path = f"data/{dataset_version}_0_original.json"
    decoded_json_path = f"data/{dataset_version}_1_decoded.json"
    video_info_path = f"data/{dataset_version}_0_info.json"
    reformatted_output_path = f"data/{dataset_version}_2_reformatted.json"

    decode_labels(original_json_path, decoded_json_path)

    reformat_data(video_info_path, decoded_json_path, reformatted_output_path, videos_to_skip)

def main():
    dataset_configs = {
        'v1': [],
        'v2': ["0000110.mp4", "0000112.mp4"]
    }

    for version, skip_videos in dataset_configs.items():
        process_dataset_version(version, skip_videos)
        print("")

if __name__ == "__main__":
    main()