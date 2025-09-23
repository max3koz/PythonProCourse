import pytest
from assertpy import assert_that

from .file_processor import FileProcessor


def test_file_write_read(tmpdir):
	file = tmpdir.join("testfile.txt")
	FileProcessor.write_to_file(str(file), "Hello, World!")
	content = FileProcessor.read_from_file(str(file))
	assert_that(content == "Hello, World!",
	            "Error: somthing wrong!").is_true()


def test_empty_string(tmpdir):
	file = tmpdir.join("empty.txt")
	FileProcessor.write_to_file(str(file), "")
	content = FileProcessor.read_from_file(str(file))
	assert_that(content == "",
	            "Error: somthing wrong!").is_true()


def test_large_data(tmpdir):
	file = tmpdir.join("large.txt")
	large_text = "A" * 10 ** 6  # 1 MB of 'A'
	FileProcessor.write_to_file(str(file), large_text)
	content = FileProcessor.read_from_file(str(file))
	assert_that(content == large_text,
	            "Error: somthing wrong!").is_true()


def test_file_not_found():
	with pytest.raises(FileNotFoundError):
		FileProcessor.read_from_file("non_existent_file.txt")
