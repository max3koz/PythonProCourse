from datetime import datetime, timedelta
from uuid import UUID, uuid4

import pytest
from cassandra.cluster import Session

from .cassandra.config import get_session
from .event_log_manager import EventLogManager


@pytest.fixture(scope="module")
def session() -> Session:
	"""
	Initializes a Cassandra session, creates a keyspace and table
	if they do not exist.
	Returns: Session: Active Cassandra session with keyspace 'logs'.
	"""
	return get_session()


@pytest.fixture(scope="module")
def manager(session: Session) -> EventLogManager:
	"""
	Initializes an event manager that works with Cassandra.
	Args: session (Session): Cassandra session.
	Returns: EventLogManager: Manager for working with the event_logs table.
	"""
	return EventLogManager(session)


@pytest.fixture
def old_event_id(session: Session) -> UUID:
	"""
	Creates an event with an artificial date (older than 7 days) to verify deletion.
	Args: session (Session): Cassandra session.
	Returns: UUID: The identifier of the created event.
	"""
	event_id = uuid4()
	old_timestamp = datetime.utcnow() - timedelta(days=10)
	session.execute("""
        INSERT INTO event_logs (event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
    """, (event_id, "user999", "expired", old_timestamp, '{"test":"old"}'))
	return event_id
