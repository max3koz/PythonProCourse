import csv
import os
from typing import List, Dict


class StudentManager:
	
	def __init__(self, csv_file_name: str):
		"""Initializes the student manager with the specified CSV file."""
		self.csv_file_name = csv_file_name
	
	def read_students_data(self) -> List[Dict[str, str]]:
		"""Reads students from a CSV file."""
		with open(self.csv_file_name, mode="r", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			return list(reader)
	
	def calculate_average_grade(self) -> float:
		"""Calculates the average grade for all students."""
		students = self.read_students_data()
		grades = [int(student["Grade"]) for student in students]
		return sum(grades) / len(grades) if grades else 0.0
	
	def add_student(self, name: str, age: int, grade: int) -> None:
		"""Add a new student to the CSV file."""
		file_exists = os.path.isfile(self.csv_file_name)
		write_header = not file_exists or os.path.getsize(
			self.csv_file_name) == 0
		
		with open(self.csv_file_name, mode="a", encoding='utf-8') as file:
			writer = csv.writer(file)
			writer.writerow([name, age, grade])
		print(f"Added student {name} with grade {grade}")


manager = StudentManager("task_03_students_data.csv")

average_grade = manager.calculate_average_grade()
print(f"Average grade of student in the list is {average_grade:.2f}")
manager.add_student("Maksym", 51, 5)
average_grade = manager.calculate_average_grade()
print(f"Average grade of student in the list is {average_grade:.2f}")
