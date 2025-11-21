from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from ninja import Schema


class TaskOut(Schema):
	"""
	The output data schema for the task.
	Fields:
		- id: Unique identifier for the task.
		- title: Name of the task.
		- description: Description of the task.
		- status: Status of the task (pending | done).
		- due_date: Due date (may be missing).
		- created_at: Date and time the task was created.
	"""
	id: int
	title: str
	description: str
	status: str
	due_date: Optional[date]
	created_at: datetime


class TaskCreateIn(Schema):
	"""
	Schema for creating a new task.
	Fields:
		- title: Task title (required).
		- description: Task description (optional).
		- due_date: Deadline date (optional).
	"""
	title: str
	description: Optional[str] = None
	due_date: Optional[date] = None


class TaskUpdateIn(Schema):
	"""
	Schema for updating an existing task.
	Fields:
		- title: New task title (optional).
		- description: New task description (optional).
		- status: New task status (pending | done).
		- due_date: New due date (optional).
	"""
	title: Optional[str] = None
	description: Optional[str] = None
	status: Optional[str] = None
	due_date: Optional[date] = None
