from typing import Any


def email_sender(data: Any) -> None:
	"""Send an email when a user registers."""
	print(f"[EMAIL] Sending welcome email to {data}")


def logger(data: Any) -> None:
	"""Log event data."""
	print(f"[LOGGER] Event logged: {data}")


def analytics(data: Any) -> None:
	"""Track analytics for events."""
	print(f"[ANALYTICS] Tracking event: {data}")
