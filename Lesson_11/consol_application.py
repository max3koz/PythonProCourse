import os
from datetime import datetime
from typing import List, Optional, Tuple

from rich.console import Console
from rich.table import Table

from database import MovieDatabase


def display_menu() -> None:
	"""
	Displays the menu of the "Kinobase" console application.
	"""
	console = Console()
	
	table = Table(title="Menu of the \"Kinobase\" application")
	table.add_column("Number")
	table.add_column("Action")
	
	table.add_row("1", "Enter movie data")
	table.add_row("2", "Enter the the actor/actress data")
	table.add_row("3", "Show all movies with actors")
	table.add_row("4", "Show unique genres")
	table.add_row("5", "Show number of movies by genre")
	table.add_row("6", "Show the ave.year of birth of actors in movies "
	                   "of a specific genre")
	table.add_row("7", "Search for a movie by title")
	table.add_row("8", "Show movies (with pagination)")
	table.add_row("9", "Show all actor's names and all movie titles")
	table.add_row("10", "Show movies and their age")
	table.add_row("0", "Quit the app")
	
	console.print(table)


def clear_screen() -> None:
	"""
	The function clears the console screen.
	Works for both Windows ('cls') and Unix-like ('clear').
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


def validate_year(prompt: str, min_year: int, max_year: int) -> int:
	"""
	The function prompts the user for a year and validates it within the specified range.
	Args:
		prompt (str): The message to display to the user.
		min_year (int): The minimum allowed year.
		max_year (int): The maximum allowed year.
	Returns: int: The valid year entered by the user.
	"""
	while True:
		try:
			year_input = input(prompt)
			year = int(year_input)
			if min_year <= year <= max_year:
				return year
			else:
				print(f"The year must be between {min_year} and {max_year}. "
				      f"Please try again.")
		except ValueError:
			print("Invalid format. Please enter a whole number.")


def app() -> None:
	"""The main function that launches the "Kinobase" console application"""
	db = MovieDatabase("kinobaza.db")
	
	while True:
		display_menu()
		choice: str = input("Enter the number of the action: ").strip()
		clear_screen()
		
		if choice == '1':
			print("--- Enter movie data ---")
			title: str = input("Enter the movie title: ").strip()
			release_year: int = validate_year("Enter the year of release: ",
			                                  1800, datetime.now().year)
			genre: str = input("Enter the genre: ").strip()
			
			actors_data: List[Tuple[int, str]] = db.get_all_actors()
			actor_ids: List[int] = []
			if actors_data:
				print("\nAvailable actors:")
				for actor_id, actor_name in actors_data:
					print(f"{actor_id}. {actor_name}")
				actor_ids_input: str = input("Enter actor IDs separated "
				                             "by commas (e.g. 1,3,5), "
				                             "or leave blank: ").strip()
				if actor_ids_input:
					try:
						potential_actor_ids: List[int] = [int(id_num.strip())
						                                  for id_num in
						                                  actor_ids_input.split(
							                                  ',') if
						                                  id_num.strip()]
						for actual_id in potential_actor_ids:
							if db.get_actor_by_id(actual_id):
								actor_ids.append(actual_id)
							else:
								print(f"Warning: Actor with ID {actual_id} "
								      f"was not found and will not be added "
								      f"to the movie.")
					except ValueError:
						print("Invalid actor ID format. Please enter numbers "
						      "separated by commas.")
			else:
				print("There are currently no actors added. To add actors "
				      "to your movie, first add them.")
			
			movie_id: Optional[int] = db.add_movie(title, release_year, genre,
			                                       actor_ids)
			if movie_id:
				print(f"Movie '{title}' successfully added (ID: {movie_id}).")
			else:
				print(f"Error adding movie '{title}'.")
		
		elif choice == '2':
			print("--- Enter the the actor/actress data ---")
			name: str = input("Enter the actor's name: ").strip()
			birth_year: int = validate_year("Enter actor's year of birth: ",
			                                1900, datetime.now().year)
			actor_id: Optional[int] = db.add_actor(name, birth_year)
			if actor_id:
				print(f"Actor '{name}' successfully added (ID: {actor_id}).")
			else:
				print(f"Error adding actor's data '{name}'.")
		
		elif choice == '3':
			print("--- Show all movies with actors ---")
			movies_with_actors: List[Tuple[
				str, int, str, Optional[str]]] = db.get_all_movies_with_actors()
			if movies_with_actors:
				for num, (title, year, genre, actors) in enumerate(
						movies_with_actors, 1):
					actors_str: str = actors if actors else "No actors"
					print(f"{num}. Movie: \"{title}\" ({year}, {genre}), "
					      f"Actors: {actors_str}")
			else:
				print("No movies found.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '4':
			print("--- Show unique genres ---")
			genres: List[str] = db.get_unique_genres()
			if genres:
				for i, genre in enumerate(genres, 1):
					print(f"{i}. {genre}")
			else:
				print("No genres found.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '5':
			print("--- Show number of movies by genre ---")
			genre_counts: List[Tuple[str, int]] = db.count_movies_by_genre()
			if genre_counts:
				for genre, count in genre_counts:
					print(f"{genre}: {count} movies")
			else:
				print("No movies found.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '6':
			genre_input: str = input("Enter a genre to find the average year "
			                         "of birth of actors: ").strip()
			avg_year: Optional[int] = db.avg_actor_birth_year_by_genre(
				genre_input)
			if avg_year is not None:
				print(f"Average year of birth of actors in genre movies '"
				      f"{genre_input}': {avg_year} рік.")
			else:
				print(f"No actors found in movies of genre '{genre_input}' "
				      f"or genre does not exist.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '7':
			print("--- Search for a movie by title  ---")
			keyword: str = input(
				"Enter a keyword to search for a movie: ").strip()
			found_movies: List[
				Tuple[str, int, str]] = db.search_movies_by_title(keyword)
			if found_movies:
				print("\n--- Found movies ---")
				for i, (title, release_year, genre) in enumerate(found_movies,
				                                                 1):
					print(f"{i}. {title} ({release_year}, {genre})")
			else:
				print(f"No movies found for keyword '{keyword}'.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '8':
			print("--- Show movies (with pagination)  ---")
			page_size: int = 5
			total_movies: int = db.get_total_movie_count()
			if total_movies == 0:
				print("No movies found.")
				input("\nPress Enter to return to the main menu...")
				continue
			
			total_pages: int = (total_movies + page_size - 1) // page_size
			current_page: int = 1
			
			while True:
				offset: int = (current_page - 1) * page_size
				movies_paginated: List[
					Tuple[str, int, str]] = db.get_movies_paginated(page_size,
				                                                    offset)
				clear_screen()
				print(
					f"\n--- Page {current_page} from {total_pages} pages ---")
				for item, (title, release_year, genre) in enumerate(
						movies_paginated, 1):
					print(f"{offset + item}. {title} ({release_year}, {genre})")
				
				if total_pages > 1:
					print(
						"\n[<] Previous page | [>] Next page | [m] Main menu")
					nav_choice: str = input("Your choice: ").lower().strip()
					if nav_choice == '<':
						current_page = max(1, current_page - 1)
					elif nav_choice == '>':
						current_page = min(total_pages, current_page + 1)
					elif nav_choice == 'm':
						break
					else:
						print("Incorrect navigation choice.")
						input("\nНPress Enter to continue....")
				else:
					input("\nPress Enter to return to the main menu....")
					break
		
		elif choice == '9':
			print("--- Show all actor's names and all movie titles ---")
			union_results: List[
				Tuple[str, str]] = db.get_all_actors_and_movies_union()
			if union_results:
				for item, (item_name, item_type) in enumerate(union_results, 1):
					print(f"{item}. {item_name} ({item_type})")
			else:
				print("No data found.")
			input("\nPress Enter to return to the main menu...")
		
		elif choice == '10':
			print("--- Show movies and their age ---")
			movies_with_age: List[
				Tuple[str, int, int]] = db.get_movies_with_age()
			if movies_with_age:
				for item, (title, release_year, age) \
						in enumerate(movies_with_age, 1):
					print(f"{item}. Movie: \"{title}\" — {age} years old "
					      f"(released in {release_year})")
			else:
				print("No movies found.")
			input("\nPress Enter to return to the main menu....")
		
		elif choice == '0':
			print("Exit from the program...")
			db.close()
			break
		else:
			print("Press Enter to continue...")
			input("\nНатисніть Enter, щоб продовжити...")


if __name__ == "__main__":
	os.environ["TERM"] = "xterm"
	app()
