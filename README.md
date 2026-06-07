# GitHub Events Monitor

A Python‑based monitoring service that streams GitHub repository events (WatchEvent, PullRequestEvent, IssuesEvent), computes real‑time metrics, prints them to the terminal, and exposes the same metrics through a REST API built with FastAPI.

## Architecture (C4 L1)



## Flow Summary
The Event Monitor Service polls the GitHub Events API for a specific repository (microsoft/vscode).\n
->It filters relevant event types and computes:
-Average time between PullRequestEvents
-Event counts grouped by event type for a given offset

->Metrics are:
-Printed live in the terminal
-Exposed via REST API endpoints


## Components

- **Event Monitor:**Continuously polls https://api.github.com/repos/microsoft/vscode/events, filters the target event types (WatchEvent, PullRequestEvent, IssuesEvent),stores them in memory, and computes the required metrics (average PR interval + event counts).Also prints live metrics to the terminal.
- **REST API Service:** A FastAPI‑based service that runs the monitor in a background thread and exposes the metrics through HTTP endpoints.
  Provides /metrics/event-counts, /metrics/avg-pr-interval, and /metrics/visualization.
- **Requirements File:** Defines the minimal dependencies (fastapi, uvicorn, requests) needed to run the monitoring service and REST API.

## Setup

1) Python env
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

2) Run monitor
- python service/python monitor.py            # This prints live metrics every 30 seconds
- python service/python api.py --once     # This script runs:The monitor loop,The FastAPI server,Terminal logging
