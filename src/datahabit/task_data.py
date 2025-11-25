"""
task_data.py
------------
Stores structured information about each submitted task.
Includes validation and built-in error handling.
"""

from datetime import datetime


class TaskData:
    """Represents a single academic task submission."""

    def __init__(self, student_id: str, task_name: str, submission_time):
        # --- VALIDATION / ERROR HANDLING ---
        if not student_id or not isinstance(student_id, str):
            raise ValueError("student_id must be a non-empty string.")

        if not task_name or not isinstance(task_name, str):
            raise ValueError("task_name must be a non-empty string.")

        if isinstance(submission_time, str):
            try:
                submission_time = datetime.fromisoformat(submission_time)
            except ValueError:
                raise ValueError("submission_time string must follow ISO format YYYY-MM-DD HH:MM:SS")
        elif not isinstance(submission_time, datetime):
            raise TypeError("submission_time must be a datetime object or ISO-format string.")

        self._student_id = student_id
        self._task_name = task_name
        self._submission_time = submission_time

    # ---------------------------
    # GETTERS
    # ---------------------------
    @property
    def student_id(self):
        return self._student_id

    @property
    def task_name(self):
        return self._task_name

    @property
    def submission_time(self):
        return self._submission_time

    # ---------------------------
    # CORE FUNCTIONALITY
    # ---------------------------
    def get_delay(self, due_date):
        if not isinstance(due_date, datetime):
            raise TypeError("due_date must be a datetime object.")

        return self._submission_time - due_date

    def __repr__(self):
        return f"TaskData(student={self._student_id}, task='{self._task_name}', time={self._submission_time})"
