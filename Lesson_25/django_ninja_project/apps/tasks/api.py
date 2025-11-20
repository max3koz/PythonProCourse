from functools import wraps

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Task
from .schemas import TaskOut, TaskCreateIn, TaskUpdateIn


def api_login_required(view_func):
	@wraps(view_func)
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({"detail": "Authentication required"},
			                    status=401)
		return view_func(request, *args, **kwargs)
	
	return wrapper


router = Router(tags=["Tasks"])


@router.get("/", response=list[TaskOut])
@api_login_required
def list_tasks(request, status: str | None = None, order_by: str | None = None):
	""""Returns the list of tasks for the current user."""
	qs = Task.objects.filter(user=request.user)
	if status:
		qs = qs.filter(status=status)
	if order_by:
		qs = qs.order_by(order_by)
	return list(qs)


@router.get("/{task_id}", response=TaskOut)
@api_login_required
def get_task(request, task_id: int) -> Task:
	"""Get one task by the current user ID."""
	return get_object_or_404(Task, id=task_id, user=request.user)


@router.post("/", response=TaskOut)
@api_login_required
def create_task(request, data: TaskCreateIn) -> Task:
	"""Create a new task for the current user."""
	return Task.objects.create(user=request.user, **data.dict())


@router.put("/{task_id}", response=TaskOut)
@api_login_required
def update_task(request, task_id: int, data: TaskUpdateIn) -> Task:
	"""Update an existing task."""
	task = get_object_or_404(Task, id=task_id, user=request.user)
	for field, value in data.dict(exclude_unset=True).items():
		setattr(task, field, value)
	task.save()
	return task


@router.delete("/{task_id}")
@api_login_required
def delete_task(request, task_id: int) -> dict[str, bool]:
	# 	"""Delete the current user's task."""
	task = get_object_or_404(Task, id=task_id, user=request.user)
	task.delete()
	return {"success": True}
