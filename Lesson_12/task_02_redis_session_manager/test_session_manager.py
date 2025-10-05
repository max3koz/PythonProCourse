from time import sleep
from typing import Dict

import fakeredis
import pytest
from assertpy import assert_that

from .session_manager import SessionManager


@pytest.fixture
def session_manager() -> SessionManager:
	fake = fakeredis.FakeRedis(decode_responses=True)
	manager = SessionManager()
	manager.redis = fake  # підміна реального Redis
	return manager


def test_create_session(session_manager: SessionManager) -> None:
	session_manager.create_session("user1", "token123")
	data: Dict[str, str] = session_manager.redis.hgetall("session:user1")
	
	#Check token
	assert_that(data).contains_key("session_token")
	assert_that(data["session_token"]).is_equal_to("token123")
	
	# Check login_time
	assert_that(data).contains_key("login_time")
	assert_that(data["login_time"]).is_type_of(str)
	assert_that(data["login_time"]).matches(
		r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?")
	

def test_get_session(session_manager: SessionManager) -> None:
	session_manager.create_session("user2", "token456")
	session = session_manager.get_session("user2")
	
	#Check that session exist
	assert_that(session).is_not_none()
	
	# Verify the session token
	assert_that(session).contains_key("session_token")
	assert_that(session["session_token"]).is_equal_to("token456")


def test_update_activity(session_manager: SessionManager) -> None:
	session_manager.create_session("user3", "token789")
	
	# Decrease TTL
	session_manager.redis.expire("session:user3", 100)
	
	# Verify activity update
	ttl_before = session_manager.redis.ttl("session:user3")
	session_manager.update_activity("user3")
	ttl_after = session_manager.redis.ttl("session:user3")
	assert_that(ttl_after).is_greater_than(ttl_before)


def test_delete_session(session_manager: SessionManager) -> None:
	session_manager.create_session("user4", "token000")
	
	#Check that session exist
	assert_that(session_manager.redis.exists("session:user4")).is_true()
	
	# Check delete session
	session_manager.delete_session("user4")
	assert_that(session_manager.redis.exists("session:user4")).is_false()


def test_ttl_expiry(session_manager: SessionManager) -> None:
	# Set TTL equal to 1 sec
	session_manager.ttl_seconds = 1
	
	# Create session
	session_manager.create_session("user5", "tokenTTL")
	assert_that(session_manager.redis.exists("session:user5")).is_true()
	
	# Verify that the session was expired
	sleep(2)
	assert_that(session_manager.redis.exists("session:user5")).is_false()