from datetime import datetime
from typing import Optional, Dict

import redis


class SessionManager:
	"""
	The class for managing user sessions in Redis.
	Stores 'user_id', 'session_token', 'login_time'.
	"""
	
	def __init__(self, host: str = "localhost", port: int = 6379,
	             db: int = 0) -> None:
		"""
		Initializes the connection to Redis and ttl life time.
		Param:
		  - host: Redis-server host
		  - port: Redis-server port
		  - db: Redis database number
		"""
		self.redis = redis.Redis(host=host, port=port, db=db,
		                         decode_responses=True)
		self.ttl_seconds = 1800
	
	def create_session(self, user_id: str, session_token: str) -> None:
		"""
		The function creates a new session for the user.
		Param:
			- user_id: User ID
			- session_token: Unique session token
		"""
		key = f"session:{user_id}"
		self.redis.hmset(key, {
			"session_token": session_token,
			"login_time": datetime.utcnow().isoformat()
		})
		self.redis.expire(key, self.ttl_seconds)
	
	def get_session(self, user_id: str) -> Optional[Dict[str, str]]:
		"""
		Gets the active user session.
		Param: user_id: User ID
		Return: Session data or None
		"""
		key = f"session:{user_id}"
		if self.redis.exists(key):
			session = self.redis.hgetall(key)
			try:
				dt = datetime.fromisoformat(session["login_time"])
				session["login_time"] = dt.strftime("%d-%m-%Y %H:%M:%S")
			except Exception:
				pass  # leave as is if the format is not ISO
			return session
		return None

	def update_activity(self, user_id: str) -> None:
		"""
		Updates the user's last activity time (restarts TTL).
		Paaram: user_id: User ID
		"""
		key = f"session:{user_id}"
		if self.redis.exists(key):
			self.redis.hset(key, "login_time", datetime.utcnow().isoformat())
			self.redis.expire(key, self.ttl_seconds)


	def delete_session(self, user_id: str) -> None:
		"""
		Deletes the user session.
		Param: user_id: User ID
		"""
		key = f"session:{user_id}"
		self.redis.delete(key)
		