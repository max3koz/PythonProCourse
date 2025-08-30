def training_session(rounds: int) -> None:
	time_per_round = default_time
	
	def adjust_time() -> None:
		nonlocal time_per_round
		time_per_round -= 2
	
	for round_number in range(1, rounds + 1):
		print(f"Round {round_number}: {time_per_round} minutes")
		adjust_time()


default_time = 60
training_session(10)
