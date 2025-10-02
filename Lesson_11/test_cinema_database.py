from datetime import datetime
from typing import Generator, Tuple, List, Optional

import pytest
from assertpy import assert_that

from .database import MovieDatabase


@pytest.fixture
def db() -> Generator[MovieDatabase, None, None]:
	"""
	Pytest fixture to create a temporary in-memory database for each test.
	"""
	test_db = MovieDatabase(db_name=":memory:")
	yield test_db
	test_db.close()


def test_db_connection_and_table_creation(db: MovieDatabase) -> None:
	"""
	Checks the success of connecting to the database and creating
	all necessary tables.
	"""
	assert_that(db.conn).is_not_none()
	assert_that(db.cursor).is_not_none()
	
	if db.cursor:
		db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
		tables: List[str] = [row[0] for row in db.cursor.fetchall()]
		assert_that(tables, f"Error: unexpected result {tables}").contains(
			'movies')
		assert_that(tables, f"Error: unexpected result {tables}").contains(
			'actors')
		assert_that(tables, f"Error: unexpected result {tables}").contains(
			'movie_cast')


def test_add_actor(db: MovieDatabase) -> None:
	"""
	Tests adding a new actor to the database.
	Verifies that the actor is added and its data is stored correctly.
	"""
	actor_id: Optional[int] = db.add_actor("Tom Hanks", 1956)
	assert_that(actor_id, f"Error: unexpected result {actor_id}").is_not_none()
	assert_that(actor_id,
	            f"Error: unexpected result {actor_id}").is_instance_of(int)
	
	if db.cursor:
		db.cursor.execute("SELECT id, name, birth_year FROM actors "
		                  "WHERE id = ?", (actor_id,))
		actor: Optional[Tuple[int, str, int]] = db.cursor.fetchone()
		assert_that(actor == (actor_id, "Tom Hanks", 1956),
		            f"Error: unexpected result {actor}").is_true()


def test_add_movie_without_actors(db: MovieDatabase) -> None:
	"""
	Tests adding a movie without actors.
	Checks that the movie is added and its data is saved correctly.
	"""
	movie_id: Optional[int] = db.add_movie("Forrest Gump", 1994,
	                                       "Drama")
	assert_that(movie_id, f"Error: unexpected result {movie_id}").is_not_none()
	assert_that(movie_id,
	            f"Error: unexpected result {movie_id}").is_instance_of(int)
	
	if db.cursor:
		db.cursor.execute(
			"SELECT id, title, release_year, genre FROM movies WHERE id = ?",
			(movie_id,))
		movie: Optional[Tuple[int, str, int, str]] = db.cursor.fetchone()
		assert_that(movie == (movie_id, "Forrest Gump", 1994, "Drama"),
		            f"Error: unexpected result {movie}").is_true()


def test_add_movie_with_actors(db: MovieDatabase) -> None:
	"""
	Tests adding a movie with actors.
	Checks that the movie and actor connections are added correctly.
	"""
	actor1_id: Optional[int] = db.add_actor("Tom Hanks", 1956)
	actor2_id: Optional[int] = db.add_actor("Robin Wright", 1966)
	assert_that(actor1_id,
	            f"Error: unexpected result {actor1_id}").is_not_none()
	assert_that(actor2_id,
	            f"Error: unexpected result {actor2_id}").is_not_none()
	
	movie_id: Optional[int] = db.add_movie("Forrest Gump", 1994,
	                                       "Drama", [actor1_id, actor2_id])
	assert_that(movie_id, f"Error: unexpected result {movie_id}").is_not_none()
	
	if db.cursor:
		db.cursor.execute(
			"SELECT movie_id, actor_id FROM movie_cast WHERE movie_id = ?",
			(movie_id,))
	movie_list: List[Tuple[int, int]] = db.cursor.fetchall()
	assert_that(len(movie_list) == 2, f"Error: unexpected result "
	                                  f"{len(movie_list)}").is_true()
	assert_that(movie_list, f"Error: unexpected result {movie_list}").contains(
		(movie_id, actor1_id))
	assert_that(movie_list, f"Error: unexpected result {movie_list}").contains(
		(movie_id, actor2_id))


