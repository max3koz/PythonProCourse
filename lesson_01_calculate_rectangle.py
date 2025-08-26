from assertpy import assert_that

class Rectangle:
	def __init__(self, weight: float, height: float):
		self.weight = weight
		self.height = height
	
	
	def area(self) -> float:
		return self.weight * self.height
	
	
	def perimeter(self) -> float:
		return 2 * (self.weight + self.height)
	
	
	def is_square(self) -> float:
		return self.weight == self.height
	
	
	def resize(self, new_weight, new_height):
		self.weight = new_weight
		self.height = new_height
		
print("Test 1: calculate circle area.")
rectangle_sample = Rectangle(10.5, 5.5)
expected_result = 57.75
actual_result = rectangle_sample.area()
if assert_that(actual_result,f"Error: unexpected value of circle area: "
                          f"{actual_result}").is_equal_to(expected_result):
	print("Test 'calculate_circle_area' is Done!!!")
print()

print("Test 2: calculate circle perimeter.")
expected_result = 32
actual_result = rectangle_sample.perimeter()
if assert_that(actual_result,
               f"Error: unexpected value of the circle perimeter: "
               f"{actual_result}").is_equal_to(expected_result):
	print("Test 'calculate_circle_perimeter' is Done!!!")
print()
	
print("Test 3: the rectangle is not a square.")
actual_result = rectangle_sample.is_square()
if assert_that(actual_result,
               f"Error: the rectangle is a square: "
               f"{actual_result}").is_equal_to(False):
	print("Test is Done, the rectangle is not a square!!!")
print()
	
print("Test 4: the rectangle is a square after resize rectangle")
rectangle_sample.resize(20,20)
actual_result = rectangle_sample.is_square()
if assert_that(actual_result,
               f"Error: the rectangle is not a square: "
               f"{actual_result}").is_equal_to(True):
	print("Test is Done, the rectangle is a square after resize rectangle!!!")
print()
	