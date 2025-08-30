def subscribe(name: str) -> None:
	global subscribers
	subscribers.append(name)
	
	def confirm_subscription() -> str:
		return f"Subscription confirmed for {name}"
	
	print(confirm_subscription())


def unsubscribe(name: str) -> str:
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
