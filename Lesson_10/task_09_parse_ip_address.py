import re
from pathlib import Path
from typing import Dict

from assertpy import assert_that


def count_requests_by_ip_from_file(file_path: str) -> Dict[str, int]:
	"""
	The function parses a web server log file and counts the number
	of requests per IP address.
	Args:
		file_path (str): Path to the log file.
	Returns:
		Dict[str, int]: A dictionary mapping each IP address to its request count.
	"""
	ip_pattern = re.compile(r'\] - (\d{1,3}(?:\.\d{1,3}){3})')
	stats: Dict[str, int] = {}
	
	with open(file_path, 'r', encoding='utf-8') as file:
		for line in file:
			match = ip_pattern.search(line)
			if match:
				ip = match.group(1)
				stats[ip] = stats.get(ip, 0) + 1
	
	return stats


def test_count_requests_by_ip_existing_file():
	path_to_log_file = Path(__file__).parent / "task_09_log_file.log"
	expected_result = {
		"192.168.1.10": 2,
		"192.168.1.11": 2,
		"10.0.0.5": 1
	}
	
	actual_result = count_requests_by_ip_from_file(str(path_to_log_file))
	assert_that(actual_result,
	            f"Error: unexpected result {actual_result}").is_equal_to(
		expected_result)
