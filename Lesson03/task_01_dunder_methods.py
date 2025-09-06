from assertpy import assert_that


class Fraction:
	"""
	A class that represents a common fraction in numerator/denominator format.
	Supports basic arithmetic operations between Fraction objects.
	"""
	
	def __init__(self, numerator: int, denominator: int) -> None:
		"""
		Initializes a fraction object.
		Args: numerator (int): The numerator of the fraction,
		denominator (int): The denominator of the fraction.
		"""
		self.numerator = numerator
		self.denominator = denominator
	
	def __add__(self, other: 'Fraction') -> 'Fraction':
		"""
		Add two fractions.
		Args: other (Fraction): Another fraction.
		Returns:Fraction: The result of the addition.
		"""
		new_numerator = (self.numerator * other.denominator +
		                 other.numerator * self.denominator)
		new_denominator = self.denominator * other.denominator
		return Fraction(new_numerator, new_denominator)
	
	def __sub__(self, other: 'Fraction') -> 'Fraction':
		"""
		Subtracts one fraction from another.
		Args: other (Fraction): Another fraction.
		Returns: Fraction: The result of the subtraction.
		"""
		new_numerator = (self.numerator * other.denominator -
		                 other.numerator * self.denominator)
		new_denominator = self.denominator * other.denominator
		return Fraction(new_numerator, new_denominator)
	
	def __mul__(self, other: 'Fraction') -> 'Fraction':
		"""
		Multiplies two fractions.
		Args: other (Fraction): Another fraction.
		Returns: Fraction: The result of the multiplication.
		"""
		new_numerator = self.numerator * other.numerator
		new_denominator = self.denominator * other.denominator
		return Fraction(new_numerator, new_denominator)
	
	def __truediv__(self, other: 'Fraction') -> 'Fraction':
		"""
		Divides one fraction by another.
		Args: other (Fraction): Divisor.
		Returns: Fraction: The result of the division.
		"""
		new_numerator = self.numerator * other.denominator
		new_denominator = self.denominator * other.numerator
		return Fraction(new_numerator, new_denominator)
	
	def __repr__(self) -> str:
		"""
		Returns the string representation of a fraction.
		Returns: str: Format "numerator/denominator".
		"""
		return f"{self.numerator}/{self.denominator}"


fraction_1 = Fraction(1, 2)
fraction_2 = Fraction(3, 4)

print(f"a = {fraction_1}")
print(f"b = {fraction_2}")
add_fraction = fraction_1 + fraction_2
assert_that(str(add_fraction),
            f"Error: unexpected result: {add_fraction}").is_equal_to("10/8")
sub_fraction = fraction_1 - fraction_2
assert_that(str(sub_fraction),
            f"Error: unexpected result: {sub_fraction}").is_equal_to("-2/8")
mul_fraction = fraction_1 * fraction_2
assert_that(str(mul_fraction),
            f"Error: unexpected result: {mul_fraction}").is_equal_to("3/8")
truediv_fraction = fraction_1 / fraction_2
assert_that(str(truediv_fraction),
            f"Error: unexpected result: {truediv_fraction}").is_equal_to("4/6")
