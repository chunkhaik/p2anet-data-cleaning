import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv

plt.rcParams['font.family'] = 'Noto Sans CJK JP'


"""
UTILITY FUNCTIONS
"""
def load_data(json_paths):
    combined_data = []
    for path in json_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            combined_data.extend(data)
    return combined_data

def save_plot(fig, output_path):
    fig.tight_layout()
    fig.savefig(output_path, format="jpg", dpi=300)
    print(f"Plot saved as {output_path}")
    plt.close(fig)

def plot_heatmap(data, title, output_path, cmap="Blues"):
    plt.figure(figsize=(12, 6))
    sns.heatmap(data, annot=True, fmt="d", cmap=cmap)
    plt.title(title)
    plt.savefig(output_path, format="jpg", dpi=300)
    print(f"{title} plot saved as {output_path}")
    plt.close()

"""
ANALYSIS FUNCTIONS
"""
def save_split_labels_csv(data, output_dir):
    split_labels = []
    for video_idx, video in enumerate(data):
        for event_idx, event in enumerate(video["events"]):
            split_labels.append({
                "video_id": video_idx,
                "event_id": event_idx,
                "label_parts": event["label"].split('_')
            })

    output_path = os.path.join(output_dir, "split_labels.csv")
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["video_id", "event_id", "label_parts"])
        writer.writeheader()
        writer.writerows(split_labels)
    print(f"Split labels saved as CSV at {output_path}")

def plot_action_distribution(df, output_dir):
    counts = {
        "Type": df["Type"].value_counts(),
        "Negation": df["Negation"].value_counts(),
        "Action": df["Action"].value_counts()
    }
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, (label, count) in zip(axes, counts.items()):
        count.plot(kind='bar', ax=ax, title=f"{label} Distribution")
    save_plot(fig, os.path.join(output_dir, "data_distribution.jpg"))

def plot_type_action_correlation(df, output_dir):
    type_action_correlation = pd.crosstab(df["Type"], df["Action"])
    plot_heatmap(type_action_correlation, "Type vs. Action Correlation", os.path.join(output_dir, "type_action_correlation.jpg"))

def plot_negation_action_correlation(df, output_dir):
    negation_action_correlation = pd.crosstab(df["Negation"], df["Action"])
    plot_heatmap(negation_action_correlation, "Negation vs. Action Correlation", os.path.join(output_dir, "negation_action_correlation.jpg"), cmap="Greens")

def plot_labels_per_event(data, output_dir):
    label_counts = [len(event["label"].split('_')) for video in data for event in video["events"]]
    label_counts_series = pd.Series(label_counts)

    fig, ax = plt.subplots(figsize=(10, 6))
    label_counts_series.plot(kind='hist', bins=20, title="Distribution of Label Parts per Event")
    ax.set_xlabel("Number of Parts in Label (e.g., 'label1_label2_label3' counted as 3)")
    ax.set_ylabel("Frequency")
    save_plot(fig, os.path.join(output_dir, "labels_per_event_distribution.jpg"))

def count_action_occurrences(df, output_dir):
    action_counts = df["Action"].value_counts()
    output_path = os.path.join(output_dir, "action_occurrences.csv")
    action_counts.to_csv(output_path)
    print(f"Action occurrences saved as {output_path}")

def main():
    output_dir = "analysis"
    os.makedirs(output_dir, exist_ok=True)

    data = load_data(["data/v1_2_reformatted.json", "data/v2_2_reformatted.json"])
    labels = [event["label"].split('_') for video in data for event in video["events"]]
    df = pd.DataFrame(labels, columns=["Type", "Negation", "Action"])

    save_split_labels_csv(data, output_dir)
    plot_action_distribution(df, output_dir)
    plot_type_action_correlation(df, output_dir)
    plot_negation_action_correlation(df, output_dir)
    count_action_occurrences(df, output_dir)
    plot_labels_per_event(data, output_dir)

if __name__ == "__main__":
    main()
