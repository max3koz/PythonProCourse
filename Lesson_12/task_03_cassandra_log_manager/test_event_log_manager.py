from uuid import UUID


def test_create_event(manager):
	event_id = manager.create_event("user123",
	                                "login",
	                                '{"ip":"127.0.0.1"}')
	assert isinstance(event_id, UUID)


def test_get_recent_events_by_type(manager):
	manager.create_event("user123",
	                     "logout",
	                     '{"reason":"timeout"}')
	events = manager.get_recent_events_by_type("logout")
	assert any("logout" in e["event_type"] for e in events)


def test_update_metadata(manager):
	event_id = manager.create_event("user456",
	                                "purchase",
	                                '{"item":"book"}')
	manager.update_metadata(event_id, '{"item":"book","price":12.99}')
	events = manager.get_recent_events_by_type("purchase")
	updated = [e for e in events if e["event_id"] == event_id]
	assert updated[0]["metadata"] == '{"item":"book","price":12.99}'


def test_delete_old_events(manager, old_event_id):
	# Verify that the event exists
	rows = manager.session.execute("SELECT * FROM event_logs WHERE event_id=%s",
	                               (old_event_id,))
	assert any(row.event_id == old_event_id for row in rows)
	# Remove old events
	manager.delete_old_events()
	# Verify that the event removed
	rows_after = manager.session.execute(
		"SELECT * FROM event_logs WHERE event_id=%s", (old_event_id,))
	assert not any(row.event_id == old_event_id for row in rows_after)
