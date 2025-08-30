def event_calendar() -> tuple:
	global events
	
	def add_event(event: str) -> None:
		events.append(event)
		print(f"Added event: {event}.")
	
	def remove_event(event: str) -> None:
		if event in events:
			events.remove(event)
			print(f"Event deleted: {event}.")
		else:
			print(f"Event {event} did not find.")
	
	def view_events() -> None:
		if events:
			print("Exist event:")
			for event_item in events:
				print(f"   - {event_item}")
		else:
			print("The list og event is empty!!!")
	
	return add_event, remove_event, view_events


events = []
add_calendar_item, remove_calendar_item, events_list = event_calendar()

events_list()
add_calendar_item("Meeting 1")
add_calendar_item("Meeting 2")
events_list()
remove_calendar_item("Meeting 2")
events_list()
