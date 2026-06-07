import requests
import logging
from datetime import datetime, timedelta, UTC
from collections import defaultdict


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

RELEVANT_EVENTS = {"WatchEvent", "PullRequestEvent", "IssuesEvent"}


class GitHubMonitor:
    def __init__(self, repo):
        self.repo = repo.lower()
        self.pr_times = defaultdict(list)
        self.events = []
        self.seen_ids = set()

    def _url(self):
        return f"https://api.github.com/repos/{self.repo}/events"

    def fetch_events(self):
        try:
            response = requests.get(self._url(), timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"GitHub API returned status {response.status_code} for {self.repo}")
                return

            for event in response.json():
                etype = event.get("type")
                if etype not in RELEVANT_EVENTS:
                    continue

                eid = event.get("id")
                if not eid or eid in self.seen_ids:
                    continue

                self.seen_ids.add(eid)

                created_at = event.get("created_at")
                if not created_at:
                    continue

                ts = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                ts = ts.replace(microsecond=0)

                self.events.append({"type": etype, "created_at": ts})

                if etype == "PullRequestEvent":
                    self.pr_times[self.repo].append(ts)

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching events for {self.repo}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in fetch_events for {self.repo}: {e}")

    def event_counts(self, minutes):
        cutoff = (datetime.now(UTC) - timedelta(minutes=minutes)).replace(microsecond=0)
        counts = defaultdict(int)
        for e in self.events:
            if e["created_at"] >= cutoff:
                counts[e["type"]] += 1
        return dict(counts)

    def avg_pr_interval(self, window=60):
        times = self.pr_times[self.repo]
        if len(times) < 2:
            return None
        cutoff = (datetime.now(UTC) - timedelta(minutes=window)).replace(microsecond=0)
        filtered = sorted(t for t in times if t >= cutoff)
        if len(filtered) < 2:
            return None
        diffs = [(filtered[i] - filtered[i-1]).total_seconds()
                 for i in range(1, len(filtered))]
        avg_minutes = (sum(diffs) / len(diffs)) / 60
        return round(avg_minutes, 2)

    def pr_debug(self, window=60):
        times = sorted(self.pr_times[self.repo])
        cutoff = (datetime.now(UTC) - timedelta(minutes=window)).replace(microsecond=0)
        filtered = [t for t in times if t >= cutoff]
        diffs = [(filtered[i] - filtered[i-1]).total_seconds()
                 for i in range(1, len(filtered))]
        avg_minutes = round((sum(diffs) / len(diffs)) / 60, 2) if diffs else None
        return cutoff, filtered, diffs, avg_minutes
