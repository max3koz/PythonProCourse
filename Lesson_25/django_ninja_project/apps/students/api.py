from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response

from .models import Student, Course, Enrollment, ExamResult
from .schemas import (StudentIn, StudentOut, CourseIn, CourseOut, EnrollmentIn,
                      EnrollmentOut, ExamResultIn, ExamResultOut)

students_router = Router(tags=["students"])


# ------------------ Students ------------------
@students_router.post("/students/", response=StudentOut)
@login_required
def create_student(request: HttpRequest, payload: StudentIn) -> Response:
	"""Create a new student."""
	student: Student = Student.objects.create(**payload.dict())
	return Response(StudentOut.from_orm(student), status=201)


@students_router.get("/students/", response=list[StudentOut])
@login_required
def list_students(request: HttpRequest) -> list[Student]:
	"""Retrieve all students."""
	return Student.objects.all()


@students_router.get("/students/{student_id}", response=StudentOut)
@login_required
def get_student(request: HttpRequest, student_id: int) -> Student:
	"""Retrieve a single student by ID."""
	return get_object_or_404(Student, id=student_id)


@students_router.put("/students/{student_id}", response=StudentOut)
@login_required
def update_student(request: HttpRequest, student_id: int,
                   payload: StudentIn) -> Student:
	"""Update an existing student."""
	student: Student = get_object_or_404(Student, id=student_id)
	for attr, value in payload.dict().items():
		setattr(student, attr, value)
	student.save()
	return student


@students_router.delete("/students/{student_id}")
@login_required
def delete_student(request: HttpRequest, student_id: int) -> dict[str, bool]:
	"""Delete a student."""
	student: Student = get_object_or_404(Student, id=student_id)
	student.delete()
	return {"success": True}


# ------------------ Courses ------------------
@students_router.post("/courses/", response=CourseOut)
@login_required
def create_course(request: HttpRequest, payload: CourseIn) -> Response:
	"""Create a new course."""
	course: Course = Course.objects.create(**payload.dict())
	return Response(CourseOut.from_orm(course), status=201)


@students_router.get("/courses/", response=list[CourseOut])
@login_required
def list_courses(request: HttpRequest) -> list[Course]:
	"""Retrieve all courses."""
	return Course.objects.all()


@students_router.get("/courses/{course_id}", response=CourseOut)
@login_required
def get_course(request: HttpRequest, course_id: int) -> Course:
	"""Retrieve a single course by ID."""
	return get_object_or_404(Course, id=course_id)


@students_router.put("/courses/{course_id}", response=CourseOut)
@login_required
def update_course(request: HttpRequest, course_id: int,
                  payload: CourseIn) -> Course:
	"""Update an existing course."""
	course: Course = get_object_or_404(Course, id=course_id)
	for attr, value in payload.dict().items():
		setattr(course, attr, value)
	course.save()
	return course


@students_router.delete("/courses/{course_id}")
@login_required
def delete_course(request: HttpRequest, course_id: int) -> dict[str, bool]:
	"""Delete a course."""
	course: Course = get_object_or_404(Course, id=course_id)
	course.delete()
	return {"success": True}


# ------------------ Enrollment ------------------
@students_router.post("/enrollments/", response=EnrollmentOut)
@login_required
def enroll_student(request: HttpRequest, payload: EnrollmentIn) -> Response:
	"""Enroll a student in a course."""
	student: Student = get_object_or_404(Student, id=payload.student_id)
	course: Course = get_object_or_404(Course, id=payload.course_id)
	enrollment: Enrollment = Enrollment.objects.create(student=student,
	                                                   course=course)
	return Response(EnrollmentOut.from_orm(enrollment), status=201)


# ------------------ Exam Results ------------------
@students_router.post("/results/", response=ExamResultOut)
@login_required
def add_result(request: HttpRequest, payload: ExamResultIn) -> Response:
	"""Add exam result for a student in a course."""
	student: Student = get_object_or_404(Student, id=payload.student_id)
	course: Course = get_object_or_404(Course, id=payload.course_id)
	result: ExamResult = ExamResult.objects.create(
		student=student, course=course, score=payload.score
	)
	return Response(ExamResultOut.from_orm(result), status=201)


@students_router.get("/results/{course_id}")
@login_required
def average_score(request: HttpRequest, course_id: int) -> dict[
	str, float | str]:
	"""Calculate average exam score for a course."""
	course: Course = get_object_or_404(Course, id=course_id)
	avg: float = course.results.aggregate(avg_score=Avg("score"))[
		             "avg_score"] or 0.0
	return {"course": course.title, "average_score": avg}
