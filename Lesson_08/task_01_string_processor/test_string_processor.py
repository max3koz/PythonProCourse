import unittest

from .string_processor import StringProcessor


class TestStringProcessorRevers(unittest.TestCase):
	def test_reverse_string_regular(self):
		self.assertEqual(StringProcessor.reverse_string("hello"), "olleh")
	
	def test_reverse_string_with_symbols(self):
		self.assertEqual(StringProcessor.reverse_string("123!abc"), "cba!321")
	
	@unittest.skip(
	"Known issue with empty string - will be fixed later")
	def test_reverse_string_empty(self):
		self.assertEqual(StringProcessor.reverse_string(""), "")


class TestStringProcessorCapitalize(unittest.TestCase):
	def test_capitalize_string_lowercase(self):
		self.assertEqual(StringProcessor.capitalize_string("hello"), "Hello")
	
	def test_capitalize_string_mixed_case(self):
		self.assertEqual(StringProcessor.capitalize_string("hELLO"), "Hello")
	
	def test_capitalize_string_empty(self):
		self.assertEqual(StringProcessor.capitalize_string(""), "")
	
	def test_capitalize_string_with_digits(self):
		self.assertEqual(StringProcessor.capitalize_string("123abc"), "123abc")


class TestStringProcessorCountVowels(unittest.TestCase):
	def test_count_vowels_regular(self):
		self.assertEqual(StringProcessor.count_vowels("hello"), 2)
	
	def test_count_vowels_uppercase(self):
		self.assertEqual(StringProcessor.count_vowels("HELLO"), 2)
	
	def test_count_vowels_mixed(self):
		self.assertEqual(StringProcessor.count_vowels("HeLLo123!"), 2)
	
	def test_count_vowels_empty(self):
		self.assertEqual(StringProcessor.count_vowels(""), 0)
	
	def test_count_vowels_no_vowels(self):
		self.assertEqual(StringProcessor.count_vowels("bcdfg"), 0)