def test_add_movie_with_invalid_actor_id(db: MovieDatabase) -> None:
	"""
	Tests adding a movie with a combination of valid and invalid actor IDs.
	Checks that only valid actor relationships are added.
	"""
	actor_id: Optional[int] = db.add_actor("John Doe", 1980)
	assert_that(actor_id, f"Error: unexpected result {actor_id}").is_not_none()
	
	movie_id: Optional[int] = db.add_movie("Test film", 2000,
	                                       "Fantasy", [actor_id, 99999])
	assert_that(movie_id, f"Error: unexpected result {movie_id}").is_not_none()
	
	if db.cursor:
		db.cursor.execute(
			"SELECT movie_id, actor_id FROM movie_cast WHERE movie_id = ?",
			(movie_id,))
		movie_list: List[Tuple[int, int]] = db.cursor.fetchall()
		assert_that(len(movie_list) == 1,
		            f"Error: unexpected result {len(movie_list)}").is_true()
		assert_that(movie_list,
		            f"Error: unexpected result {movie_list}").contains(
			(movie_id, actor_id))


def test_get_all_movies_with_actors(db: MovieDatabase) -> None:
	"""
	Tests getting a list of all movies with actors.
	Checks the correctness of data merging and actor formatting.
	"""
	actor1_id: Optional[int] = db.add_actor("Tom Henks", 1956)
	actor2_id: Optional[int] = db.add_actor("Robin Wright", 1966)
	actor3_id: Optional[int] = db.add_actor("Matthew McConaughey", 1969)
	assert_that(actor1_id,
	            f"Error: unexpected result {actor1_id}").is_not_none()
	assert_that(actor2_id,
	            f"Error: unexpected result {actor2_id}").is_not_none()
	assert_that(actor3_id,
	            f"Error: unexpected result {actor1_id}").is_not_none()
	
	db.add_movie("Forrest Gump", 1994, "Drama", [actor1_id, actor2_id])
	db.add_movie("Interstellar", 2014, "Science fiction", [actor3_id])
	db.add_movie("Another Movie", 2020, "Comedy")
	
	movies_data: List[
		Tuple[str, int, str, Optional[str]]] = db.get_all_movies_with_actors()
	assert_that(len(movies_data) == 3,
	            f"Error: unexpected result {len(movies_data)}").is_true()
	
	expected_titles: List[str] = ['Another Movie', 'Forrest Gump',
	                              'Interstellar']
	actual_titles: List[str] = [item[0] for item in movies_data]
	assert_that(actual_titles == expected_titles).is_true()
	
	assert_that(any(item[0] == "Forrest Gump" and item[3]
	                in {"Robin Wright, Tom Henks", "Tom Henks, Robin Wright"}
	                for item in movies_data)).is_true()
	assert_that(movies_data).contains(
		("Interstellar", 2014, "Science fiction", "Matthew McConaughey"))
	assert_that(movies_data).contains(("Another Movie", 2020, "Comedy", None))


def test_get_unique_genres(db: MovieDatabase) -> None:
	"""
	Tests getting a list of unique genres.
	Checks that empty or NULL genres are ignored
	"""
	db.add_movie("Forrest Gump", 1994, "Drama")
	db.add_movie("Interstellar", 2014, "Science Fiction")
	db.add_movie("Titanic", 1997, "Drama")
	db.add_movie("Avatar", 2009, "Science Fiction")
	db.add_movie("Empty Genre", 2020, "")
	db.add_movie("Null Genre", 2021, None)
	
	genres: List[str] = db.get_unique_genres()
	assert_that(sorted(genres) == ["Drama", "Science Fiction"]).is_true()


