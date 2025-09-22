from unittest.mock import patch

import pytest
from assertpy.assertpy import assert_that

from .bank_account import BankAccount


@pytest.fixture
def account():
	"""Fixture for creating an account with an initial balance"""
	test_acc = BankAccount()
	test_acc.deposit(100.0)
	return test_acc


@pytest.mark.parametrize("amount, expected", [
	(50.0, 150.0),
	(0.0, 100.0),
	(25.5, 125.5),
])
def test_deposit(account, amount, expected):
	"""Replenishment test with parameterization"""
	account.deposit(amount)
	assert_that(account.get_balance() == expected,
	            "Error: something wrong!").is_true()


@pytest.mark.parametrize("amount, expected", [
	(20.0, 80.0),
	(100.0, 0.0),
])
def test_withdraw(account, amount, expected):
	"""Test removal with parameterization"""
	account.withdraw(amount)
	assert_that(account.get_balance() == expected,
	            "Error:something wrong!").is_true()


@pytest.mark.skipif(BankAccount().get_balance() == 0.0,
                    reason="Balance is empty — withdrawal is not possible")
def test_withdraw_on_empty():
	"""Skip if balance is zero"""
	test_acc = BankAccount()
	with pytest.raises(ValueError, match="Insufficient funds"):
		test_acc.withdraw(10.0)


@patch("Lesson_08.task_06_bank_account.bank_account.BankAccount.get_balance")
def test_mocked_balance(mock_get_balance):
	"""Test case with mocking, verify balans via outside API"""
	mock_get_balance.return_value = 999.99
	test_acc = BankAccount()
	balance = test_acc.get_balance()
	assert_that(balance == 999.99,
	            "Error: unexpected result!").is_true()
	mock_get_balance.assert_called_once()
