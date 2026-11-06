import json
import urllib.request

ENDPOINT = "https://api.tracker.example/v1/track"


def track(event, props):
    body = json.dumps({"event": event, "properties": props}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST")
    try:
        urllib.request.urlopen(req, timeout=2)
    except Exception:
        pass