import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
from typing import List


class Organism:
	"""
	The class representing an individual organism in a population.
	Attributes:
		energy (float): The current energy level of the organism.
		age (int): The age of the organism.
	"""
	
	def __init__(self, energy: float, age: int = 0) -> None:
		self.energy: float = energy
		self.age: int = age
	
	def eating(self) -> None:
		"""Simulates the process of eating by adding a random amount of energy."""
		self.energy += random.uniform(0.5, 2.0)
	
	def age_one_step(self) -> None:
		"""Increases the age of the body and reduces energy."""
		self.age += 1
		self.energy -= random.uniform(0.2, 1.0)
	
	def is_alive(self) -> bool:
		"""
		Checks if the organism is alive.
		Returns: bool: True if the organism is alive, False if not.
		"""
		return self.energy > 0 and self.age < 80
	
	def can_reproduce(self) -> bool:
		"""
		Checks if the organism can reproduce.
		Returns: bool: True if the organism has enough energy and age.
		"""
		return self.energy > 3.0 and self.age >= 18
	
	def reproduce(self) -> 'Organism':
		"""
		Creates a new organism with an energy mutation.
		Returns: Organism: A new descendant organism.
		"""
		child_energy: float = self.energy / 2
		self.energy /= 2
		mutation: float = random.uniform(-0.5, 0.5)
		mutated_energy: float = max(0.1, child_energy + mutation)
		return Organism(energy=mutated_energy)


class Event:
	"""
	Represents a cataclysm that affects a population.
	Attributes:
		name (str): Name of the event.
		impact (Callable[[Organism], Optional[Organism]]): Function of
		the impact on the organism.
		probability (float): Probability of the event being activated.
	"""
	
	def __init__(self, name: str,
	             impact: Callable[[Organism], Optional[Organism]],
	             probability: float) -> None:
		self.name = name
		self.impact = impact
		self.probability = probability
	
	def occurs(self) -> bool:
		"""
		Determines whether the event occurs.
		Returns: bool: True if the event is triggered.
		"""
		return random.random() < self.probability


def disaster_impact(organism_item: Organism) -> Optional[Organism]:
	"""Impact of the Natural Disaster: 70% energy reduction."""
	organism_item.energy *= 0.3
	return organism_item if organism_item.is_alive() else None


def epidemic_impact(organism_item: Organism) -> Optional[Organism]:
	"""Impact of the Epidemic: Decreased energy and chance of death."""
	organism_item.energy -= random.uniform(1.0, 5.0)
	return organism_item if organism_item.is_alive() else None


def apply_event(population: List[Organism], event: Event) -> List[Organism]:
	"""
	Applies an event to a population.
	Args:
		population (List[Organism]): The current population.
		event (Event): The event to apply.
	Returns:
		List[Organism]: The new population after the event.
	"""
	print(f"Cataclysm: {event.name}!")
	new_population: List[Organism] = []
	for organism_item in population:
		affected = event.impact(organism_item)
		if affected:
			new_population.append(affected)
	return new_population


def process_organism(organism_item: Organism) -> List[Organism]:
	"""
	Processes a single organism: nutrition, aging, checking for reproduction.
	Args: organism_item (Organism): The organism to process.
	Returns: List[Organism]: A list of living organisms (including descendants).
	"""
	organism_item.eating()
	organism_item.age_one_step()
	offspring: List[Organism] = []
	if organism_item.can_reproduce():
		offspring.append(organism_item.reproduce())
	return [organism_item] + offspring if organism_item.is_alive() else []


def simulate_generation(population: List[Organism]) -> List[Organism]:
	"""
	Simulates one generation of a population with parallel processing of organisms.
	Args: population (List[Organism]): Current population.
	Returns: List[Organism]: New population after simulation.
	"""
	new_population: List[Organism] = []
	with ThreadPoolExecutor() as executor:
		results = executor.map(process_organism, population)
		for result in results:
			new_population.extend(result)
	return new_population


def run_simulation(initial_size: int, generations: int) -> None:
	"""
	Runs a population evolution simulation.
	Args:
		initial_size (int): Initial population size.
		generations (int): Number of generations to simulate.
	"""
	events: List[Event] = [
		Event("Natural Disaster", disaster_impact, probability=0.15),
		Event("Epidemic", epidemic_impact, probability=0.4),
	]
	
	population: List[Organism] = [Organism(energy=random.uniform(1.0, 5.0))
	                              for _ in range(initial_size)]
	
	for event in events:
		if event.occurs():
			population = apply_event(population, event)
	
	population_sizes: List[int] = []
	
	for gen in range(generations):
		print(f"Generation {gen + 1}: Population size = {len(population)}")
		population_sizes.append(len(population))
		population = simulate_generation(population)
		time.sleep(0.2)


def generate_population(size: int, energy_range: tuple[float, float]) -> List[
	Organism]:
	"""
	Generates an initial population with a given energy range.
	Args:
		size (int): Number of organisms.
		energy_range (tuple[float, float]): Minimum and maximum energy.
	Returns:
		List[Organism]: List of organisms.
	"""
	return [Organism(energy=random.uniform(*energy_range)) for _ in range(size)]


initial_population = generate_population(size=10, energy_range=(2.0, 10.0))
run_simulation(initial_size=len(initial_population), generations=100)
