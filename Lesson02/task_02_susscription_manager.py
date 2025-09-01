def subscribe(name: str) -> None:
	"""
	The function takes the subscriber's name as an argument and adds it to
	the subscriber list.
	"""
	global subscribers
	subscribers.append(name)
	
	def confirm_subscription() -> str:
		"""
		Function that returns the message: "Subscription confirmed for <name>"
		"""
		return f"Subscription confirmed for {name}"
	
	print(confirm_subscription())


def unsubscribe(name: str) -> str:
	"""
	 The function that takes a name and removes it from the subscriber list.
	"""
	global subscribers
	if name in subscribers:
		subscribers.remove(name)
		return f"{name} unsubscribed successfully!!!"
	return f"{name} doesn't find in the subscribers list!!!"


subscribers = []
subscribe("Maksym")
subscribe("Oksana")
print(subscribers)
print(unsubscribe("Jeff"))
print(subscribers)
print(unsubscribe("Maksym"))
print(subscribers)
subscribe("Olesja")
print(subscribers)
