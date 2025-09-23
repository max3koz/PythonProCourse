from typing import List, Tuple

from assertpy.assertpy import assert_that


def filter_adults(people: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
	"""
	Filters out underage individuals from a list of people.
	Parameters:
	- people (List[Tuple[str, int]]): A list of tuples, each containing
	  a person's name and age.
	Returns:
	- List[Tuple[str, int]]: A list containing only those individuals who are
	  18 years old or older.
	"""
	return [person for person in people if person[1] >= 18]


def test_filter_adults_basic():
	test_people_data = [("Андрій", 25),
	                    ("Олег", 16),
	                    ("Марія", 19),
	                    ("Ірина", 15)]
	expected_result = [("Андрій", 25),
	                   ("Марія", 19)]
	actual_result = filter_adults(test_people_data)
	assert_that(actual_result == expected_result).is_true()
	
def test_filter_adults_empty_list():
	test_people_data = []
	expected_result = []
	actual_result = filter_adults(test_people_data)
	assert_that (actual_result == expected_result).is_true()
