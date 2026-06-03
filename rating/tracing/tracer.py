# tracing/tracer.py

import time

class Tracer:
    def __init__(self):
        self.events = []

    def start(self, step):
        self.events.append({
            "step": step,
            "event": "start",
            "ts": time.time()
        })

    def end(self, step, context):
        self.events.append({
            "step": step,
            "event": "end",
            "ts": time.time(),
            "snapshot": {
                "vehicle_count": len(context.vehicles),
                "has_policy": context.quote_version is not None
            }
        })