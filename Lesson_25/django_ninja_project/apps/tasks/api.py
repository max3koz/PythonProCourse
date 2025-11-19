from __future__ import annotations

from typing import List, Optional

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Task
from .schemas import TaskOut, TaskCreateIn, TaskUpdateIn

router = Router(tags=["Tasks"])


def ensure_auth(request: HttpRequest) -> None:
	"""Checks user authentication for any request."""
	if not request.user.is_authenticated:
		raise PermissionDenied("Authentication required")

# ------------------ Task ------------------
@router.get("/", response=List[TaskOut])
def list_tasks(request: HttpRequest, status: Optional[str] = None,
               order_by: Optional[str] = None, ) -> List[Task]:
	"""Returns the list of tasks for the current user."""
	ensure_auth(request)
	qs: QuerySet[Task] = Task.objects.filter(user=request.user)
	if status:
		qs = qs.filter(status=status)
	if order_by:
		qs = qs.order_by(order_by)
	return list(qs)


@router.get("/{task_id}", response=TaskOut)
def get_task(request: HttpRequest, task_id: int) -> Task:
	"""Get one task by the current user ID."""
	ensure_auth(request)
	return get_object_or_404(Task, id=task_id, user=request.user)


@router.post("/", response=TaskOut)
def create_task(request: HttpRequest, data: TaskCreateIn) -> Task:
	"""Create a new task for the current user."""
	ensure_auth(request)
	task: Task = Task.objects.create(user=request.user, **data.dict())
	return task


@router.put("/{task_id}", response=TaskOut)
def update_task(request: HttpRequest, task_id: int, data: TaskUpdateIn) -> Task:
	"""Update an existing task."""
	ensure_auth(request)
	task: Task = get_object_or_404(Task, id=task_id, user=request.user)
	for field, value in data.dict(exclude_unset=True).items():
		setattr(task, field, value)
	task.save()
	return task


@router.delete("/{task_id}")
def delete_task(request: HttpRequest, task_id: int) -> dict[str, bool]:
	"""Delete the current user's task."""
	ensure_auth(request)
	task: Task = get_object_or_404(Task, id=task_id, user=request.user)
	task.delete()
	return {"success": True}
