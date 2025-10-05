CREATE KEYSPACE IF NOT EXISTS logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE logs;

CREATE TABLE IF NOT EXISTS event_logs (
    event_id UUID PRIMARY KEY,
    user_id TEXT,
    event_type TEXT,
    timestamp TIMESTAMP,
    metadata TEXT
);