import pytest

from assertpy import assert_that


class InsufficientResourcesException(Exception):
	"""
	The exception that signals insufficient resources to perform an action.
	Attributes:
		required_resource (str): Name of the missing resource.
		required_amount (int | float): Required amount of the resource.
		current_amount (int | float): Current amount of the resource the player
		has.
	"""
	
	def __init__(
			self,
			required_resource: str,
			required_amount: int | float,
			current_amount: int | float
	) -> None:
		"""
		Initializes an InsufficientResourcesException exception.
		Args:
			required_resource (str): Resource name.
			required_amount (int | float): Required amount.
			current_amount (int | float): Available amount.
		"""
		super().__init__(f"Not enough resource: {required_resource}")
		self.required_resource: str = required_resource
		self.required_amount: int | float = required_amount
		self.current_amount: int | float = current_amount


def perform_action(resource_name: str, required: int | float,
                   available: int | float) -> str:
	"""
	Verify that the availability of a resource and either performs an action
	or throws an exception.
	Args:
		resource_name (str): Name of the resource.
		required (int | float): Required quantity.
		available (int | float): Available quantity.
	Raises:
		InsufficientResourcesException: If there are insufficient resources.
	"""
	if available < required:
		raise InsufficientResourcesException(resource_name, required, available)
	
	action_log = (f"Action completed! {required} units of the resource "
	              f"‘{resource_name}’ were used.")
	return action_log


@pytest.mark.parametrize("test_resource_name, test_required_value, "
                         "test_actual_value, expected_result", [
	pytest.param("petrol", 20, 20,
	             "Action completed! 20 units of the resource ‘petrol’ were used.",
	             id="TC_04_04: positive test_case"),
	pytest.param("petrol", 21, 20,
	             "Error not enough resource 'petrol'!!! Need: 21, exist: 20.",
	             id="TC_04_05: negative testcase.")
])
def test_insufficient_resource(test_resource_name, test_required_value,
                               test_actual_value, expected_result):
	try:
		action_resource_log = perform_action(test_resource_name,
		                                     required=test_required_value,
		                                     available=test_actual_value)
	except InsufficientResourcesException as e:
		action_resource_log = (
			f"Error not enough resource '{e.required_resource}'!!! "
			f"Need: {e.required_amount}, exist: {e.current_amount}."
		)
	
	assert_that(action_resource_log == expected_result,
	            f"Error: expected result: {expected_result}, "
	            f"actual result: {action_resource_log}").is_true()
