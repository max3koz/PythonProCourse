from unittest.mock import patch, Mock

import pytest
import requests


def fetch_data(url: str) -> dict:
	response = requests.get(url)
	response.raise_for_status()
	return response.json()


@patch("requests.get")
def test_fetch_data_success(mock_get):
	mock_response = Mock()
	mock_response.json.return_value = {"status": "ok", "data": [1, 2, 3]}
	mock_get.return_value = mock_response
	
	result = fetch_data("https://example.com/api")
	assert result == {"status": "ok", "data": [1, 2, 3]}
	mock_get.assert_called_once_with("https://example.com/api")


@patch("requests.get")
def test_fetch_data_http_error(mock_get):
	mock_response = Mock()
	mock_response.raise_for_status.side_effect = Exception("404 error")
	mock_get.return_value = mock_response
	
	with pytest.raises(Exception):
		fetch_data("https://example.com/bad")

#
# def is_prime(num: int) -> bool:
# 	if num < 2:
# 		return False
# 	for i in range(2, num):
# 		if num % i == 0:
# 			return False
# 	return True
#
#
# @pytest.mark.parametrize("num", [
# 	2,3,5,7
# ])
# def test_primes(num):
# 	assert is_prime(num)
#
# @pytest.mark.parametrize("num", [
# 	0,1,4,9
# ])
# def test_non_primes(num):
# 	assert not is_prime(num)
