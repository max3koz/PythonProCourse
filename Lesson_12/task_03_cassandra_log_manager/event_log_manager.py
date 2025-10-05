from datetime import datetime, timedelta
from typing import List, Dict
from uuid import UUID, uuid4

from cassandra.cluster import Session


class EventLogManager:
	"""
	The class for managing event logs in Cassandra.
	"""
	
	def __init__(self, session: Session) -> None:
		self.session = session
	
	def create_event(self, user_id: str, event_type: str,
	                 metadata: str) -> UUID:
		"""
		Creates a new event in the event_logs table.
		Args:
			user_id (str): User ID.
			event_type (str): Event type (e.g. 'login', 'purchase').
			metadata (str): JSON string with additional data.
		Returns: UUID: The identifier of the created event.
		"""
		event_id = uuid4()
		timestamp = datetime.utcnow()
		query = """
        INSERT INTO event_logs (event_id, user_id, event_type, timestamp, metadata)
        VALUES (%s, %s, %s, %s, %s)
        """
		self.session.execute(query, (event_id, user_id, event_type, timestamp,
		                             metadata))
		return event_id
	
	def get_recent_events_by_type(self, event_type: str) -> List[
		Dict[str, str]]:
		"""
		The function returns a list of events of a specific type created
		in the last 24 hours.
		Args: event_type (str): The type of event to filter.
		Returns: List[Dict[str, str]]: A list of events as dictionaries.
		"""
		cutoff = datetime.utcnow() - timedelta(days=1)
		query = """
        SELECT * FROM event_logs WHERE event_type=%s AND timestamp >= %s ALLOW FILTERING
        """
		rows = self.session.execute(query, (event_type, cutoff))
		return [dict(row._asdict()) for row in rows]
	
	def update_metadata(self, event_id: UUID, new_metadata: str) -> None:
		query = """
        UPDATE event_logs SET metadata=%s WHERE event_id=%s
        """
		self.session.execute(query, (new_metadata, event_id))
	
	def delete_old_events(self) -> None:
		"""
		The function updates the metadata field for the given event.
		Args:
			event_id (UUID): Event identifier.
			new_metadata (str): New JSON string with metadata.
		"""
		cutoff = datetime.utcnow() - timedelta(days=7)
		query = """
        SELECT event_id FROM event_logs WHERE timestamp < %s ALLOW FILTERING
        """
		rows = self.session.execute(query, (cutoff,))
		for row in rows:
			self.session.execute("DELETE FROM event_logs WHERE event_id=%s",
			                     (row.event_id,))
