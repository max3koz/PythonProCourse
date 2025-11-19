from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response

from .models import Book, Rental
from .schemas import BookIn, BookOut, RentalIn, RentalOut

library_router = Router(tags=["library"])


# ------------------ Books ------------------
@library_router.post("/books/", response=BookOut)
def create_book(request, payload: BookIn) -> Response:
	"""Create a new book (auth required)."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	book = Book.objects.create(**payload.dict())
	return Response(BookOut.from_orm(book), status=201)


@library_router.get("/books/", response=list[BookOut])
def list_books(request, title: str = None, author: str = None,
               genre: str = None):
	"""List all books with optional filters."""
	qs = Book.objects.all()
	if title:
		qs = qs.filter(title__icontains=title)
	if author:
		qs = qs.filter(author__icontains=author)
	if genre:
		qs = qs.filter(genre__icontains=genre)
	return qs


@library_router.get("/books/{book_id}", response=BookOut)
def get_book(request, book_id: int):
	"""Retrieve a single book by ID."""
	return get_object_or_404(Book, id=book_id)


@library_router.put("/books/{book_id}", response=BookOut)
def update_book(request, book_id: int, payload: BookIn):
	"""Update an existing book (auth required)."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	book = get_object_or_404(Book, id=book_id)
	for attr, value in payload.dict().items():
		setattr(book, attr, value)
	book.save()
	return book


@library_router.delete("/books/{book_id}")
def delete_book(request, book_id: int):
	"""Delete a book (auth required)."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	book = get_object_or_404(Book, id=book_id)
	book.delete()
	return {"success": True}


# ------------------ Rentals ------------------
@library_router.post("/rentals/", response=RentalOut)
def rent_book(request, payload: RentalIn) -> Response:
	"""Rent a book (auth required)."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	book = get_object_or_404(Book, id=payload.book_id)
	if not book.available:
		return Response({"detail": "Book not available"}, status=400)
	rental = Rental.objects.create(book=book, user=request.user,
	                               return_date=payload.return_date)
	book.available = False
	book.save()
	return Response(RentalOut.from_orm(rental), status=201)


@library_router.post("/rentals/{rental_id}/return")
def return_book(request, rental_id: int):
	"""Return a rented book (auth required)."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	rental = get_object_or_404(Rental, id=rental_id)
	rental.book.available = True
	rental.book.save()
	rental.delete()
	return {"success": True}