def test_count_movies_by_genre(db: MovieDatabase) -> None:
	"""
	Тестує підрахунок кількості фільмів для кожного жанру.
	Перевіряє коректність агрегатних функцій.
	"""
	db.add_movie("Forrest Gump", 1994, "Drama")
	db.add_movie("Interstellar", 2014, "Science Fiction")
	db.add_movie("Titanic", 1997, "Drama")
	db.add_movie("Avatar", 2009, "Science Fiction")
	db.add_movie("The One", 2020, "Comedy")
	db.add_movie("No Genre", 2020, "")
	db.add_movie("Null Genre", 2021, None)
	
	genre_counts: List[Tuple[str, int]] = db.count_movies_by_genre()
	expected_counts: List[Tuple[str, int]] = [("Drama", 2), ("Comedy", 1),
	                                          ("Science Fiction", 2)]
	assert_that(sorted(genre_counts) == sorted(expected_counts)).is_true()


def test_avg_actor_birth_year_by_genre(db: MovieDatabase) -> None:
	"""
	Тестує обчислення середнього року народження акторів у фільмах певного жанру.
	"""
	actor1_id: Optional[int] = db.add_actor("Actor A", 1970)
	actor2_id: Optional[int] = db.add_actor("Actor B", 1980)
	actor3_id: Optional[int] = db.add_actor("Actor C", 1990)
	assert_that(actor1_id,
	            f"Error: unexpected result {actor1_id}").is_not_none()
	assert_that(actor2_id,
	            f"Error: unexpected result {actor2_id}").is_not_none()
	assert_that(actor3_id,
	            f"Error: unexpected result {actor1_id}").is_not_none()
	
	db.add_movie("Movie 1", 2000, "Drama", [actor1_id, actor2_id])
	db.add_movie("Movie 2", 2005, "Comedy", [actor3_id])
	db.add_movie("Movie 3", 2010, "Drama", [actor3_id])
	
	avg_drama: Optional[int] = db.avg_actor_birth_year_by_genre("Drama")
	avg_comedy: Optional[int] = db.avg_actor_birth_year_by_genre("Comedy")
	avg_fantasy: Optional[int] = db.avg_actor_birth_year_by_genre("Fantasy")
	
	assert_that(avg_drama == 1980,
	            f"Error: unexpected result {avg_drama}").is_true()
	assert_that(avg_comedy == 1990,
	            f"Error: unexpected result {avg_comedy}").is_true()
	assert_that(avg_fantasy,
	            f"Error: unexpected result {avg_fantasy}").is_none()


def test_search_movies_by_title(db: MovieDatabase) -> None:
	"""
	Tests searching for movies by keyword in the title.
	Tests the LIKE operator.
	"""
	db.add_movie("Movie 4", 2014, "Fantasy")
	db.add_movie("Movie 3", 2010, "Fantasy")
	db.add_movie("Movie 2", 1999, "Fantasy")
	db.add_movie("Film 1", 2020, "Drama")
	
	results_int: List[Tuple[str, int, str]] = db.search_movies_by_title(
		"Movie 4")
	assert_that(len(results_int) == 1).is_true()
	assert_that([("Movie 4", 2014, "Fantasy")] == results_int,
	            f"Error: unexpected result {results_int}").is_true()
	
	results: List[Tuple[str, int, str]] = db.search_movies_by_title(
		"Movie ")
	assert_that(len(results) == 3).is_true()
	assert_that([('Movie 2', 1999, 'Fantasy'), ('Movie 3', 2010, 'Fantasy'),
	             ('Movie 4', 2014, 'Fantasy')] == results,
	            f"Error: unexpected result {results}").is_true()
	
	results_none: List[Tuple[str, int, str]] = db.search_movies_by_title(
		"None movie")
	assert_that(len(results_none) == 0).is_true()


