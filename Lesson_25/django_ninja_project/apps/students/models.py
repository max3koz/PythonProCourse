from django.db import models


class Student(models.Model):
	"""Represents a student."""
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	
	def __str__(self) -> str:
		return self.name


class Course(models.Model):
	"""Represents a course."""
	title = models.CharField(max_length=200)
	description = models.TextField()
	
	def __str__(self) -> str:
		return self.title


class Enrollment(models.Model):
	"""Represents student enrollment in a course."""
	student = models.ForeignKey(Student, on_delete=models.CASCADE,
	                            related_name="enrollments")
	course = models.ForeignKey(Course, on_delete=models.CASCADE,
	                           related_name="enrollments")
	enrolled_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self) -> str:
		return f"{self.student.name} enrolled in {self.course.title}"


class ExamResult(models.Model):
	"""Represents exam results for a student in a course."""
	student = models.ForeignKey(Student, on_delete=models.CASCADE,
	                            related_name="results")
	course = models.ForeignKey(Course, on_delete=models.CASCADE,
	                           related_name="results")
	score = models.FloatField()
	
	def __str__(self) -> str:
		return f"{self.student.name} - {self.course.title}: {self.score}"
