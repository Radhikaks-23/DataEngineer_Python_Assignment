import time
import threading
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime, UTC
from monitor import GitHubMonitor
from visualize import visualize_event_counts

monitor = GitHubMonitor(repo="microsoft/vscode")
app = FastAPI(title="GitHub Monitor API")

def print_live_metrics():
    print("\n=== LIVE METRICS ===")
    counts = monitor.event_counts(60)
    print(f"Event counts (last 60 min): {counts}\n")

    print("Raw PullRequestEvent timestamps:")
    for ts in sorted(monitor.pr_times[monitor.repo]):
        print(f" - {ts}")
    print()

    cutoff, filtered, diffs, avg_minutes = monitor.pr_debug(60)

    print("=== Cutoff Time ===")
    print(f"Cutoff: {cutoff}\n")

    print("Timestamps used:")
    for ts in filtered:
        print(f" - {ts}")
    print()

    print("Diffs (seconds):")
    for d in diffs:
        print(f" - {d}")
    print("==============================\n")

    print(f"Average PullRequestEvent interval (minutes): {avg_minutes}\n")

def monitor_loop():
    while True:
        monitor.fetch_events()
        print_live_metrics()
        time.sleep(30)

@app.on_event("startup")
async def start_background_monitor():
    threading.Thread(target=monitor_loop, daemon=True).start()

@app.get("/metrics/event-counts")
def api_event_counts(offset: int = 10):
    return {
        "offset_minutes": offset,
        "event_counts": monitor.event_counts(offset),
        "timestamp": datetime.now(UTC).isoformat()
    }

@app.get("/metrics/avg-pr-interval")
def api_avg_pr():
    return {
        "repo": monitor.repo,
        "avg_interval_minutes": monitor.avg_pr_interval(),
        "timestamp": datetime.now(UTC).isoformat()
    }

@app.get("/metrics/visualization")
def api_visualization(offset: int = 30):
    counts = monitor.event_counts(offset)
    visualization = [{"event_type": e, "count": c, "bar": "#" * c}
                     for e, c in counts.items()]
    return {
        "offset_minutes": offset,
        "visualization": visualization,
        "timestamp": datetime.now(UTC).isoformat()
    }

@app.get("/metrics/visualization-image")
def api_visualization_image(offset: int = 30):
    filename = "events.png"
    visualize_event_counts(monitor, minutes=offset, filename=filename)
    return FileResponse(filename, media_type="image/png", filename=filename)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
