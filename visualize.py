import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def visualize_event_counts(monitor, minutes=60, filename="events.png"):
    counts = monitor.event_counts(minutes)

    event_types = ["WatchEvent", "PullRequestEvent", "IssuesEvent"]
    values = [counts.get(e, 0) for e in event_types]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(event_types, values, color=["#4C72B0", "#55A868", "#C44E52"])

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.1, str(height),
                 ha="center", va="bottom", fontsize=12)

    plt.title(f"GitHub Events in Last {minutes} Minutes", fontsize=16)
    plt.ylabel("Number of Events", fontsize=14)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    print(f"Saved to: {os.path.abspath(filename)}")
