def training_session(rounds: int) -> None:
	"""
	A function that takes the number of training rounds.
	- uses the time_per_round variable, which is responsible for the time
	per round, and changes it locally for each training;
    - a nested function adjust_time, which allows you to adjust the time
    for each individual round (through the implicit use of nonlocal)
	"""
	time_per_round = default_time
	
	def adjust_time() -> None:
		"""
		The function which allows you to adjust the time for each individual round
		"""
		nonlocal time_per_round
		time_per_round -= 2
	
	for round_number in range(1, rounds + 1):
		print(f"Round {round_number}: {time_per_round} minutes")
		adjust_time()


default_time = 60
training_session(10)
