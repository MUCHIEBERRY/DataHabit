"""
behavior_analyzer.py
--------------------
Analyzes submission delays and classifies academic behavior.
"""

from datetime import datetime
import statistics
from .task_data import TaskData


class BehaviorAnalyzer(TaskData):
    """Extends TaskData with behavior logic."""

    def __init__(self, student_id, task_name, submission_time):
        super().__init__(student_id, task_name, submission_time)
        self._behavior_label = None
        self._delay_history = []

    def classify_behavior(self, due_date):
        if not isinstance(due_date, datetime):
            raise TypeError("due_date must be a datetime object.")

        delay = self.get_delay(due_date)
        delay_hours = delay.total_seconds() / 3600
        self._delay_history.append(delay_hours)

        avg = statistics.mean(self._delay_history)

        # --- RULES ---
        if avg > 24:
            self._behavior_label = "Procrastinator"
        elif avg < -24:
            self._behavior_label = "Early Finisher"
        elif -3 <= avg <= 3:
            self._behavior_label = "Consistent Worker"
        else:
            self._behavior_label = "Moderate / Mixed"

        return self._behavior_label

    def get_statistics(self):
        if not self._delay_history:
            return {"message": "No delay history recorded yet."}

        avg = statistics.mean(self._delay_history)
        variation = statistics.stdev(self._delay_history) if len(self._delay_history) > 1 else 0

        return {
            "tasks_analyzed": len(self._delay_history),
            "avg_delay_hours": avg,
            "consistency_std_dev": variation,
            "behavior_label": self._behavior_label
        }

    def __repr__(self):
        return f"BehaviorAnalyzer(student={self._student_id}, label={self._behavior_label})"
