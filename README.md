# GitHub Events Monitor

A Python‑based monitoring service that streams GitHub repository events (WatchEvent, PullRequestEvent, IssuesEvent), computes real‑time metrics, prints them to the terminal, and exposes the same metrics through a REST API built with FastAPI.

## Architecture (C4 L1)
<img width="1318" height="528" alt="image" src="https://github.com/user-attachments/assets/d551fa30-e6c1-407c-b890-b28f8f6cf363" />



## Flow Summary
**Event Monitor Service:**
The Event Monitor Service polls the GitHub Events API for a specific repository (microsoft/vscode).
It processes only the relevant event types and computes the required metrics.

**Filters and processes:**
WatchEvent,
PullRequestEvent,
IssuesEvent

**Computes:**
Average time between PullRequestEvents
and Event counts grouped by event type for a given offset

**Metrics are delivered:**
Printed live in the terminal during continuous monitoring
and exposed via REST API endpoints for external access

## Components:
**monitor.py**
**Responsible for:**
Polling the GitHub Events API
Filtering relevant event types
Storing events in memory
Calculating metrics
Printing metrics to the terminal

**api.py**
**Responsible for:**
Starting the FastAPI application
Launching the monitor in a background thread
Exposing REST endpoints

**requirements.txt**
**Defines the required dependencies:**
fastapi
uvicorn
requests

## Setup

**1) Create Python Environment**(Open the project folder in VS Code.)
- python -m venv venv
- source venv/bin/activate
  
**2)Install Dependencies**
- pip install -r requirements.txt

**3) 3. Run Application**
- python api.py --once     # This script runs:The monitor loop,The FastAPI server, Live metrics details

## REST Endpoints
**Event Counts**
http://localhost:8000/metrics/event-counts?offset_minutes=60

Returns event counts grouped by type within the specified offset.

**Average Pull Request Interval**
http://localhost:8000/metrics/avg-pr-interval

**Visualization**
http://localhost:8000/metrics/visualization?offset_minutes=60


