import json
import os


def decode_labels(input_file, output_file):
    def decode_garbled_text(text):
        try:
            return text.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text
        
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for video in data:
        for action in video.get("actions", []):
            decoded_labels = [decode_garbled_text(label) for label in action.get("label_names", [])]
            action["label_names"] = decoded_labels

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Decoded labels and saved to {output_file}")

target = 'v1'
input_file = f"data/{target}_original.json"
output_file = f"data/{target}_decoded.json"
decode_labels(input_file, output_file)