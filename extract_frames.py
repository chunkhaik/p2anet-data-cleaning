import cv2, os, time

def extract_frames(video_path, output_dir, target_height, verbose=False):
    
    if not os.path.isfile(video_path):
        print(f"Error: Video file {video_path} not found.")
        return
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    combined_output_dir = os.path.join(output_dir, video_name)
    os.makedirs(combined_output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    aspect_ratio = original_width / original_height
    target_width = int(target_height * aspect_ratio)
    
    if verbose:
        print(f"Resizing frames to {target_width}x{target_height} pixels (aspect ratio preserved).")
        print(f"Total frames to process: {frame_count}")

    frame_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        resized_frame = cv2.resize(frame, (target_width, target_height))
        frame_filename = os.path.join(combined_output_dir, f"{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, resized_frame)
        
        frame_number += 1

    cap.release()
    print(f"All frames extracted and resized to {target_height}px height in directory: {combined_output_dir}") if verbose else None

def process_videos(base_input_dir, base_output_dir, target_height, video_count, set_name, full_verbose=False):
    input_dir = os.path.join(base_input_dir, set_name)
    output_dir = os.path.join(base_output_dir, set_name)
    
    for i in range(video_count):
                
        video_filename = f"{i:07d}.mp4"
        video_path = os.path.join(input_dir, video_filename)
        
        start_time = time.time()
        extract_frames(video_path, output_dir, target_height)
        time_taken = time.time() - start_time

        if full_verbose:
            print(f"{set_name.upper()}: processed {video_filename} in {time_taken:.2f} seconds")
        else:
            if i % 100 == 0:
                print(f"{set_name.upper()}: processed {video_filename} in {time_taken:.2f} seconds")

BASE_INPUT_DIR = os.path.expanduser("~/dataset/video")
BASE_OUTPUT_DIR = os.path.expanduser("~/dataset/frames")
TARGET_HEIGHT = 224

# V1 (from 0000000 to 0001280)
process_videos(BASE_INPUT_DIR, BASE_OUTPUT_DIR, TARGET_HEIGHT, 1281, "v1", True)

# V2 (from 0000000 to 0001207)
process_videos(BASE_INPUT_DIR, BASE_OUTPUT_DIR, TARGET_HEIGHT, 1208, "v2", True)