from datetime import datetime

from ninja import Schema


class StudentIn(Schema):
	name: str
	email: str


class StudentOut(Schema):
	id: int
	name: str
	email: str


class CourseIn(Schema):
	title: str
	description: str


class CourseOut(Schema):
	id: int
	title: str
	description: str


class EnrollmentIn(Schema):
	student_id: int
	course_id: int


class EnrollmentOut(Schema):
	id: int
	student_id: int
	course_id: int
	enrolled_at: datetime


class ExamResultIn(Schema):
	student_id: int
	course_id: int
	score: float


class ExamResultOut(Schema):
	id: int
	student_id: int
	course_id: int
	score: float
