import pytest

from .user_manager import UserManager


@pytest.fixture
def user_manager():
	um = UserManager()
	um.add_user("Sashko", 30)
	um.add_user("Mark", 25)
	return um


def test_add_user(user_manager):
	user_manager.add_user("Petro", 40)
	users = user_manager.get_all_users()
	assert ("Petro", 40) in users
	assert len(users) == 3


def test_remove_user(user_manager):
	user_manager.remove_user("Mark")
	users = user_manager.get_all_users()
	assert ("Mark", 30) not in users
	assert len(users) == 1


def test_get_all_users(user_manager):
	users = user_manager.get_all_users()
	assert ("Sashko", 30) in users
	assert ("Mark", 25) in users
	assert len(users) == 2


def test_skip_if_less_than_three(user_manager):
	um = UserManager()
	um.add_user("User_1", 1)
	um.add_user("User_2", 2)
	
	if len(um.get_all_users()) < 3:
		pytest.skip("Fewer than three users — test skipped")
		assert len(um.get_all_users()) >= 3
