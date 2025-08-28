import math

def calculate_circle_area() -> float:
	radius = float(input(f"Enter the circlec radius value: "))
	return math.pi * radius ** 2
	
print(f"The area of the circle is : {calculate_circle_area()}")