def test_get_movies_paginated(db: MovieDatabase) -> None:
	"""
	Tests movie pagination using LIMIT and OFFSET.
	"""
	for i in range(1, 9):
		db.add_movie(f"Movie {i}", 2000 + i, "Drama")
	
	page1: List[Tuple[str, int, str]] = db.get_movies_paginated(3, 0)
	assert_that(len(page1) == 3).is_true()
	assert_that(page1[0][0],
	            f"Error: unexpected result {page1[0][0]}").is_equal_to(
		"Movie 1"),
	assert_that(page1[2][0],
	            f"Error: unexpected result {page1[2][0]}").is_equal_to(
		"Movie 3"),
	
	page2: List[Tuple[str, int, str]] = db.get_movies_paginated(3, 3)
	assert_that(len(page2) == 3).is_true()
	assert_that(page2[0][0],
	            f"Error: unexpected result {page2[0][0]}").is_equal_to(
		"Movie 4"),
	assert_that(page2[2][0],
	            f"Error: unexpected result {page2[2][0]}").is_equal_to(
		"Movie 6"),
	
	page_last: List[Tuple[str, int, str]] = db.get_movies_paginated(3, 6)
	assert_that(len(page_last) == 2,
	            f"Error: unexpected result {len(page_last)}").is_true()
	assert_that(page_last[0][0],
	            f"Error: unexpected result {page2[0][0]}").is_equal_to(
		"Movie 7"),


def test_get_total_movie_count(db: MovieDatabase) -> None:
	"""Tests getting the total number of movies."""
	assert_that(db.get_total_movie_count() == 0,
	            f"Error: unexpected result {db.get_total_movie_count()}").is_true()
	db.add_movie("Movie 1", 2000, "Drama")
	assert_that(db.get_total_movie_count() == 1,
	            f"Error: unexpected result {db.get_total_movie_count()}").is_true()
	db.add_movie("Movie 2", 2001, "Drama")
	db.add_movie("Movie 3", 2002, "Drama")
	assert_that(db.get_total_movie_count() == 3,
	            f"Error: unexpected result {db.get_total_movie_count()}").is_true()


def test_get_all_actors_and_movies_union(db: MovieDatabase) -> None:
	"""
	Tests the union of actor names and movie titles using UNION ALL.
	Checks the correctness of the results and sorting.
	"""
	db.add_actor("Actor 1", 1962)
	db.add_actor("Actor 2", 1969)
	db.add_movie("Movie 1", 1986, "Drama")
	db.add_movie("Movie 2", 2021, "Comedy")
	db.add_actor("3 Actor", 1956)
	db.add_movie("3 Movie", 2009, "Drama")
	
	results: List[Tuple[str, str]] = db.get_all_actors_and_movies_union()
	
	expected_results_sorted: List[Tuple[str, str]] = [
		('3 Actor', 'actor'), ('3 Movie', 'movie'), ('Actor 1', 'actor'),
		('Actor 2', 'actor'), ('Movie 1', 'movie'), ('Movie 2', 'movie')
	]
	assert_that(results == expected_results_sorted,
	            f"Error: unexpected result {results}").is_true()


def test_movie_age_function(db: MovieDatabase) -> None:
	"""
	Tests the custom function 'movie_age' to calculate the age of a movie.
	"""
	current_year: int = datetime.now().year
	
	db.add_movie("Movie this year", current_year, "New")
	if db.cursor:
		db.cursor.execute(
			"SELECT movie_age(release_year) FROM movies WHERE title = 'Movie this year';")
		age: Optional[int] = db.cursor.fetchone()[0]
		assert age == 0
	
	db.add_movie("Old movie", current_year - 1, "Old")
	if db.cursor:
		db.cursor.execute(
			"SELECT movie_age(release_year) FROM movies WHERE title = 'Old movie';")
		age = db.cursor.fetchone()[0]
		assert age == 1
	
	db.add_movie("Retro movie", current_year - 30, "Retro")
	if db.cursor:
		db.cursor.execute(
			"SELECT movie_age(release_year) FROM movies WHERE title = 'Retro movie';")
		age = db.cursor.fetchone()[0]
		assert age == 30


