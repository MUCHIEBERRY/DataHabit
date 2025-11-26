"""
task_data.py
-------------
Strict, well-typed TaskData class with defensive validation and helpful errors.

Package: DataHabit
"""

from __future__ import annotations
from datetime import datetime
from typing import Union


class TaskDataError(Exception):
    """Base exception for TaskData related errors."""
    pass


class TaskData:
    """
    Represents a single student task submission.

    This class enforces strict types and validates timestamps on construction.
    It intentionally fails fast (raises) when inputs are invalid so callers
    must handle or correct upstream data first.

    Attributes
    ----------
    student_id : str
        Unique identifier for the student.
    task_name : str
        Short title/name of the task.
    submission_time : datetime
        Parsed submission timestamp as a datetime object.
    """

    def __init__(self, student_id: str, task_name: str, submission_time: Union[str, datetime]):
        # Validate student_id
        if not isinstance(student_id, str) or not student_id.strip():
            raise TaskDataError("student_id must be a non-empty string.")
        self._student_id: str = student_id.strip()

        # Validate task_name
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskDataError("task_name must be a non-empty string.")
        self._task_name: str = task_name.strip()

        # Parse and validate submission_time
        self._submission_time: datetime = self._parse_submission_time(submission_time)

    # -----------------------
    # Internal helpers
    # -----------------------
    @staticmethod
    def _parse_submission_time(value: Union[str, datetime]) -> datetime:
        """
        Convert a string or datetime to a datetime object.

        Accepts ISO-like strings: "YYYY-MM-DD HH:MM:SS" or full ISO "YYYY-MM-DDTHH:MM:SS".
        Raises TaskDataError on invalid formats or types.
        """
        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            raise TaskDataError("submission_time must be a datetime or ISO-format string.")

        # Try several common parse approaches in deterministic order
        # 1) datetime.fromisoformat handles "YYYY-MM-DD" and "YYYY-MM-DDTHH:MM:SS" and with optional microseconds
        try:
            dt = datetime.fromisoformat(value)
            return dt
        except ValueError:
            pass

        # 2) Try explicit format "YYYY-MM-DD HH:MM:SS"
        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return dt
        except ValueError:
            pass

        # If both fail, raise a clear error
        raise TaskDataError(
            "submission_time string must be ISO-like (e.g. 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DDTHH:MM:SS')."
        )

    # -----------------------
    # Properties (read-only)
    # -----------------------
    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def submission_time(self) -> datetime:
        return self._submission_time

    # -----------------------
    # Core functionality
    # -----------------------
    def get_delay(self, due_date: Union[str, datetime]) -> float:
        """
        Compute the delay in hours between submission_time and due_date.

        Parameters
        ----------
        due_date : str | datetime
            The due date (string or datetime). Strings must be in the same ISO-like formats accepted above.

        Returns
        -------
        float
            Number of hours (positive => late, negative => early).

        Raises
        ------
        TaskDataError
            If due_date is invalid.
        """
        if isinstance(due_date, str):
            # re-use parsing logic (raises TaskDataError on failure)
            try:
                due_dt = TaskData._parse_submission_time(due_date)
            except TaskDataError as e:
                raise TaskDataError(f"Invalid due_date: {e}")
        elif isinstance(due_date, datetime):
            due_dt = due_date
        else:
            raise TaskDataError("due_date must be a datetime or ISO-format string.")

        delta = self._submission_time - due_dt
        hours = delta.total_seconds() / 3600.0
        return hours

    # -----------------------
    # Representations
    # -----------------------
    def __repr__(self) -> str:
        ts = self._submission_time.isoformat(sep=" ", timespec="seconds")
        return f"TaskData(student_id={self._student_id!r}, task_name={self._task_name!r}, submitted={ts!r})"

    def to_dict(self) -> dict:
        """Return a lightweight dict for reporting or serialization."""
        return {
            "student_id": self._student_id,
            "task_name": self._task_name,
            "submission_time": self._submission_time.isoformat(sep=" ", timespec="seconds")
        }
