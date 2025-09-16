from __future__ import annotations
import time


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        self.elapsed = 0.0
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False