def test_get_movies_with_age(db: MovieDatabase) -> None:
	"""
	Tests getting a list of movies along with their ages.
	"""
	current_year: int = datetime.now().year
	db.add_movie("Movie 1", current_year - 5, "Drama")
	db.add_movie("Movie 2", current_year - 10, "Comedy")
	
	movies_with_age: List[Tuple[str, int, int]] = db.get_movies_with_age()
	assert len(movies_with_age) == 2
	assert_that(movies_with_age[0] == ("Movie 1", current_year - 5, 5),
	            f"Error: unexpected result {movies_with_age[0]}").is_true()
	assert_that(movies_with_age[1] == ("Movie 2", current_year - 10, 10),
	            f"Error: unexpected result {movies_with_age[0]}").is_true()


def test_get_all_actors(db: MovieDatabase) -> None:
	"""Tests getting a list of all actors. Tests sorting by name."""
	db.add_actor("Actor_3", 1970)
	db.add_actor("Actor_1", 1980)
	db.add_actor("Actor_2", 1990)
	
	actors: List[Tuple[int, str]] = db.get_all_actors()
	assert_that(len(actors) == 3).is_true()
	assert_that(actors[0][1] == "Actor_1",
	            f"Error: unexpected result {actors[0][1]}").is_true()
	assert_that(actors[1][1] == "Actor_2",
	            f"Error: unexpected result {actors[1][1]}").is_true()
	assert_that(actors[2][1] == "Actor_3",
	            f"Error: unexpected result {actors[2][1]}").is_true()


def test_get_actor_by_id(db: MovieDatabase) -> None:
	"""
	Tests getting an actor by its unique ID.
	"""
	actor_id: Optional[int] = db.add_actor("Test Actor", 1985)
	assert_that(actor_id).is_not_none()
	
	actor_found: Optional[Tuple[int, str]] = db.get_actor_by_id(actor_id)
	assert_that(actor_found == (actor_id, "Test Actor"),
	            f"Error: unexpected result {actor_found}").is_true()
	
	actor_not_found: Optional[Tuple[int, str]] = db.get_actor_by_id(99999)
	assert_that(actor_not_found).is_none()


def test_delete_movie_cascades_to_movie_cast(db: MovieDatabase) -> None:
	"""
	Tests cascading deletion of links in movie_cast when deleting a movie.
	"""
	actor_id: Optional[int] = db.add_actor("Test Actor Актор", 1980)
	assert_that(actor_id).is_not_none()
	movie_id: Optional[int] = db.add_movie("Test movie", 2000, "Comedy",
	                                       [actor_id])
	assert_that(movie_id).is_not_none()
	
	if db.cursor and db.conn:
		db.cursor.execute("SELECT * FROM movie_cast WHERE movie_id = ?",
		                  (movie_id,))
		assert_that(db.cursor.fetchone()).is_not_none()
		
		db.cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
		db.conn.commit()
		
		db.cursor.execute("SELECT * FROM movie_cast WHERE movie_id = ?",
		                  (movie_id,))
		assert_that(db.cursor.fetchone()).is_none()
		
		db.cursor.execute("SELECT * FROM actors WHERE id = ?", (actor_id,))
		assert_that(db.cursor.fetchone()).is_not_none()


def test_delete_actor_cascades_to_movie_cast(db: MovieDatabase) -> None:
	"""
	Tests cascading deletion of relationships in movie_cast when deleting an actor.
	"""
	actor_id: Optional[int] = db.add_actor("Test Actor Актор", 1980)
	assert_that(actor_id).is_not_none()
	movie_id: Optional[int] = db.add_movie("Test movie", 2000, "Comedy",
	                                       [actor_id])
	assert_that(movie_id).is_not_none()
	
	if db.cursor and db.conn:
		db.cursor.execute("SELECT * FROM movie_cast WHERE actor_id = ?",
		                  (actor_id,))
		assert_that(db.cursor.fetchone()).is_not_none()
		
		db.cursor.execute("DELETE FROM actors WHERE id = ?", (actor_id,))
		db.conn.commit()
		
		db.cursor.execute("SELECT * FROM movie_cast WHERE actor_id = ?",
		                  (actor_id,))
		assert_that(db.cursor.fetchone()).is_none()
		
		db.cursor.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
		assert_that(db.cursor.fetchone()).is_not_none()
