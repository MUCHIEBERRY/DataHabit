"""
data_cleaner.py
---------------
Cleans raw timestamps, handles invalid formats, deduplicates, and sorts data.
"""

from datetime import datetime


class DataCleaner:
    """Cleans and standardizes raw timestamp data."""

    def __init__(self, raw_timestamps):
        if not isinstance(raw_timestamps, list):
            raise TypeError("raw_timestamps must be a list.")

        self.raw = raw_timestamps
        self.cleaned = []

    def clean(self):
        """Convert raw timestamps to datetime objects."""
        for ts in self.raw:
            if isinstance(ts, datetime):
                self.cleaned.append(ts)
                continue

            if isinstance(ts, str):
                try:
                    parsed = datetime.fromisoformat(ts)
                    self.cleaned.append(parsed)
                except ValueError:
                    print(f"[WARNING] Skipped invalid timestamp: {ts}")
                continue

            print(f"[WARNING] Skipped unsupported type: {ts}")

        # Deduplicate + sort
        self.cleaned = sorted(list(set(self.cleaned)))
        return self.cleaned

    def count_invalid(self):
        """Counts how many raw items are invalid."""
        valid = len(self.cleaned)
        total = len(self.raw)
        return total - valid
