import pytest

from assertpy import assert_that


class GameEventException(Exception):
	"""
	Exception class for handling game events.
	Attributes:
	event_type (str): Event type (e.g., “death,” “levelUp”).
	details (dict[str, str | int | float]): Additional information about the event.
	"""
	
	def __init__(self, event_type: str,
	             details: dict[str, str | int | float]) -> None:
		"""
		Initializes a GameEventException exception.
		Args:
			event_type (str): Event type.
			details (dict): Dictionary with event details.
		"""
		super().__init__(f"Game event occurred: {event_type}")
		self.event_type: str = event_type
		self.details: dict[str, str | int | float] = details


def simulate_game_event(event_type: str) -> None:
	"""
	Simulates a game event and throws the corresponding exception.
	Args: event_type (str): The type of event to simulate.
	Raises: GameEventException: An exception with the event details.
	"""
	if event_type == "death":
		raise GameEventException(
			event_type="death",
			details={
				"cause": "collision",
				"location": "Track_011",
				"type_cause": "car-to-car"
			}
		)
	elif event_type == "levelUp":
		raise GameEventException(
			event_type="levelUp",
			details={
				"new_level": 5,
				"place-in-rate": 12
			}
		)
	else:
		raise GameEventException(
			event_type="unknown",
			details={"message": "Unexpected exception"}
		)


@pytest.mark.parametrize("test_event, expected_result", [
	pytest.param("levelUp", "Great!! You get the new rate: 5",
	             id="Test_04_01: get 'level up' exception."),
	pytest.param("death", "Car was crashed. Issue: collision!!!",
	             id="Test_04_02: get 'death' exception."),
	pytest.param("other", "Other issue: {'message': 'Unexpected exception'}!!!",
	             id="Test_04_03: get 'other' exception.")
])
def test_get_exception(test_event, expected_result):
	event_log = ""
	try:
		simulate_game_event(test_event)
	except GameEventException as e:
		if e.event_type == "death":
			event_log = f"Car was crashed. Issue: {e.details.get('cause')}!!!"
		elif e.event_type == "levelUp":
			event_log = f"Great!! You get the new rate: {e.details.get('new_level')}"
		else:
			event_log = f"Other issue: {e.details}!!!"
	
	assert_that(event_log == expected_result,
	            f"Error: unexpected event exception: {event_log}!!!").is_true()
