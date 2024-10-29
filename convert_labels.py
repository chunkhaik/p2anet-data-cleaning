import json
import os

target='v1'
input_file = f"data/{target}_reformatted.json"
output_file = f"data/{target}_final.json"

def decode_garbled_text(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for video in data:
    for event in video.get("events", []):
        decoded_parts = [decode_garbled_text(part) for part in event["label"].split('_')]
        event["label"] = "_".join(decoded_parts)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Decoded labels and saved to {output_file}")
