from cassandra.cluster import Cluster


def get_session(keyspace: str = "logs"):
	cluster = Cluster(['127.0.0.1'], port=9042)
	session = cluster.connect()
	session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};
    """)
	session.set_keyspace(keyspace)
	session.execute("""
        CREATE TABLE IF NOT EXISTS event_logs (
            event_id UUID PRIMARY KEY,
            user_id TEXT,
            event_type TEXT,
            timestamp TIMESTAMP,
            metadata TEXT
        );
    """)
	return session
