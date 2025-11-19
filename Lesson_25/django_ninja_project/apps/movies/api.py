from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response

from .models import Movie, Genre, Review
from .schemas import MovieIn, MovieOut, GenreIn, GenreOut, ReviewIn, ReviewOut

movies_router = Router(tags=["movies"])


# ------------------ Genres ------------------
@movies_router.post("/genres/", response=GenreOut)
def create_genre(request, payload: GenreIn):
	"""Create a new genre."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	genre = Genre.objects.create(**payload.dict())
	return Response(GenreOut.from_orm(genre), status=201)


@movies_router.get("/genres/", response=list[GenreOut])
def list_genres(request):
	"""Retrieve all genres."""
	return Genre.objects.all()


# ------------------ Movies ------------------
@movies_router.post("/", response=MovieOut)
def create_movie(request, payload: MovieIn):
	"""Create a new movies."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	movie = Movie.objects.create(title=payload.title,
	                             description=payload.description,
	                             release_date=payload.release_date,
	                             rating=payload.rating, )
	movie.genres.set(Genre.objects.filter(id__in=payload.genre_ids))
	return Response(MovieOut.from_orm(movie), status=201)


@movies_router.get("/", response=list[MovieOut])
def list_movies(request, genre: str = None, min_rating: float = None,
                release_year: int = None, search: str = None):
	"""Retrieve all movies"""
	qs = Movie.objects.all()
	if genre:
		qs = qs.filter(genres__name__icontains=genre)
	if min_rating:
		qs = qs.filter(rating__gte=min_rating)
	if release_year:
		qs = qs.filter(release_date__year=release_year)
	if search:
		qs = qs.filter(title__icontains=search)
	return qs


@movies_router.get("/{movie_id}", response=MovieOut)
def get_movie(request, movie_id: int):
	"""Get the movies by movie ID"""
	return get_object_or_404(Movie, id=movie_id)


@movies_router.put("/{movie_id}", response=MovieOut)
def update_movie(request, movie_id: int, payload: MovieIn):
	"""Update movie data"""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	movie = get_object_or_404(Movie, id=movie_id)
	for attr, value in payload.dict().items():
		if attr != "genre_ids":
			setattr(movie, attr, value)
	movie.save()
	movie.genres.set(Genre.objects.filter(id__in=payload.genre_ids))
	return movie


@movies_router.delete("/{movie_id}")
def delete_movie(request, movie_id: int):
	"""Get the movies by movie ID"""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	movie = get_object_or_404(Movie, id=movie_id)
	movie.delete()
	return {"success": True}


# ------------------ Reviews ------------------
@movies_router.post("/reviews/", response=ReviewOut)
def add_review(request, payload: ReviewIn):
	"""Add review"""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	movie = get_object_or_404(Movie, id=payload.movie_id)
	review = Review.objects.create(movie=movie, user=request.user,
	                               text=payload.text, score=payload.score)
	return Response(ReviewOut.from_orm(review), status=201)


@movies_router.get("/reviews/{movie_id}", response=list[ReviewOut])
def list_reviews(request, movie_id: int):
	"Retrive list of reviews"
	movie = get_object_or_404(Movie, id=movie_id)
	return movie.reviews.all()
