import time
import threading
import uvicorn
from fastapi import FastAPI
from datetime import datetime, UTC
from monitor import GitHubMonitor

# Initialize monitor
monitor = GitHubMonitor(repo="microsoft/vscode")

# Initialize API
app = FastAPI(title="GitHub Monitor API")


# -------------------------------
# BACKGROUND MONITOR + TERMINAL LOGGING
# -------------------------------
def monitor_loop():
    while True:
        monitor.fetch_events()

        # ⭐ Terminal output
        print("\n=== LIVE METRICS (microsoft/vscode) ===")
        print("Event counts (last 60 min):", monitor.event_counts(60))

        print("\nPullRequestEvent timestamps:")
        for ts in monitor.pr_times["microsoft/vscode"]:
            print(" -", ts)

        avg = monitor.avg_pr_interval()
        print("\nAverage PullRequestEvent interval (seconds):", avg)
        print("===========================================\n")

        time.sleep(30)


# Start monitor thread on startup
@app.on_event("startup")
async def start_background_monitor():
    threading.Thread(target=monitor_loop, daemon=True).start()


# -------------------------------
# API ENDPOINTS
# -------------------------------
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
        "repo": "microsoft/vscode",
        "avg_interval_seconds": monitor.avg_pr_interval(),
        "timestamp": datetime.now(UTC).isoformat()
    }


@app.get("/metrics/visualization")
def api_visualization(offset: int = 30):
    counts = monitor.event_counts(offset)

    visualization = [
        {"event_type": etype, "count": count, "bar": "#" * count}
        for etype, count in counts.items()
    ]

    return {
        "offset_minutes": offset,
        "visualization": visualization,
        "timestamp": datetime.now(UTC).isoformat()
    }


# -------------------------------
# RUN UVICORN PROGRAMMATICALLY
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
