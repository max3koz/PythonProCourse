import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class MovieDatabase:
	"""
	The class for managing the "Kinobaza" database containing information
	about movies, actors, and their relationships.
	Uses SQLite to store data.
	"""
	
	def __init__(self, db_name: str) -> None:
		"""
		The function initializes a database connection and creates tables
		if they do not exist.
			Args: db_name (str): The name of the SQLite database file.
		"""
		self.db_name: str = db_name
		self.conn: Optional[sqlite3.Connection] = None
		self.cursor: Optional[sqlite3.Cursor] = None
		self._connect()
		self._create_tables()
		self._register_custom_functions()
	
	def _connect(self) -> None:
		"""
		The function establishes a connection to the SQLite database with:
		 - foreign key checking: SQLite starts enforcing FOREIGN KEY constraints;
		 - preventing invalid inserts: For example, you can't add a record
		 to movie_cast if movie_id doesn't exist.
		"""
		try:
			self.conn = sqlite3.connect(self.db_name)
			self.cursor = self.conn.cursor()
			if self.cursor:
				self.cursor.execute("PRAGMA foreign_keys = ON;")
		except sqlite3.Error as e:
			print(f"Database connection error: {e}")
			raise ConnectionError(f"Could not connect to database: {e}")
	
	def _create_tables(self) -> None:
		"""
		The function creates the `movies, actors, and movie_cast`tables
		in the database if they do not already exist.
		"""
		if not self.cursor or not self.conn:
			raise ConnectionError("Could not connect to database to create "
			                      "tables.")
		
		self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                release_year INTEGER NOT NULL,
                genre TEXT
            );
        """)
		self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS actors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                birth_year INTEGER
            );
        """)
		# PRIMARY KEY(movie_id, actor_id), - uniqueness of the couple
		self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movie_cast (
                movie_id INTEGER,
                actor_id INTEGER,
                PRIMARY KEY (movie_id, actor_id),
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
                FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
            );
        """)
		self.conn.commit()
	
	def _register_custom_functions(self) -> None:
		"""
		The function registers SQLite custom functions, currently registers
		the 'movie_age' function.
		"""
		if self.conn:
			self.conn.create_function("movie_age", 1, self._movie_age_function)
	
	def _movie_age_function(self, release_year: int) -> int:
		"""
		The SQLite custom function to calculate the age of a movie.
		Args: release_year (int): The year the movie was released.
		Returns: int: The number of years since the movie was released
		to the current year.
		"""
		current_year = datetime.now().year
		return current_year - release_year
	
	def add_movie(self, title: str, release_year: int, genre: str,
	              actor_ids: Optional[List[int]] = None) -> Optional[int]:
		"""
		The function adds a new movie to the database.
		Args:
		 - title (str): Movie title;
		 - release_year (int): Movie release year;
		 - genre (str): Movie genre;
		 - actor_ids (Optional[List[int]]): List of actor IDs that appeared in this movie.
		Returns: Optional[int]: The ID of the added movie, or None on error.
		"""
		if not self.cursor or not self.conn:
			print("Error: Database connection not established.")
			return None
		try:
			self.cursor.execute(
				"INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
				(title, release_year, genre))
			movie_id: int = self.cursor.lastrowid
			if actor_ids:
				for actor_id in actor_ids:
					# Checking for the existence of an actor before adding it to movie_cast
					self.cursor.execute("SELECT id FROM actors WHERE id = ?",
					                    (actor_id,))
					if not self.cursor.fetchone():
						print(
							f"Warning: Actor with ID {actor_id} does not exist. "
							f"Skipping connection.")
						continue
					self.cursor.execute(
						"INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
						(movie_id, actor_id))
			self.conn.commit()
			return movie_id
		except sqlite3.Error as e:
			print(f"Error adding movie: {e}")
			self.conn.rollback()
			return None
	
	def add_actor(self, name: str, birth_year: int) -> Optional[int]:
		"""
		The function adds a new actor to the database.
		Args:
			name (str): The name of the actor.
			birth_year (int): The year of birth of the actor.
		Returns:
			Optional[int]: The ID of the added actor, or None on error.
		"""
		if not self.cursor or not self.conn:
			print("Error: Database connection not established.")
			return None
		try:
			self.cursor.execute(
				"INSERT INTO actors (name, birth_year) VALUES (?, ?)",
				(name, birth_year))
			self.conn.commit()
			return self.cursor.lastrowid
		except sqlite3.Error as e:
			print(f"Error adding actor: {e}")
			self.conn.rollback()
			return None
	
	def get_all_movies_with_actors(self) -> List[
		Tuple[str, int, str, Optional[str]]]:
		"""
		The function gets a list of all movies along with the names of the actors
		who starred in them. If the movie has no actors, the 'actors'
		field will be None.
		Returns:
			List[Tuple[str, int, str, Optional[str]]]: A list of tuples, where
			each tuple contains: movie title (str), release year (int), genre (str),
			actor's names, separated by commas (Optional[str])
		"""
		if not self.cursor:
			return []
		self.cursor.execute("""
            SELECT m.title, m.release_year, m.genre, GROUP_CONCAT(a.name, ', ')
            AS actors FROM movies m
            LEFT JOIN movie_cast mc ON m.id = mc.movie_id
            LEFT JOIN actors a ON mc.actor_id = a.id
            GROUP BY m.id, m.title, m.release_year, m.genre
            ORDER BY m.title;
        """)
		return self.cursor.fetchall()
	
	def get_unique_genres(self) -> List[str]:
		"""
		The function gets a unique list of all movie genres. Ignores empty
		or NULL genres.
		Returns: List[str]: A list of unique genres.
		"""
		if not self.cursor:
			return []
		self.cursor.execute(
			"SELECT DISTINCT genre FROM movies WHERE genre IS NOT NULL "
			"AND genre != '' ORDER BY genre;")
		return [row[0] for row in self.cursor.fetchall()]
	
	def count_movies_by_genre(self) -> List[Tuple[str, int]]:
		"""
		The function counts the number of movies for each genre. Ignores empty
		or NULL genres.
		Returns: List[Tuple[str, int]]: List of tuples (genre, number of movies).
		"""
		if not self.cursor:
			return []
		self.cursor.execute(
			"SELECT genre, COUNT(id) FROM movies WHERE genre IS NOT NULL "
			"AND genre != '' GROUP BY genre ORDER BY genre;")
		return self.cursor.fetchall()
	
	def avg_actor_birth_year_by_genre(self, genre: str) -> Optional[int]:
		"""
		The function finds the average year of birth of actors who appeared
		in movies of a certain genre.
		Args: genre (str): The genre of movies to analyze.
		Returns:
			Optional[int]: The average year of birth of the actors,
			or None if no actors for this genre were found.
		"""
		if not self.cursor:
			return None
		self.cursor.execute("""
            SELECT AVG(a.birth_year) FROM movies m
            INNER JOIN movie_cast mc ON m.id = mc.movie_id
            INNER JOIN actors a ON mc.actor_id = a.id
            WHERE m.genre = ?;""", (genre,))
		result = self.cursor.fetchone()[0]
		return int(result) if result is not None else None
	
	def search_movies_by_title(self, text: str) -> List[
		Tuple[str, int, str]]:
		"""
		The function searches for movies by keyword in the title.
		Uses LIKE operator for partial matches.
		Args: keyword (str): Keyword to search for in movie titles.
		Returns: List[Tuple[str, int, str]]: List of tuples
		(title, release year, genre) of found movies.
		"""
		if not self.cursor:
			return []
		self.cursor.execute(
			"SELECT title, release_year, genre FROM movies "
			"WHERE title LIKE ? ORDER BY title;", (f"%{text}%",))
		return self.cursor.fetchall()
	
	def get_movies_paginated(self, limit: int, offset: int) -> List[
		Tuple[str, int, str]]:
		"""
		The function gets a paginated list of movies.
		Args:
			limit (int): Maximum number of movies to display.
			offset (int): Offset from the start of the list (for pagination).
		Returns:
			List[Tuple[str, int, str]]: List of tuples (title, release year, genre)
			for the current page.
		"""
		if not self.cursor:
			return []
		self.cursor.execute(
			"SELECT title, release_year, genre FROM movies "
			"ORDER BY title LIMIT ? OFFSET ?;", (limit, offset))
		return self.cursor.fetchall()
	
	def get_total_movie_count(self) -> int:
		"""
		The function gets the total number of movies in the database.
		Returns: int: Total number of movies.
		"""
		if not self.cursor:
			return 0
		self.cursor.execute("SELECT COUNT(id) FROM movies;")
		result = self.cursor.fetchone()
		return result[0] if result else 0
	
	def get_all_actors_and_movies_union(self) -> List[Tuple[str, str]]:
		"""
		The function gets a list that combines the names of all actors and
		the names of all movies. Each element contains a name and
		a type ('actor' or 'movie').
		Returns: List[Tuple[str, str]]: A list of tuples (name, type).
		"""
		if not self.cursor:
			return []
		self.cursor.execute("""
            SELECT name AS item_name, 'actor' AS type FROM actors UNION ALL
            SELECT title AS item_name, 'movie' AS type FROM movies
            ORDER BY item_name;
        """)
		return self.cursor.fetchall()
	
	def get_movies_with_age(self) -> List[Tuple[str, int, int]]:
		"""
		The function gets a list of all movies along with their age (number
		of years since release). Uses the user-defined function `movie_age().
		Returns:
			List[Tuple[str, int, int]]: List of tuples (title, release year, movie age).
		"""
		if not self.cursor:
			return []
		self.cursor.execute(
			"SELECT title, release_year, movie_age(release_year) "
			"FROM movies ORDER BY title;")
		return self.cursor.fetchall()
	
	def get_all_actors(self) -> List[Tuple[int, str]]:
		"""
		The function gets a list of all actors with their IDs and names.
		Returns: List[Tuple[int, str]]: List of tuples (actor ID, actor name).
		"""
		if not self.cursor:
			return []
		self.cursor.execute("SELECT id, name FROM actors ORDER BY name;")
		return self.cursor.fetchall()
	
	def get_actor_by_id(self, actor_id: int) -> Optional[Tuple[int, str]]:
		"""
		Thr function gets information about an actor by its ID.
		Args: actor_id (int): The actor's ID.
		Returns: Optional[Tuple[int, str]]: A tuple (actor ID, actor name),
		or None	if the actor is not found.
		"""
		if not self.cursor:
			return None
		self.cursor.execute("SELECT id, name FROM actors WHERE id = ?",
		                    (actor_id,))
		result = self.cursor.fetchone()
		return tuple(result) if result else None  # type: ignore
	
	def close(self) -> None:
		"""
		The function closes the database connection.
		"""
		if self.conn:
			self.conn.close()
